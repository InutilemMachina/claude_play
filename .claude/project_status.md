---
title: Project Status -- Playground PDCA log
type: log
status: active
version: 2.0
updated: 2026-05-23
description: Playground (claude_play) PDCA log. Session elején Claude olvassa be. NEM tantárgy-specifikus.
---

# Project Status -- Playground PDCA Log

_Frissítve: 2026-05-23 (2. update)_

# 1. Plan (következő lépések)

_Frissítve: 2026-05-24 -- ACT a diagnosztika alapján_

| # | Feladat | Felelős | Megjegyzés |
|:--|:--------|:--------|:-----------|
| **P1** | **Pipeline output újrafuttatás** -- mind a 3 hét (03-10 skill-ek) ékezetes magyarral | 🤖+👤 | ❌ KRITIKUS -- 15 fájl 0% ékezet; csak az NLM clean_sources OK |
| **P2** | **MatrixProfil HTML forrás** -- SingleFile mentés → NLM upload → lekérdezés | 🤖+👤 | Chrome-on manuális lépés; majd nlm_query.py |
| **P3** | **matrixprofil Q4** újrafuttatás | 🤖 | Jelenleg [SIM] placeholder -- valós NLM query kell |
| **P4** | **citations.json minőség** -- `file` és `title` mezők kitöltése | 🤖 | source_1 generikus → valós fájlnév |
| B | **NLM Prompt B automatizálás** vizsgálata -- CLI vagy Chrome | 🤖 | Megjegyzés: ASCII-ot küld CLI-n; ékezetes UI-on kell beállítani |
| C | **NLM metapromptok pedagógiai felülvizsgálata** | 🤖+👤 | nlm_prompts.md átírás |
| D | **du_template.pptx** megszerkesztése | 👤 | Hiányzik, bypass él |
| E | **PDF-ek feltöltése** (MP I, II) + MinerU futtatása | 👤 | kepek_workflow.md §8 |
| G | **context_sablon.md lépésszámok frissítése** | 🤖 | C00-C08 oszlopok elavultak |

# 2. Do (elvégzett munkák)

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
| Képek | ❌