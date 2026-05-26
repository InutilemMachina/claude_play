---
title: Pipeline.md -- NLM pipeline
type: meta
status: active
version: 5.0
updated: 2026-05-25
description: Pipeline lépések 01-14 + 03-1/03-2/05/06 alaplépések, IO táblázat, mappastruktúra, checkpointok.
---

# PIPELINE.MD -- NLM Pipeline
NOTE: (IMPORTANT but not at the moment) Távlati cél, afféle északi csillag, ami felé orientálódnunk kell, hogy a pipeline minél inkább mentesüljön a Claude és az emberi vezérléstől, az egyes lépéseket script-ek sorozota kezelné.

NOTE: egyelőre az a legfontosabb, hogy a 4_wip_outputs tartalmilag **magas minőségű** legyen. Később ezekből csinálunk egy prezentációt a `templates\due_prenetation_template.pptx` felhasználásával és egy jegyzetet a `templates\due_jegyzet_template.docx` felhasználásával. 
A bonyolult formaiságok miatt majd megvizsgáljuk a Pandoc használatát is például. 

# 1. Lépések és IO

| Input | Input felelős | Lépés | Automatizáltság / Checkpoint | Output |
|:------|:--------------|:------|:-----------------------------|:-------|
| User PDF-ek, URL-ek | 😎 | [01_references_collector](skills/01_references_collector.md) | 🤖+😎 | `1_raw_inputs/` + `citations_seed.json` |
| `1_raw_inputs/` | 🤖+😎 | [02_nlm_notebook_setup](skills/02_nlm_notebook_setup.md) | 🔌 🛑 | NLM notebook + [Prompt B](nlm_prompts.md#2-prompt-b--notebooklm-custom-instructions) + UUID-k |
| `1_raw_inputs/*.pdf` | 😎 | [03_mineru_extractor](skills/03_mineru_extractor.md) | 🐍 | `2_clean_inputs/<forrasnev>/` + `3_raw_outputs/figure_catalog.json` |
| NLM notebook | 🔌 | `scripts/03-1_qfig_parser.py` -- Qfig query → caption + keywords | 🐍 | `3_raw_outputs/figure_catalog.json` (caption + keywords feltöltve) |
| `3_raw_outputs/figure_catalog.json` | 🐍 | `scripts/03-2_dedup_figures.py` -- hash-alapú dedup | 🐍 | `3_raw_outputs/figure_catalog.json` (`duplicate` flag) |
| NLM notebook (mindmap-vez.) | 🔌 | [04_nlm_query_runner](skills/04_nlm_query_runner.md) | 🔌 | `3_raw_outputs/nlm_q*.txt` + `3_raw_outputs/nlm_qfig_raw.txt` |
| `3_raw_outputs/nlm_q*.txt` | 🔌 | `scripts/05_assemble.py` -- Q1-Q4 összefűzés | 🐍 🛑 | `4_wip_outputs/N_Jegyzet.md` (draft) |
| `3_raw_outputs/nlm_q*.txt` | 🔌 | [05_source_controller](skills/05_source_controller.md) | 🤖 🛑 | (belső ellenőrzés) |
| `4_wip_outputs/N_Jegyzet.md` draft | 🤖 | [06_excerpt_block_maker](skills/06_excerpt_block_maker.md) | 🤖 | `4_wip_outputs/N_Jegyzet.md` (blockquote-ok) |
| `4_wip_outputs/N_Jegyzet.md` | 🐍 | `scripts/06_table_caption_injector.py` -- táblázat feliratok felülre | 🐍 | `4_wip_outputs/N_Jegyzet.md` (táblázat captionök) |
| `citations_seed.json` + `3_raw_outputs/` | 🤖 | [07_citations_maker](skills/07_citations_maker.md) | 🤖 🛑 | `4_wip_outputs/N_Szozedet.md` + `3_raw_outputs/citations.json` |
| `3_raw_outputs/nlm_mindmap_export.md` (😎 Ultra Explorer export) | 😎 | [08_mindmap_manager](skills/08_mindmap_manager.md) | 🤖 | `4_wip_outputs/N_Mindmap.md` |
| `3_raw_outputs/figure_catalog.json` + `3_raw_outputs/` | 🐍 | [09_figure_mapper](skills/09_figure_mapper.md) | 🤖 | `4_wip_outputs/N_Jegyzet.md` (FIG blokkok) |
| `4_wip_outputs/N_Jegyzet.md` | 🤖 | [10_notes_collector](skills/10_notes_collector.md) | 🤖 | `4_wip_outputs/N_Jegyzet.md` (Tartalomjegyzék) |
| `4_wip_outputs/N_Jegyzet.md` | 🤖 | [11_typesetter](skills/11_typesetter.md) | 🤖 | `4_wip_outputs/N_Jegyzet.md` (lint + próza) |
| `4_wip_outputs/N_Jegyzet.md` + template | 🤖 | [12_presentation_maker](skills/12_presentation_maker.md) | 🤖+🐍 | `4_wip_outputs/N_Prezentacio.md` → `5_clean_outputs/N_Prezentacio.pptx` |
| NLM notebook (mindmap-vez.) | 🔌 | [13_question_bank_collector](skills/13_question_bank_collector.md) | 🔌+🤖 | `4_wip_outputs/N_Kerdesek.md` |
| `4_wip_outputs/N_*.md` | 🤖 | [14_bsc_filter](skills/14_bsc_filter.md) | 🐍 | `5_clean_outputs/` |

💡 **Egy NLM notebook = egy hét anyaga.** Prompt B és forrás-UUID-ek per-hét izoláltak.

**NLM promptok:** [nlm_prompts.md](nlm_prompts.md) 
- Prompt A (Claude),
- Prompt B (NLM Configure Chat),
- Prompt C (Data Tables Studio).

💡 **03-1→03-2→04 sorrend:** Qfig query (03-1) az NLM-ből tölti fel a figure_catalog caption+keywords mezőit; 03-2 deduplikálja; 04 futtatja Q1-Q4-et. A `scripts/05_assemble.py` összefűzi a Q-outputokat draft Jegyzetté.

# 2. Mappastruktúra (heti mappa)

```
test_outputs/<TantargyNeve>/
└── N_het/
    ├── 1_raw_inputs/          😎  nyers forrás PDF-ek, HTML-ek, DOCX-ok (NLM-be töltés előtt)
```


```
test_outputs/<TantargyNeve>/
└── N_het/
    ├── 1_raw_inputs/          😎  nyers forrás PDF-ek, HTML-ek, DOCX-ok (NLM-be töltés előtt)
    │   ├── szerzo2024_tipus.pdf
    │   └── citations_seed.json
    ├── 2_clean_inputs/        🐍  MinerU kimenet, per-forrás almappák
    │   ├── szerzo2024_tipus/
    │   │   ├── images/
    │   │   └── szerzo2024_tipus.md
    │   └── figure_catalog.json
    ├── 3_raw_outputs/         🔌  NLM CLI JSON kimenetek
    │   ├── nlm_q1_raw.txt
    │   ├── nlm_mindmap_export.md  (😎 Ultra Explorer export ide kerül)
    │   └── citations.json
    ├── 4_wip_outputs/         🤖  work-in-progress md + konverziók
    │   ├── N_Jegyzet.md
    │   ├── N_Szozedet.md
    │   ├── N_Mindmap.md
    │   ├── N_Prezentacio.md
    │   └── N_Kerdesek.md
    └── 5_clean_outputs/       ✅  camera-ready végtermékek
        ├── N_Prezentacio.pptx
        ├── N_Jegyzet.docx
        └── (BSc outputok _bsc suffixszel)
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

# 5. Pipeline-szintű szabályok

NOTE ⚠️ **Dash kiirtás (Rule H):** Minden `4_wip_outputs/` és `5_clean_outputs/` fájlban tilos a `--` (dupla kötőjel), `–` (n-dash) és `—` (m-dash). Magyarban ezek szinte mindig hibák (NLM formázási mellékhatás). Megoldandó: `11_typesetter.py` Rule H-ként implementálni, amely az összes output fájlból eltávolítja.

NOTE ⚠️ **NLM Studio Mindmap -- architektúrai sarokkő:** A Studio Gondolattérkép exportja (08. lépés, Ultra Explorer bővítmény) adja a lekérdezési struktúrát (04), a BSc/MSc határt (13-14) és a pedagógiai szerkezetet (05, 06). Ha ez kiesik vagy rosszul generálódik, az egész downstream csonka. A mindmap export minőségét mindig ellenőrizni kell az NLM notebook felállítása után (02. lépés checkpoint).

# 6. Forrástípusok

NOTE (architektúrai gap): Minden forrástípushoz definiálni kell egy **determinisztikus extraktort**, amely `2_clean_inputs/<forrás>/` struktúrát hoz létre (szöveg + képek). Jelenleg csak PDF lefedett:

| Forrástípus | Extraktor | Státusz |
|:------------|:----------|:--------|
| PDF | MinerU (`03_run_mineru_pipeline.py`) | ✅ definiált |
| PPTX | PDF-konverzió → MinerU | ❔ tervezendő |
| DOCX | Pandoc / python-docx | ❔ tervezendő |
| HTML (URL) | NLM-be URL-ként (de `2_clean_inputs` nem keletkezik) | ⚠️ részleges |
| HTML (helyi) | Nincs | ❌ hiányzik |

- Tiszta/scannelt PDF (képpel, táblázattal, egyenlettel)
- MS Office: Word, PowerPoint vagy ezek PDF változatai
- Weblap: Edge `--print-to-pdf` mentéssel (képek megtartásához)

⚠️ **Weblap PDF-ként:** `msedge --headless --print-to-pdf="output.pdf" "<URL>"` -- a sima HTML mentés képeket veszít.

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-25 | 5.1 | Heading hierarchia gap NOTE (05_assemble Q1); §5 Pipeline-szintű szabályok (Rule H dash cleanup, mindmap sarokkő) |
| 2026-05-26 | 6.0 | M3: mappanév konvenció (1_raw_inputs..5_clean_outputs); M2: YAML name mezők szinkronizálva; 06b/03b/03c átnevezve 06/03-1/03-2 |
| 2026-05-25 | 5.0 | Új lépések: 03-1 (Qfig parser), 03-2 (dedup), 05_assemble.py (formalizálva), 06 (táblázat caption felülre); 04_nlm_query_runner.md: Qfig §4 + szekcióátszámozás; util_heading_numberer.py: Roman-numeral bug javítva; 10_notes_collector.py: ToC + figura beillesztés; 12_pptx_gyarto.py: add_picture + add_table szegmens-alapú renderelés |
| 2026-05-25 | 4.0 | IO táblázat átstrukturálva (Input/Input felelős/Lépés/Automatizáltság/Output); Prompt B + összes NLM prompt linkelve; 🛑 checkpointok a táblázatba beolvasztva; 05_assemble hiányzó lépés jelölve; figure_catalog.json path javítva 3_raw_outputs/-ra |
| 2026-05-24 | 3.0 | Teljes újraírás: 01-14 számozás, raw/clean/wip/5_clean_outputs mappastruktúra, linkek, TODO-k eltávolítva, mindmap-vezérelt lekérdezés dokumentálva |
| 2026-05-23 | 2.0 | IO táblázat, 00c + 05b beillesztve |
| 2026-05-21 | 1.0 | Létrehozva, NLM-only pipeline |
