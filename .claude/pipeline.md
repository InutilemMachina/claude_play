---
title: Pipeline.md -- NLM pipeline
type: meta
status: active
version: 5.0
updated: 2026-05-25
description: Pipeline lépések 01-14 + 03b/03c/05/06b alaplépések, IO táblázat, mappastruktúra, checkpointok.
---

# PIPELINE.MD -- NLM Pipeline
NOTE: (IMPORTANT but not at the moment) Távlati cél, afféle északi csillag, ami felé orientálódnunk kell, hogy a pipeline minél inkább mentesüljön a Claude és az emberi vezérléstől, az egyes lépéseket script-ek sorozota kezelné.

NOTE: egyelőre az a legfontosabb, hogy a wip_outputs tartalmilag **magas minőségű** legyen. Később ezekből csinálunk egy prezentációt a `templates\due_prenetation_template.pptx` felhasználásával és egy jegyzetet a `templates\due_jegyzet_template.docx` felhasználásával. 
A bonyolult formaiságok miatt majd megvizsgáljuk a Pandoc használatát is például. 

# 1. Lépések és IO

| Input | Input felelős | Lépés | Automatizáltság / Checkpoint | Output |
|:------|:--------------|:------|:-----------------------------|:-------|
| User PDF-ek, URL-ek | 😎 | [01_references_collector](skills/01_references_collector.md) | 🤖+😎 | `raw_inputs/` + `citations_seed.json` |
| `raw_inputs/` | 🤖+😎 | [02_nlm_notebook_setup](skills/02_nlm_notebook_setup.md) | 🔌 🛑 | NLM notebook + [Prompt B](nlm_prompts.md#2-prompt-b--notebooklm-custom-instructions) + UUID-k |
| `raw_inputs/*.pdf` | 😎 | [03_mineru_extractor](skills/03_mineru_extractor.md) | 🐍 | `clean_inputs/<forrasnev>/` + `raw_outputs/figure_catalog.json` |
| NLM notebook | 🔌 | `scripts/03b_qfig_parser.py` -- Qfig query → caption + keywords | 🐍 | `raw_outputs/figure_catalog.json` (caption + keywords feltöltve) |
| `raw_outputs/figure_catalog.json` | 🐍 | `scripts/03c_dedup_figures.py` -- hash-alapú dedup | 🐍 | `raw_outputs/figure_catalog.json` (`duplicate` flag) |
| NLM notebook (mindmap-vez.) | 🔌 | [04_nlm_query_runner](skills/04_nlm_query_runner.md) | 🔌 | `raw_outputs/nlm_q*.txt` + `raw_outputs/nlm_qfig_raw.txt` |
| `raw_outputs/nlm_q*.txt` | 🔌 | `scripts/05_assemble.py` -- Q1-Q4 összefűzés | 🐍 🛑 | `wip_outputs/N_Jegyzet.md` (draft) |
| `raw_outputs/nlm_q*.txt` | 🔌 | [05_source_controller](skills/05_source_controller.md) | 🤖 🛑 | (belső ellenőrzés) |
| `wip_outputs/N_Jegyzet.md` draft | 🤖 | [06_excerpt_block_maker](skills/06_excerpt_block_maker.md) | 🤖 | `wip_outputs/N_Jegyzet.md` (blockquote-ok) |
| `wip_outputs/N_Jegyzet.md` | 🐍 | `scripts/06b_table_caption_injector.py` -- táblázat feliratok felülre | 🐍 | `wip_outputs/N_Jegyzet.md` (táblázat captionök) |
| `citations_seed.json` + `raw_outputs/` | 🤖 | [07_citations_maker](skills/07_citations_maker.md) | 🤖 🛑 | `wip_outputs/N_Szozedet.md` + `raw_outputs/citations.json` |
| `raw_outputs/nlm_mindmap_raw.txt` | 🔌 | [08_mindmap_manager](skills/08_mindmap_manager.md) | 🤖 | `wip_outputs/N_Mindmap.md` |
| `raw_outputs/figure_catalog.json` + `raw_outputs/` | 🐍 | [09_figure_mapper](skills/09_figure_mapper.md) | 🤖 | `wip_outputs/N_Jegyzet.md` (FIG blokkok) |
| `wip_outputs/N_Jegyzet.md` | 🤖 | [10_notes_collector](skills/10_notes_collector.md) | 🤖 | `wip_outputs/N_Jegyzet.md` (Tartalomjegyzék) |
| `wip_outputs/N_Jegyzet.md` | 🤖 | [11_typesetter](skills/11_typesetter.md) | 🤖 | `wip_outputs/N_Jegyzet.md` (lint + próza) |
| `wip_outputs/N_Jegyzet.md` + template | 🤖 | [12_presentation_maker](skills/12_presentation_maker.md) | 🤖+🐍 | `wip_outputs/N_Prezentacio.md` → `clean_outputs/N_Prezentacio.pptx` |
| NLM notebook (mindmap-vez.) | 🔌 | [13_question_bank_collector](skills/13_question_bank_collector.md) | 🔌+🤖 | `wip_outputs/N_Kerdesek.md` |
| `wip_outputs/N_*.md` | 🤖 | [14_bsc_filter](skills/14_bsc_filter.md) | 🐍 | `clean_outputs/bsc/` |

💡 **Egy NLM notebook = egy hét anyaga.** Prompt B és forrás-UUID-ek per-hét izoláltak.

**NLM promptok:** [nlm_prompts.md](nlm_prompts.md) 
- Prompt A (Claude),
- Prompt B (NLM Configure Chat),
- Prompt C (Data Tables Studio).

💡 **03b→03c→04 sorrend:** Qfig query (03b) az NLM-ből tölti fel a figure_catalog caption+keywords mezőit; 03c deduplikálja; 04 futtatja Q1-Q4-et. A `scripts/05_assemble.py` összefűzi a Q-outputokat draft Jegyzetté.

# 2. Mappastruktúra (heti mappa)

```
test_outputs/<TantargyNeve>/
└── N_het/
    ├── raw_inputs/          😎  nyers forrás PDF-ek, HTML-ek, DOCX-ok (NLM-be töltés előtt)
    │   ├── szerzo2024_tipus.pdf
    │   └── citations_seed.json
    ├── clean_inputs/        🐍  MinerU kimenet, per-forrás almappák
    │   ├── szerzo2024_tipus/
    │   │   ├── images/
    │   │   └── szerzo2024_tipus.md
    │   └── figure_catalog.json
    ├── raw_outputs/         🔌  NLM CLI JSON kimenetek
    │   ├── nlm_q1_raw.txt
    │   ├── nlm_mindmap_raw.txt
    │   └── citations.json
    ├── wip_outputs/         🤖  work-in-progress md + konverziók
    │   ├── N_Jegyzet.md
    │   ├── N_Szozedet.md
    │   ├── N_Mindmap.md
    │   ├── N_Prezentacio.md
    │   └── N_Kerdesek.md
    └── clean_outputs/       ✅  camera-ready végtermékek
        ├── N_Prezentacio.pptx
        ├── N_Jegyzet.docx
        └── bsc/
```

# 3. Mindmap-vezérelt lekérdezés (04, 13)

A lekérdezések a NLM mindmap csomópontjaira épülnek -- nem generikus kérdések.
Az NLM belső query-sablonja:

```
Gyökér:   "Beszélgessen az ezekben a forrásokban tárgyalt <fő node> témakörről."
2. szint: "Beszélgessen az ezekben a forrásokban tárgyalt,
           a(z) <szülő> tágabb kontextusába tartozó <gyerek> témakörről."
```
TODO: több szint is lehetséges, erre való utalást kéne tenni, hogy Depth-First-Search pásztázza végig a mindmap-et. 
Helyes sorrend: **02 (mindmap generálás) → 03 (MinerU) → 04 (lekérdezések mindmap alapján)**.
Részletek: [04_nlm_query_runner.md](skills/04_nlm_query_runner.md) §3.1.

# 4. Checkpointok

A 🛑 jelölések az IO táblázatban (§1) mutatják a checkpoint lépéseket. Bővebb feltételek:

| Checkpoint | Feltétel | Következő lépés |
|:-----------|:---------|:----------------|
| 02 után 🛑 | NLM notebook + Prompt B aktív | 03 + 04 párhuzamosan |
| 05 után 🛑 | 😎 jóváhagyás (source check OK) | 06 indul |
| 07 után 🛑 | 😎 szószedet jóváhagyva | 08-11 sorban |
| 12 után | pptx generált | 13-14 |

TODO: A 12 lépés utáni checkpoint nincs a táblázatban. 

# 5. Forrástípusok

- Tiszta/scannelt PDF (képpel, táblázattal, egyenlettel)
- MS Office: Word, PowerPoint vagy ezek PDF változatai
- Weblap: Edge `--print-to-pdf` mentéssel (képek megtartásához)

⚠️ **Weblap PDF-ként:** `msedge --headless --print-to-pdf="output.pdf" "<URL>"` -- a sima HTML mentés képeket veszít.

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-25 | 5.0 | Új lépések: 03b (Qfig parser), 03c (dedup), 05_assemble.py (formalizálva), 06b (táblázat caption felülre); 04_nlm_query_runner.md: Qfig §4 + szekcióátszámozás; util_heading_numberer.py: Roman-numeral bug javítva; 10_notes_collector.py: ToC + figura beillesztés; 12_pptx_gyarto.py: add_picture + add_table szegmens-alapú renderelés |
| 2026-05-25 | 4.0 | IO táblázat átstrukturálva (Input/Input felelős/Lépés/Automatizáltság/Output); Prompt B + összes NLM prompt linkelve; 🛑 checkpointok a táblázatba beolvasztva; 05_assemble hiányzó lépés jelölve; figure_catalog.json path javítva raw_outputs/-ra |
| 2026-05-24 | 3.0 | Teljes újraírás: 01-14 számozás, raw/clean/wip/clean_outputs mappastruktúra, linkek, TODO-k eltávolítva, mindmap-vezérelt lekérdezés dokumentálva |
| 2026-05-23 | 2.0 | IO táblázat, 00c + 05b beillesztve |
| 2026-05-21 | 1.0 | Létrehozva, NLM-only pipeline |
