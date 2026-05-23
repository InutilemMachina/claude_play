---
title: CLAUDE.md -- Tantárgy-fejlesztés Meta-Instrukciók
type: meta
status: active
version: 2.0
updated: 2026-05-23
description: Master index. Navigáció, naming conventions, mappastruktúra, fájlkatalógus, dokumentálási protokoll. Tartalmi részletek a hivatkozott fájlokban vannak.
---

# CLAUDE.MD -- Tantárgy-fejlesztés Meta-Instrukciók

_Utolsó frissítés: 2026-05-23_

# 1. Kommunikáció

## 1.1. Emoji státuszok

| Emoji | Jelentés |
|-------|----------|
| 🔲 | TODO |
| ✅ | KÉSZ / OK |
| ⚙️ | FÉLKÉSZ / WIP |
| ❌ | NOK / HIÁNYZIK |
| ❔ | KÉRDÉS / NYITOTT |
| ⚠️ | VIGYÁZAT / FONTOS |
| 🚦 | CHECKPOINT (🔴 blokkolt / 🟢 mehet) |
| ⚡ | HIBA / inkonzisztencia |
| 💬 | NOTE |
| 💡 | IDEA |
| 📎 | LINK (projekten belül) |
| 🔗 | LINK (projekten kívülre) |

## 1.2. Szerepkörök

| Emoji | Ki | Mikor |
|-------|----|-------|
| 😎 | Felhasználó | Manuális teendő, döntés, checkpoint jóváhagyás |
| 🤖 | Claude | Pipeline lépések (01-10) |
| 🐍 | Python script | MinerU, pptx, audit |
| 🔌 | NLM CLI | NLM lekérdezések (Windows-MCP PowerShell hídon) |
| 💻 | Bash/terminal | Fájlműveletek, szkript-futtatás |

# 2. Nevezéktan

## 2.1. Fejléc konvenció

- Dokumentum címe: `# Nagy Kezdőbetűk`
- Első szint: `# 1. Főcím első betű nagy`
- Második szint: `## 1.1. Alcím első betű nagy`
- Sorszámozás kötelező; utolsó szám után `. `; `#` után szóköz.
- Nincs `---` vízszintes vonal (kivétel: prezentációk, YAML frontmatter).

## 2.2. Fájlnév konvenció

- Tananyag (végtermék): mindig **magyar** nyelv
- Meta és skill fájlok neve: **angol**; tartalmuk: **magyar**
- Python kódok: **angol** (name + content); magyarázat: **magyar**
- Heti outputok (`N` = hét száma): `N_Szozedet.md`, `N_Mindmap.md`, `N_Jegyzet.md`, `N_Prezentacio.md`, `N_Kerdesek.md`
- Szóköz tilos -- alulvonás
- Forrás PDF-ek: `vezeteknev2024_tipus.pdf`; azonos esetben: `vezeteknev2024a_tipus.pdf`

## 2.3. Pipeline lépések

| Lépés | Skill | Output |
|-------|-------|--------|
| 00_references_collector | [skills/00_references_collector.md](skills/00_references_collector.md) | forrasok/*.pdf + citations_seed.json |
| 00b_nlm_notebook_setup | [skills/00b_nlm_notebook_setup.md](skills/00b_nlm_notebook_setup.md) | NLM notebook + UUID-k |
| 00c_mineru_extractor | [skills/00c_mineru_extractor.md](skills/00c_mineru_extractor.md) | kepek/ + figure_catalog.json 🐍 |
| 01_nlm_query_runner | [skills/01_nlm_query_runner.md](skills/01_nlm_query_runner.md) | nlm_q*_raw.txt (Q5=ábra) |
| 02_source_controller | [skills/02_source_controller.md](skills/02_source_controller.md) | (belső) 🛑 |
| 03_excerpt_block_maker | [skills/03_excerpt_block_maker.md](skills/03_excerpt_block_maker.md) | N_Jegyzet.md (in-place) |
| 04_citations_maker | [skills/04_citations_maker.md](skills/04_citations_maker.md) | N_Szozedet.md + citations.json 🛑 |
| 05_mindmap_manager | [skills/05_mindmap_manager.md](skills/05_mindmap_manager.md) | N_Mindmap.md |
| 05b_figure_mapper | [skills/05b_figure_mapper.md](skills/05b_figure_mapper.md) | N_Jegyzet.md (FIG placeholderek) |
| 06_notes_collector | [skills/06_notes_collector.md](skills/06_notes_collector.md) | N_Jegyzet.md (Tárgymutató) |
| 07_typesetter | [skills/07_typesetter.md](skills/07_typesetter.md) | N_Jegyzet.md (lint) |
| 08_presentation_maker | [skills/08_presentation_maker.md](skills/08_presentation_maker.md) | N_Prezentacio.md + .pptx 🐍 |
| 09_question_bank_collector | [skills/09_question_bank_collector.md](skills/09_question_bank_collector.md) | N_Kerdesek.md |
| 10_bsc_filter | [skills/10_bsc_filter.md](skills/10_bsc_filter.md) | bsc/ 🐍 |

Archív: `01_html_to_md` (felváltja: 01_nlm_query_runner)

Pipeline flowchart és IO táblázat: [pipeline.md](pipeline.md)

# 3. Mappastruktúra

```
claude_play/                      ← playground (prototipizálás)
├── .claude/
│   ├── CLAUDE.md                 ez a fájl (master index)
│   ├── pipeline.md               pipeline flowchart + IO + checkpointok
│   ├── project_status.md         PDCA log (Plan/Do/Check/Act)
│   ├── pitfalls.md               ismert hibák + gyökérokok (skills ide linkelnek)
│   ├── nlm_integration.md        NLM CLI + Export-Tool + auth + notebook-lista
│   ├── nlm_prompts.md            NLM Configure Chat promptok (Prompt B, C)
│   ├── kepek_workflow.md         képpipeline (MinerU → Md; cross-cutting)
│   ├── settings.local.json       Claude bash engedélyek
│   ├── archive/                  elavult fájlok (nem töröljük)
│   └── skills/
│       └── NN_*.md               skill fájlok (standard struktúrával)
│
├── templates/                    shared -- nincs másolat per-teszt
│   ├── du_template.pptx          master prezentáció sablon
│   ├── context_sablon.md         új tantárgynál másolandó
│   ├── project_status_sablon.md  új tantárgynál másolandó
│   └── assets/                   logók, márka-elemek
│
├── scripts/                      Python szkriptek
│   ├── mineru_pdf.py
│   ├── mineru_rename.py
│   ├── build_figure_catalog.py
│   ├── citations_renumber.py
│   ├── heading_numberer.py
│   ├── bsc_export.py
│   └── pptx_gyarto.py
│
├── tests/                        minden tesztkísérlet
│   ├── matrixprofil/
│   │   ├── forrasok/             topic-szintű forrásanyag (PDF-ek, HTML-ek)
│   │   └── 1_het/
│   │       ├── forrasok/         NLM queryok, citations, kepek/
│   │       ├── N_*.md
│   │       └── bsc/
│   ├── dft/
│   │   └── forrasok/
│   ├── termografia/
│   │   └── forrasok/
│   └── surge_stall_choke/
│       └── forrasok/
│
└── CLAUDE.md                     3 sor: playground leírás + link ide
```

**Tantárgy-szintű struktúra** (éles tantárgyak -- claude_play/ testvérmappái):
```
[tantargy_neve]/
├── .claude/
│   ├── context.md                (templates/context_sablon.md-ből másolva)
│   └── project_status.md         (templates/project_status_sablon.md-ből)
├── templates/                    (claude_play/templates/-ből másolva)
├── scripts/                      (claude_play/scripts/-ből másolva)
└── N_het/
    ├── forrasok/
    └── N_*.md
```

# 4. Dokumentálási protokoll

## 4.1. PDCA szabályok (kötelező)

| Mi történt | Hova kerül | Formátum |
|-----------|-----------|----------|
| Teszt lefutott | `project_status.md §Do` | Dátum + checklist |
| Új hiba | `pitfalls.md` új §N.M | Tünet / Gyökérok / Megoldás |
| Skill javítva | `skills/NN_*.md §Változásjegyzék` | Táblasor |
| Pipeline struktúra változott | `pipeline.md` | In-place frissítés |
| Képpipeline változott | `kepek_workflow.md` | In-place frissítés |
| Következő tennivalók | `project_status.md §Plan` | Prioritástáblázat |

**Aranyszabály:** Skill fájlok LINKELNEK a pitfalls.md-be, sosem másolják a tartalmat.

## 4.2. Token-takarékos műveletek

| Feladat | Helyes módszer | Elkerülendő |
|---------|---------------|-------------|
| Sablon másolása | `bash cp templates/x.md tests/[tema]/N_het/` | Write tool újraírás |
| JSON/ékezetes fájl | `bash cat << 'HEREDOC'` | Write tool |
| Meglévő fájl módosítása | Edit tool (csak a változó rész) | Teljes újraírás |
| Nagy fájl írása | bash heredoc | Write tool pufferrel |

# 5. Fájlkatalógus

| Fájl | Típus | Leírás | Státusz |
|------|-------|--------|---------|
| pipeline.md | meta | Flowchart, IO táblázat, checkpointok | ✅ |
| project_status.md | log | PDCA log: Plan/Do/Check/Act | ✅ |
| pitfalls.md | meta | Ismert hibák + gyökérokok (skills ide linkelnek) | ✅ |
| nlm_integration.md | meta | NLM CLI, Export-Tool, auth, notebook-lista | ✅ |
| nlm_prompts.md | template | NLM Configure Chat promptok (Prompt B, C) | ✅ |
| kepek_workflow.md | meta | Képpipeline: MinerU → Md (cross-cutting) | ✅ |
| archive/ | archívum | Elavult fájlok -- nem töröljük | -- |

# 6. Quick reference

## 6.1. NLM CLI (Windows-MCP PowerShell)

```powershell
$env:PATH = $env:PATH + ";C:\Users\lasz\AppData\Roaming\uv\tools\notebooklm-mcp-cli\Scripts"
nlm notebook list
nlm query notebook "<ID>" "<kérdés>" --json
nlm query notebook "<ID>" "<follow-up>" --conversation-id <id> --json
nlm login   # cookie megújítás (2-4 hetente)
```

## 6.2. Python szkriptek (mineru conda env)

```bash
conda run -n mineru python scripts/mineru_pdf.py tests/[tema]/N_het/forrasok/
conda run -n mineru python scripts/mineru_pdf.py path/to/file.pdf
python scripts/mineru_rename.py tests/[tema]/N_het/forrasok/kepek/[forrás]/auto/ --dry-run
python scripts/bsc_export.py --het N --tantargy [subject_folder]
python scripts/pptx_gyarto.py N_het/N_Prezentacio.md --template templates/du_template.pptx
```

# 7. Környezet

- Windows 10: VSCode + Edge + Claude Desktop (Cowork)
- conda: `mineru` 🐍 (MinerU, képes PDF), `marimoenv` 🐍 (Marimo, Jupyter)
- Claude bővítmények: Excel, Word, PowerPoint, Edge

# 8. Vizualizáció prioritás

1. Inline pipeline string: `lépés1 → lépés2 → lépés3`
2. Mappastruktúra (kód blokk)
3. Felsorolás / táblázat
4. Mermaid flowchart (csak sok lépés / dokumentum esetén)

# 9. Nyitott kérdések

| # | Kérdés | Terület |
|:--|:-------|:--------|
| 1 | Pedagógiai output szekciók: mi a kötelező tartalom? Tanulási célok, főszöveg, kulcsfogalmak, összefoglaló, kérdések -- mennyi, milyen formátumban? | Tartalom |
| 2 | Összefoglaló blokk: szürke háttér MD-ben lehetséges-e? | Tipográfia |
| 3 | bsc/ struktúra lapítása: N_Mindmap.md + N_Mindmap_bsc.md egyszintű forma | Pipeline |
| 4 | Tantárgy .claude/: másolás vs hivatkozás -- éles tantárgynál az egész .claude/-t kell másolni? | Architektúra |
| 5 | context_sablon.md lépésoszlopok (C00-C08): elavultak, frissítés kell | Sablon |
| 6 | Nagy témák (3+ hetes anyag): hogyan osztja meg a forrást több NLM notebook? | Pipeline |
| 7 | Export-Tool Chrome-bővítmény: automatizálható-e Claude in Chrome-mal? | Automatizálás |
| 8 | pymupdf telepítve a mineru env-be? Ha igen, mire? | Környezet |

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-21 | 1.0 | YAML header hozzáadva; _claude/ → .claude/ |
| 2026-05-21 | 1.1 | Inkonzisztenciák javítva: mappalista, checkpoint jelölések |
| 2026-05-23 | 2.0 | Master index refaktor: inline TODOs → §9; pipeline Mermaid → pipeline.md; §3 struktúra egységesítve (3.1+3.2 merge + tests/ + templates/); §4 PDCA protokoll + token-takarékos műveletek; §5 Fájlkatalógus hozzáadva; §6 Quick reference |
