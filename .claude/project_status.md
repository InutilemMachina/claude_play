---
title: Project Status -- Playground állapot + Backlog
type: log
status: active
version: 4.0
updated: 2026-05-29
description: Playground (claude_play) állapot és aggregált backlog. Session elején Claude olvassa be. NEM tantárgy-specifikus. A részletes történeti napló a git history-ban.
---

# Project Status

Ez a fájl az **élő állapot + aggregált backlog** (Instructions §11.1). A lezárt
tételek a Változásjegyzékbe / git history-ba kerülnek, nem itt halmozódnak.

## Aktuális állapot

- **Branch:** `meta_file_updates` (a session összes eredménye itt; `main` érintetlen, user-döntésre vár a merge).
- **Pipeline:** 01-14 + 03-1/03-2/05/06/11b lépések definiálva; a mini teszt (`test_outputs/mini/1_het`) Q1-Q13-on end-to-end fut.
- **Utolsó nagy munka:** meta bázis audit + rendrakás (M1-M6); 4 offline munkacsomag (06 excerpt, 11b check, forrás-extraktor, camera-ready Pandoc).

---

# 1. Backlog (nyitott feladatok)

Forrás: az egyes fájlok `## Nyitott pontok` / skill `§8` szekciói. Ez az aggregált prioritási sor.

## P1 — pipeline-tartalom (kvóta/API függő)
| # | Feladat | Hol | Státusz |
|---|---------|-----|---------|
| B-01 | Q14-Q23 DFS `--resume` (NLM kvóta reset után) | 04 skill | 🔲 kvótára vár |
| B-02 | F6: Szószedet NLM-alapra (Prompt C.2 / D már kész → tesztelni) | 07 skill | ⚙️ prompt kész |
| B-03 | F8: PPTX architektúra döntés (XML-mapping vs Pandoc vs Marp+Chrome) | 12 skill | ❔ döntés kell |
| B-04 | Rule J terminológia-szótár tantárgy-specifikus bővítése | 11_typesetter | 🔲 |

## P2 — meta bázis (folyamatban lévő audit hátraléka)
| # | Feladat | Hol | Státusz |
|---|---------|-----|---------|
| B-05 | M5: templates egyesítés → `course_development_template.md` | templates/ | ✅ 2026-05-29 |
| B-06 | M6: `15_backlog_index.py` aggregátor | scripts/ | ✅ 2026-05-29 |
| B-07 | Relatív linkek: elv (Instructions §8) + belépő fájlok kész; skillek auditja hátra | meta-fájlok | ⚙️ részben |
| B-08 | YAML `tags` scope-séma: definíció (Instructions §5.3) kész; meglévő fájlok átállítása hátra | minden `.md` | ⚙️ részben |
| B-15 | `00_init_course.py`: tantárgy-struktúra + context.md auto-copy a sablonból | scripts/ | ✅ 2026-05-29 |

## P1b — mini2 audit kritikusok (2026-05-30)
| # | Feladat | Hol | Státusz |
|---|---------|-----|---------|
| B-16 | `citations.json` nem generálódik a 04 DFS-ben → 07 üres inputot kap | 04 skill §8 / 04_nlm_dfs_queries.py | 🔲 |
| B-17 | DOCX export: `cwd` hiány → relatív képútvonalak nem oldódnak fel | 14_util_pandoc_export.py | ✅ javítva 2026-05-30 |
| B-18 | PDF emoji regex görög betűket törölhetett | 14_util_pandoc_export.py | ✅ javítva 2026-05-30 |
| B-19 | `[MSc]` marker nincs propagálva a szövegbe az assembler-től | 05_assemble.py | 🔲 |
| B-20 | Képsorszámozás nem globális (`10_notes_collector.py`) | 10_notes_collector.py | 🔲 |
| B-21 | Typesetter Rule K hiányzik: numerikus intervallum cleanup | 11_typesetter.py | 🔲 |
| B-22 | `05_assemble.py` üres "Bevezetes" fejléc root-query elé kerül | 05_assemble.py | 🔲 |
| B-23 | WIP prezentáció (`4_wip_outputs/N_Prezentacio.md`) nem keletkezik | 12 skill | 🔲 |
| B-24 | `06b` script neve `06_table_caption_injector.py` + direkt arg API | pipeline.md §1, 06b skill | ⚙️ doc javítva |
| B-25 | YAML `tags` hiányzik CLAUDE.md és Instructions.md fejlécéből | CLAUDE.md, Instructions.md | 🔲 |

## P3 — végtermék-minőség (alacsonyabb prioritás)
| # | Feladat | Hol | Státusz |
|---|---------|-----|---------|
| B-09 | F15: táblázat-felirat `(automatikus felirat)` placeholder valódi tartalomra | 06b skill | 🔲 |
| B-10 | Mindmap camera-ready (renderelt kép/PDF az 5_clean_outputs-ba) | 12/14 skill | ❔ felelős? |
| B-11 | 12 PPTX: TOC-dia + speaker notes (💡 blokkokból) | 12 skill | 🔲 (F8 alá) |
| B-12 | `pip install python-docx` → DOCX forrás-extraktor élesítése | env | 🔲 |
| B-13 | SingleFile CLI: képes HTML-archiválás (process-isolation korlát) | 03 skill | 🔲 alacsony |
| B-14 | `main` merge döntés (mikor olvad a meta_file_updates a main-be) | git | 😎 döntés |

---

# 2. Tanulságok (tartós elvek)

A korábbi tesztfutások (MP, Fourier, Termografia, DFT, mini) kondenzált tanulságai.
Részletek a skillek `§8`-ban és a git history-ban.

- **Automata elvárás (alapelv):** heurisztikák (pl. page_idx-közelítés) TILOSAK; minden lépés legyen determinisztikus és scriptelhető. (Instructions §2)
- **NLM kvóta:** Google-fiók szintű (nem per-notebook), ~50 query/nap, reset kb. éjfél PT. Védekezés: `--resume --sleep 5`, RESOURCE_EXHAUSTED-detektálás (04 skill).
- **Kép-keywords ingyenes út (Vision API helyett):** NLM Qfig CLI / Prompt C.3 Studio / `03_util_figure_catalog.py --from-caption` — mind API-mentes. (09 skill §6)
- **Camera-ready scope:** minden végtermék `5_clean_outputs/`-ba, BSc-szűrt verzió `_bsc` suffixszel. Jegyzet → `.docx` (Pandoc); prezentáció → `.pptx` (python-pptx).
- **MSc/BSc határ:** emberi döntés (`[MSc]` jelölés a mindmapen); a pipeline csak szűr (14_bsc_filter).
- **NLM mindmap = sarokkő:** a Studio-export adja a query-struktúrát (04), a BSc/MSc-határt (13-14), a pedagógiai szerkezetet (05-06). Vision-bypass létezik, ha az Ultra Explorer nem elérhető (08 §8).
- **Prompt B = `##` kötelező első sor + próza + ismétlés-tilalom:** e nélkül a DFS-kimenet flat/redundáns (RC-1/RC-2 tanulság, mini teszt).
- **Mappastruktúra-váltás pipeline KÖZBEN tilos** — minden érintett scriptet egyszerre kell frissíteni.
- **Prompt B mini-verzió: `VALASZOLJ KIZAROLAG MAGYARUL` az első sor** — PS 5.1 multiline bypass esetén kötelező, különben az NLM angolul válaszol.
- **`conda run --no-capture-output` + `chcp 65001`** — MinerU terminál visszajelzéshez kötelező; a `cd` Bash tool-ban megváltoztatja a working directory-t (veszélyes: mindig abszolút útvonallal dolgozz).
- **Vision bypass = LLM-hallucináció kockázat** — mindmap PNG-ből rekonstruált export megbízhatatlan; Ultra Explorer `.md` az egyetlen megbízható forrás.
- **Weblapok mentéséhez SingleFile > PDF-print > egyszerű HTML** — képek nélküli mentéssel a Qfig 0 ábra-katalógus-bejegyzést generál, és a figure_mapper üres marad.

---

# 3. Napló (legutóbbi sessionök)

Csak a legutóbbi munkamenetek tömör összefoglalója. A teljes történet: `git log`.

## 2026-05-30 — mini2 end-to-end teszt + audit (meta_file_updates)
- **mini2 pipeline végigfutott** 01-12-ig (13-14 nincs futtatva): 4 forrás (2 PDF, 2 HTML + 1 URL), 19 DFS query, 5 ábra, szószedet, DOCX+PDF camera-ready output.
- **Script bugok javítva:** `03-1_qfig_parser` CAPTION/KEYWORDS mezők, `04` TimeoutExpired handler, `14_util_pandoc_export` cwd+emoji-regex, `03_run_mineru_pipeline` log path.
- **Új feature:** `14_util_pandoc_export --pdf` flag (xelatex, emoji-szűréssel).
- **Kvalitatív review:** 13 megjegyzés (3 blokkoló, 6 javítandó) → `4_wip_outputs/1_Review.md`.
- **Meta audit:** 20 találat (4 kritikus ellenőrizve: 2 false alarm, 2 valós → backlog B-16..B-25).

## 2026-05-29 — meta bázis audit + 4 offline csomag (meta_file_updates)
- **Meta audit (M1-M4):** Instructions §11.1 TODO-szabály; CLAUDE.md relatív linkek; 2 self-attention napló → archive; pipeline.md §5/§7 tisztítás. (M5-M6 backlogban.)
- **Mini teszt iteráció 2:** J1-J5 (Prompt B `##`+próza, `--max-level 2`, Q1 bevezető, Rule J, mindmap cleanup). Bullet 85%→40%, próza 15%→59%.
- **3 kritikus bug:** Rule H HTML-komment rombolás (`<!, Q:N, >`), ToC tripla-duplikáció (idempotencia), Rule J anchor-rombolás — mind javítva + 11b regresszió-teszt.
- **4 offline munkacsomag:** `06_excerpt_block_maker.py` (extractive), `11b_quality_check.py`, `03_util_source_extractor.py` (PPTX/HTML/DOCX), `14_util_pandoc_export.py` (camera-ready DOCX). Studio C.1/C.3/C.4 parser (`03_util_studio_parser.py`). Pandoc 3.9 telepítve.
- **Kép-pipeline élesítve:** 09_figure_mapper blokkoló feltétel lazítva (keywords elég, vlm_done nem); 3 kép a mini Jegyzetben.

## 2026-05-26 — DFT DFS session + technical debt sprint
- `04_nlm_dfs_queries.py` DFS traversal; RESOURCE_EXHAUSTED recovery (`--resume`).
- 03-1_qfig_parser BOM+Markdown-bold fix; 14_bsc_filter.py; Prompt D/E.

## 2026-05-22 – 05-25 — korábbi end-to-end tesztek (MP, Fourier, Termografia)
- Pipeline 01-14 többszöri végigfuttatása; a tanulságok a §2-ben és a skillek §8-ban. Részletek: git history.

---

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-29 | 4.0 | M2: teljes újraírás (Backlog/Tanulságok/Napló); 567→~140 sor; duplikált P/R/F prioritás-táblák összevonva B-NN backloggá; régi részletes Do/Check naplók → git history; lezárt F1-F14, R1-R7, P1-P6 tételek kivezetve |
| 2026-05-29 | 3.1 | Iteráció 2 (J1-J5) eredmények |
| 2026-05-29 | 3.0 | Mini teszt post-mortem; P0-P1 státuszok |
| 2026-05-26 | 2.6 | DFT DFS session; RESOURCE_EXHAUSTED |
| 2026-05-23 | 2.0 | PDCA struktúra bevezetése |
| 2026-05-22 | 1.0 | Létrehozva |

<!-- Megjegyzés: a v3.x és korábbi részletes lépésenkénti Do/Check naplók (Fourier_teszt
01-14, Termografia_teszt_v2/v3, branch-állapotok) a git history-ban érhetők el.
Az élő tanulságok a §2-be, a nyitott feladatok a §1 Backlogba konszolidálva. -->
