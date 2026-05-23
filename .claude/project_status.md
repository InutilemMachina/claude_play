---
title: Project Status -- Playground PDCA log
type: log
status: active
version: 2.0
updated: 2026-05-23
description: Playground (claude_play) PDCA log. Session elején Claude olvassa be. NEM tantárgy-specifikus.
---

# Project Status -- Playground PDCA Log

_Frissítve: 2026-05-23_

# 1. Plan (következő lépések)

| # | Feladat | Felelős | Megjegyzés |
|:--|:--------|:--------|:-----------|
| A | **00_references_collector PoC** -- Matrix Profile, 3-5 forrás Deep Research + letöltés | 🤖 | Skill kész, futtatás hiányzik |
| B | **NLM Prompt B automatizálás** vizsgálata -- CLI parancs vagy Chrome-vezérlés | 🤖 | Új igény |
| C | **NLM metapromptok pedagógiai felülvizsgálata** -- didaktikai hangnem, képek | 🤖+👤 | nlm_prompts.md átírás |
| D | **du_template.pptx** megszerkesztése | 👤 | Hiányzik, bypass él; templates/-ben van placeholder |
| E | **PDF-ek feltöltése** (MP I, II) + MinerU futtatása | 👤 | Hiányzik, kepek_workflow.md §8 |
| F | **DFT teszt pipeline futtatása** | 🤖+👤 | sources: tests/dft/forrasok/ |
| G | **context_sablon.md lépésszámok frissítése** | 🤖 | C00-C08 oszlopok elavultak |

# 2. Do (elvégzett munkák)

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

Az alábbi tanulságok az MP 1. hét end-to-end tesztből (2026-05-22) származnak.
Minden pitfall → [pitfalls.md](pitfalls.md)-be ment; skill javítások → az érintett skill fájlba.

| Komponens | Eredmény | Tanulság |
|:----------|:---------|:---------|
| NLM CLI + Prompt B | ✅ PASS | Strukturált citáció, LaTeX képletek, táblázatok jól működnek |
| 05_mindmap_manager | ✅ PASS | Export-Tool MD → Mermaid konverzió megbízható |
| 06_notes_collector | ✅ PASS | Anchor-link ékezetes magyar szövegre is helyes |
| 03_excerpt_block_maker | ✅ PASS | whitespace szabály (\\n\\n>) beépítve |
| 07_typesetter Rule D | ⚠️ 21 javítás | 03 whitespace fix után várhatóan csökken |
| 09_question_bank_collector | ✅ PASS | NLM BSc/MSc differenciált kérdések |
| 10_bsc_filter | ✅ PASS | Hármas szűrés (MSc blokk + Mermaid node + SZINT) rögtön jól működött |
| Citation globális sorszámozás | ❌ | NLM query-nként [1]-től számoz → UUID-dedup szükséges (B opció, 04 skillben) |
| 01_html_to_md | ⚠️ archív | NLM CLI direkten lekérdez, HTML export nem szükséges |
| NLM Q2 ékezet | ⚠️ | ASCII query workaround működött; nlm_integration.md §2.2 |
| pptx_gyarto.py LaTeX | ❌ | python-pptx nem tud LaTeX-et -- elfogadott korlát |
| Képek | ❌ | PDF-ek hiányoztak → placeholder rendszer (kepek_workflow.md) |

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-22 | 1.0 | Létrehozva: Do szekciók, következő lépések |
| 2026-05-23 | 2.0 | PDCA struktúra: Plan/Do/Check/Act; tanulságok táblázatba rendezve; pipeline_next_steps.md beolvasztva |
| 2026-05-23 | 2.1 | §4 Act + §5 Arch törölve (git history + CLAUDE.md/pipeline.md lefedi) |
