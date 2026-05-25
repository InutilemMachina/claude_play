---
title: Project Status -- Playground PDCA log
type: log
status: active
version: 2.4
updated: 2026-05-25
description: Playground (claude_play) PDCA log. Session elején Claude olvassa be. NEM tantárgy-specifikus.
---

# Project Status -- Playground PDCA Log

_Frissítve: 2026-05-23 (2. update)_

# 1. Plan (következő lépések)

_Frissítve: 2026-05-24 -- refactor/v2 branch_

| # | Feladat | Felelős | Megjegyzés |
|:--|:--------|:--------|:-----------|
| **R1** | **Termografia_teszt_v3 pipeline futtatás** -- új mappastruktúrával (raw_inputs/clean_inputs/raw_outputs/wip_outputs/clean_outputs) | 🤖+😎 | 🔲 következő prioritás |
| **R2** | **MinerU** -- `03_run_mineru_pipeline.py` tesztje Termografia_teszt_v3-on | 🐍 | 🔲 |
| **R3** | **context_sablon.md** lépésszámok frissítése (C00-C08 → 01-14) | 🤖 | 🔲 |
| **R4** | **nlm_integration.md notebook-lista** frissítése (Termografia v2+v3 hozzáadva) | 🤖 | 🔲 -- beolvadt 02_nlm_notebook_setup-ba |
| **R5** | **NLM Prompt B pedagógiai felülvizsgálata** | 🤖+😎 | nlm_prompts.md átírás |
| **R6** | **du_template.pptx** megszerkesztése | 😎 | hiányzik, bypass él |
| **R7** | **03_mineru_extractor**: tesztelés -- per-forrás clean_inputs/<nev>/ almappa | 🐍 | 🔲 |

# 2. Do (elvégzett munkák)

## 2026-05-25 -- Content quality session (feature/content-quality)

- ✅ `scripts/03b_qfig_parser.py` -- Qfig NLM output → figure_catalog caption+keywords
- ✅ `scripts/03c_dedup_figures.py` -- hash-alapú figura deduplication (duplicate flag)
- ✅ `scripts/05_assemble.py` -- Q1-Q4 összefűzés, CLI-alapú, portábilis (hardcoded _assemble.py felváltja)
- ✅ `scripts/06b_table_caption_injector.py` -- GFM táblázat captionök FELÜLRE injektálása
- ✅ `scripts/09_figure_mapper.py` -- keyword × paragraph matching (dict-formátum javítva)
- ✅ `scripts/10_notes_collector.py` -- ToC generálás + figura beillesztés paragraph-koordináta alapján
- ✅ `scripts/11_typesetter.py` -- két fázis: bullet→próza (Claude API) + linting (Phase 1 megtartva)
- ✅ `scripts/12_pptx_gyarto.py` -- szegmens-alapú body: add_picture + add_table + text
- ✅ `scripts/util_heading_numberer.py` -- Roman-numeral double-prefix bug javítva
- ✅ `.claude/skills/04_nlm_query_runner.md` -- Qfig §4 hozzáadva, szekcióátszámozás, YAML name javítva
- ✅ `.claude/pipeline.md` -- v5.0: 03b/03c/05/06b lépések beillesztve, ⚠️ megjegyzés feloldva
- ✅ Git commit: `feature/content-quality` branch

## 2026-05-24 -- P1 pipeline output újragenerálás

- ✅ `scripts/regen_outputs.py` futtatva: 15+15 fájl újragenerálva ékezetes magyarral
- ✅ Ékezetsűrűség: 5-13% minden pipeline outputban (✓ küszöb: >1.5%)
- ✅ 0% maradék: `stumpy2024_webpage.md`, `rockmore1999_article.md` -- MinerU angol forrásanyag (helyes)

## 2026-05-24 -- Diagnosztika + kódolásjavítás

- ✅ pipeline.md: 55 mojibake csere (emoji + →); C1-control fallback logika
- ✅ pitfalls.md: 13 csere (§, →, á, é, Á, 🗺, 💡)
- ✅ 00c_mineru_extractor.md: 14 csere (§, →, Á, 🐍, 🔌)
- ✅ nlm_prompts.md: cím "es" → "és" (2x)
- ✅ .gitignore: `.raw_sources/` → `**/raw_sources/`, `.clean_sources/` → `**/clean_sources/`
- ✅ project_status.md: §Check + §Plan frissítve (diagnosztika eredményei)
- ❌ LELET: 15 pipeline output fájl 0% ékezetsűrűség -- újrafuttatás szükséges

## 2026-05-23 -- Meta-fájlok konszolidáció (2. kör)

- ✅ .claude/CLAUDE.md törölve -- tartalom root CLAUDE.md v3.0-ban
- ✅ pipeline.md: §6 Heti outputok törölve (duplikátum); NLM granularitás note + Nyitott kérdések szekció hozzáadva
- ✅ project_status.md: §4 Act + §5 Arch törölve (git history + CLAUDE.md lefedi)
- ✅ nlm_integration.md v2.1: YAML fix, --- elválasztók eltávolítva, Változásjegyzék táblává
- ✅ Nyitott kérdések elosztva: 06_notes_collector, 10_bsc_filter, 00b_nlm_notebook_setup, pipeline.md
- ✅ context_sablon.md: C00-C08 oszlopok → 00b/01/02/03-05/06-07/08/09/10
- ✅ git commit: 2 commit, összesen 329 sor törlés + 150 hozzáadás

## 2026-05-23 -- Workspace rendrakás

- ✅ Mappastruktúra refaktor: tests/, templates/, .claude/ konszolidáció
- ✅ test_sources_* → tests/*/forrasok/ (matrixprofil, dft, termografia, surge_stall_choke)
- ✅ matrixprofil_teszt_2 (kanonikus) → tests/matrixprofil/1_het/
- ✅ 1_Prezentacio.md + .pptx (teszt_1-ből) → tests/matrixprofil/1_het/
- ✅ templates/ létrehozva: du_template.pptx, context_sablon.md, project_status_sablon.md, assets/
- ✅ kepek_workflow.md v2.0: figure_pipeline_design.md + mineru_kepek_nevezektan.md beolvasztva
- ✅ pipeline.md v2.0: 01_nlm_query_runner, 00c, 05b beillesztve; IO táblázat hozzáadva
- ✅ CLAUDE.md újraírva master indexként (v2.0)
- ✅ git init + .gitignore
- ✅ Archivált: nlm-claude_integration_research.md, pipeline_next_steps.md, DFT_teszt*.md, _claude/, sablonok

## 2026-05-22 -- Teljes end-to-end pipeline-teszt (MP 1. hét)

- ✅ Mappastruktúra: matrixprofil_teszt/1_het/forrasok/ + Studio outputok
- ✅ 05_mindmap_manager: Export-Tool MD → Mermaid flowchart LR
- ✅ NLM lekérdezések (4 db, level-2): Áttekintés, Alapfogalmak, Algoritmusok, Alkalmazások
- ✅ 1_Jegyzet.md összeállítva (329 sor) + citations.json (6 forrás, UUID-ek)
- ✅ 06_notes_collector: Tárgymutató (22 anchor-link)
- ✅ 03_excerpt_block_maker: 13 💡 + 4 🗺️ blokk
- ✅ 07_typesetter: A=1, D=21 javítás
- ✅ 08_presentation_maker: 1_Prezentacio.md (14 dia) + 1_Prezentacio.pptx
- ✅ scripts/pptx_gyarto.py megírva (Marp MD → PPTX)
- ✅ 09_question_bank_collector: 1_Kerdesek.md (4 BSc + 2 MSc kérdés)
- ✅ 10_bsc_filter: bsc_export.py megírva + bsc/ feltöltve (4 fájl)

## 2026-05-21 -- NLM CLI integráció + DFT teszt

- ✅ NLM CLI integráció tesztelve (notebooklm-mcp-cli, Windows-MCP PowerShell hídon)
- ✅ DFT teszt 1 és 2: PASS
- ✅ **Kritikus lelet:** Prompt B (Configure Chat) hat a CLI-re
- ✅ nlm_prompts.md (rev2), nlm_integration.md (rev2), CLAUDE.md inkonzisztenciák javítva

## 2026-05-20 -- .claude/ megtisztítás

- ✅ NLM-only pipeline; nevezéktan és pipeline.md egységesítve

# 3. Check (tanulságok az utolsó futásból)

## 2026-05-25 -- feature/content-quality: architektúrai döntések

### P4/P6 revízió: NLM ingyenes alternatíva a Claude Vision API helyett

**Probléma:** Az előző session P4/P6 tervei Claude Vision API hívásokat alkalmaznak (claude-sonnet-4-6) képenként → fizetős, lassú (131 kép × API hívás).

**Döntés:** Az NLM ingyenes és már látja a PDF forrásokat (szöveges és vizuális tartalmat egyaránt). Egy dedikált NLM figura-query (Qfig) kérhető a notebooktól:

```
"Sorold fel az összes ábrát, diagramot és táblázatot a forrásokban! Minden elemhez add meg:
a forrás nevét, az ábra számát (ha van), a captionját (ha van), és 1-2 mondatos leírását."
```

Ez a kimenet:
- Feldolgozható regex-szel → `keywords` + `caption` mezők a `figure_catalog.json`-ban
- Ingyenes (NLM kvóta terhére)
- Kontextuálisan gazdagabb (NLM ismeri az ábra körüli szöveget is)

**Következmény:**
- `scripts/03_build_figure_catalog.py --vlm` (Claude Vision API): elhalasztva / opcionális fallback
- `scripts/09_figure_mapper.py` algoritmusa változatlan marad (keywords × paragraph matching)
- Új lépés: **Qfig** query a `04_nlm_query_runner`-ben (Q1-Q4 mellett)
- P4/P6 státusza: script kész, de éles futtatás Qfig-alapú megközelítéssel tesztelendő

| | Vision API (régi terv) | NLM Qfig (új terv) |
|:--|:--|:--|
| Költség | Fizetős | Ingyenes |
| Sebesség | Lassú (131 hívás) | Egy query |
| Kontextus | Kép pixelei | Kép + körülötte lévő szöveg |
| Megbízhatóság | Magas (direkt látás) | Közepes (NLM értelmezi) |
| Implementáció | `--vlm` flag, kész | Qfig query + parser, TODO |

### _assemble.py: rossz helyen van, hiányzik a pipeline-ból

**Tünet:** `test_outputs/Termografia_teszt_v3/_assemble.py` létezik; a `scripts/` mappában nincs assembler; a pipeline 04→06 között nincs dokumentált lépés, pedig `N_Jegyzet.md` draft-ot valahogy létre kell hozni.

**Gyökérok:** Az assembler ad-hoc, tesztelés közben íródott, sosem lett formalizálva.

**Megoldás:**
- `_assemble.py` → `scripts/05_assemble.py` (átnevezés + CLI argumentumok, abs. path eltávolítás)
- Pipeline-ba beillesztés: `04_nlm_query_runner` → **05_assemble** → `05_source_controller` → `06_excerpt_block_maker`
- Skill fájl: `.claude/skills/05_assemble.md` (TODO)
- `_assemble.py` eredeti helye (`test_outputs/`) gitignore-d -- sosem volt a repóban

**Dokumentálva:** pipeline.md v4.0 -- ⚠️ jelöléssel a hiányzó lépésnél.

## 2026-05-22 -- MP 1. hét end-to-end teszt

| Komponens | Eredmény | Tanulság |
|:----------|:---------|:---------|
| NLM CLI + Prompt B | ✅ PASS | Strukturált citáció, LaTeX képletek, táblázatok jól működnek |
| 05_mindmap_manager | ✅ PASS | Export-Tool MD → Mermaid konverzió megbízható |
| 06_notes_collector | ✅ PASS | Anchor-link ékezetes magyar szövegre is helyes |
| 03_excerpt_block_maker | ✅ PASS | whitespace szabály (\n\n>) beépítve |
| 07_typesetter Rule D | ⚠️ 21 javítás | 03 whitespace fix után várhatóan csökken |
| 09_question_bank_collector | ✅ PASS | NLM BSc/MSc differenciált kérdések |
| 10_bsc_filter | ✅ PASS | Hármas szűrés (MSc blokk + Mermaid node + SZINT) rögtön jól működött |
| Citation globális sorszámozás | ❌ | NLM query-nként [1]-től számoz → UUID-dedup szükséges (04 skillben) |
| pptx_gyarto.py LaTeX | ❌ | python-pptx nem tud LaTeX-et -- elfogadott korlát |
| Képek | ❌ | PDF-ek hiányoztak → placeholder rendszer (kepek_workflow.md) |

## 2026-05-24 -- 3 hetes teszt diagnosztika (teljes scan)

| Komponens | Eredmény | Tanulság |
|:----------|:---------|:---------|
| pipeline.md emoji mojibake | ✅ JAVÍTVA | 55 csere (🚀👤🤖🐍🔌🛑💡✅⚠️→); C1-control fallback szükséges a 🐍-hez |
| pitfalls.md mojibake | ✅ JAVÍTVA | 13 csere; §6.1 példa-stringek részben javultak (mellékhatás) |
| 00c_mineru_extractor.md | ✅ JAVÍTVA | 14 csere |
| Összes skill fájl (15 db) | ✅ TISZTA | Nincs mojibake |
| NLM outputok (clean_sources) | ✅ OK | Helyes magyar ékezetekkel, táblázat + LaTeX + citáció ✓ |
| nlm_prompts.md Prompt B | ✅ SZÁNDÉKOS | ASCII ékezetnélküliség dokumentált (PowerShell compat.) |
| nlm_prompts.md cím | ✅ JAVÍTVA | "es" → "és" (2 helyen) |
| .gitignore raw/clean_sources | ✅ JAVÍTVA | `.raw_sources/` → `**/raw_sources/` (pont hiba) |
| **Pipeline outputok (15 fájl)** | ❌ **KRITIKUS** | **0% ékezetsűrűség** -- minden heti output ékezet nélküli magyar. Gyökérok: a pipeline-futás idején a skill fájlok mojibake-ben voltak → Claude ékezetnélkülien generált. Újrafuttatás szükséges. |
| matrixprofil Q4 | ⚠️ SZIMULÁLT | [SIM] flag -- valós NLM query nem futott le |
| citations.json | ⚠️ HIÁNYOS | `file` mező üres, `title` = 'source_1' generikus |

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-25 | 2.3 | Check: NLM vs Vision API döntés + _assemble.py probléma dokumentálva |
| 2026-05-25 | 2.2 | feature/content-quality Do szekció; Plan P-státuszok frissítve |
| 2026-05-22 | 1.0 | Létrehozva: Do szekciók, következő lépések |
| 2026-05-23 | 2.0 | PDCA struktúra: Plan/Do/Check/Act; tanulságok táblázatba rendezve; pipeline_next_steps.md beolvasztva |
| 2026-05-23 | 2.1 | §4 Act + §5 Arch törölve (git history + CLAUDE.md/pipeline.md lefedi) |

## 2026-05-24 -- refactor/v2: teljes pipeline és meta-mappa refaktorálás

- ✅ Git branch: `refactor/v2` létrehozva
- ✅ Skill fájlok átnevezve: 00/00b/00c/01..10 → 01-14 prefixek
- ✅ Script fájlok átnevezve: `NN_script.py` konvenció
- ✅ `01_html_to_md.md` archivált (elavult skill)
- ✅ `kepek_workflow.md` → `03_mineru_extractor.md`-be beolvasztva, archivált
- ✅ `nlm_integration.md` → `02_nlm_notebook_setup.md`-be beolvasztva, archivált
- ✅ `03_run_mineru_pipeline.py`: `magic-pdf` → `mineru`, `raw_inputs/`, `clean_inputs/<forrás>/`
- ✅ `pipeline.md` v3.0: TODO-k eltávolítva, 01-14 lépések, IO táblázat aktív linkekkel
- ✅ `CLAUDE.md` v4.0: §0 Session indítás szekció, új mappastruktúra, 01-14 katalógus
- ✅ Mappastruktúra: `raw_inputs/` + `clean_inputs/` + `raw_outputs/` + `wip_outputs/` + `clean_outputs/`
- ✅ `test_outputs/` mint kimeneti gyökér mappa
- ⚠️ MinerU teszt (Termografia_teszt_v2): process futott, de 0 fájl keletkezett -- R2 tesztelés szükséges

## 2026-05-24 -- Termografia_teszt_v2 teljes pipeline futtatás

- ✅ Mappastruktúra: Termografia_teszt_v2/1_het/ + raw_sources/ + clean_sources/ + bsc/
- ✅ HTML forrás: Emissivity - Wikipedia, web_fetch-el mentve (képek nélkül -- SingleFile CLI teszt köv.)
- ✅ Fájlválogatás: 4 PDF + 3 URL (html) + 1 DOCX = 8 forrás (raw_sources-ban)
- ✅ 00b: NLM notebook létrehozva (ID: 21c5da9f), 9 forrás feltöltve (1 duplikátum), Prompt B aktív
- ✅ 01: Q1-Q4 NLM lekérdezések, 7.7-8.8% ékezetűség; Q2 numbered cit., Q1/3/4 inline cit.
- ✅ 02-07: Jegyzet (21590 char), Szószedet (15 fogalom), Mindmap (Mermaid, 6 node), Citations.json
- ✅ 08: Prezentáció (9 dia Marp MD + 105KB PPTX)
- ✅ 09: Kérdések (4 BSc + 2 MSc, LaTeX képletekkel)
- ✅ 10: BSc filter (Prezentáció -15 sor, Kérdések -17 sor)
- ✅ self_attention_log.md: 17 bejegyzés, 3 pitfall dokumentálva
- ⚠️ NYITOTT: SingleFile CLI teszt -- képeket tartalmazó HTML (user kérés)

## Do -- 2026-05-25 (feature/content-quality: minőségi réteg)

| # | Feladat | Eredmény |
|:--|:--------|:---------|
| P2 | JAMP forrás eltávolítása NLM notebookból (`nlm source delete`) + citations_seed.json | ✅ 3 forrás maradt; `nlm source list` ellenőrizve |
| P3 | Q1 query redesign: `04_nlm_query_runner.md` v1.2 -- bevezető/összefoglaló szerepkör; redundancia-szabály; §5.2 citations fallback frissítve; Q4 minta hozzáadva | ✅ |
| P1 | `11_typesetter.md` v2.0 -- kétfázisú működés (prose + linting) dokumentálva; `scripts/11_typesetter.py` megírva | ✅ |
| P4 | `scripts/03_build_figure_catalog.py` -- VLM bővítés: `--vlm` flag, `run_vlm_on_catalog()`, `vlm_done` + `inserted_after_paragraph` mezők | ✅ szintaxis OK |
| P6 | `09_figure_mapper.md` v2.0 teljes újraírás (VLM keywords × bekezdés matching); `scripts/09_figure_mapper.py` megírva | ✅ szintaxis OK |

Nem elvégzett (következő session):
- [ ] P5: HTML források NLM-be URL-ként (`nlm source add --url`)
- [ ] Q1-Q4 újrafuttatás a megtisztított (JAMP nélküli) notebookban
- [ ] `11_typesetter.py` éles futtatása a meglévő `wip_outputs/1_Jegyzet.md`-n
- [ ] `03_build_figure_catalog.py --vlm` futtatás (131 kép)
- [ ] `09_figure_mapper.py` futtatás a VLM catalog után

## Do -- 2026-05-25 (Termografia_teszt_v3 pipeline futás)

- [x] raw_inputs -> raw_inputs átnevezés (v3 mappa)
- [x] 03 MinerU: 4 PDF feldolgozva -> clean_inputs/<stem>/auto/ (kettős nesting bug javítva)
- [x] 02 NLM notebook "Termografia_teszt_v3" létrehozva (ID: 15b84ae7...)
- [x] 02 Prompt B konfigurálva (Python subprocess)
- [x] 04 Q1-Q4 NLM lekérdezések -> raw_outputs/ (Q1:5.6KB, Q2:3.4KB, Q3:3.9KB, Q4:3.6KB)
- [x] 05 citations_seed.json létrehozva (4 forrás + notebook meta)
- [x] 10 1_Jegyzet.md assembly -> wip_outputs/ (18.5 KB)
- [x] 06 1_Szozedet.md -> wip_outputs/ (4 KB)
- [x] 08 1_Mindmap.md -> wip_outputs/ (3.1 KB)
- [x] 13 1_Kerdesek.md -> wip_outputs/ (4 KB)
- [x] pitfalls.md §4.3 hozzáadva (MinerU kettős nesting)
- [x] scripts/03_run_mineru_pipeline.py javítva (clean_dir / pdf.stem -> clean_dir)

Nyitott:
- [ ] 1_Prezentacio.md + .pptx (12_pptx_gyarto.py)
- [ ] 14 BSc filter futtatása
- [ ] context.md v3 frissítése (notebook ID, státuszok)
- [ ] util_heading_numberer.py: dupla prefix bug (### I. -> ### 1.1. I.)
# 3. Plan -- feature/content-quality branch

_Frissitve: 2026-05-25_

Branch celja: eletszeru wip_outputs -- utan pipeline teljes automatizalasa.
Heurisztikak TILOSAK (pl. page_idx koezelites) -- minden lepes automatizalhato kell legyen.

## Prioritasok

| # | Feladat | Automatizhato? | Státusz |
|:--|:--------|:---------------|:--------|
| P1 | **11_typesetter**: WIP md -> olvasható próza (Claude API hívás) | igen (API) | ✅ script + skill kész; futtatás szükséges |
| P2 | **JAMP forrás eltávolítás** NLM notebookból + citations_seed-ből | igen (nlm CLI) | ✅ KÉSZ |
| P3 | **Q1 query redesign**: bevezető/összefoglaló csak, ne teljes lefedés | igen | ✅ KÉSZ |
| P4 | **VLM captioning**: képenként Claude vision API -> értelmes caption | igen (API, lassú) | ✅ script kész; `--vlm` futtatás szükséges |
| P5 | **HTML források NLM-be** URL-ként | igen (nlm CLI) | 🔲 következő session |
| P6 | **09_figure_mapper**: VLM keywords × NLM szöveg → beillesztési pont | igen | ✅ script + skill kész; P4 után futtatható |

## Architekturalis dontes (P4/P6)

A kep-szoveg illesztes automatizalhato ut:
  1. MinerU -> kep fajlok (clean_inputs/<stem>/auto/images/)
  2. Claude vision API per kep -> caption + kulcsszavak (03_build_figure_catalog.py bovitese)
  3. NLM szovegben kulcsszo-keresés -> beillesztési pont azonosítása
  4. Assembly: kep a megfelelo bekezdes utan

Ez 100%-ban automatizalhato, heurisztika-mentes.

## Kernel kerdes

Melyik modell latja a kepeket?
  - Claude vision (claude-sonnet-4-6): igen, API-n at
  - NLM: nem latja a PDF abrakat, csak a szoveget
  => VLM lepes: Claude, nem NLM