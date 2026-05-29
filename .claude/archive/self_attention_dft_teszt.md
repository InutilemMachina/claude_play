---
title: Self-Attention Log
type: log
status: active
version: 1.0
updated: 2026-05-26
description: Párhuzamos megfigyelési napló -- Claude és felhasználó észrevételei automata tesztek során
---

# Self-Attention Log

| # | Időbélyeg | Ki | Megfigyelés |
|:--|:----------|:---|:------------|
| 1 | 2026-05-26 | 🤖 | Fájl létrehozva. Készen állok az automata teszt fogadására. |
| 2 | 2026-05-26 | 🤖 | **01 lépés kész.** `DFT_teszt/1_het/` mappastruktúra OK (1_raw_inputs..5_clean_outputs). 5 forrás másolva: rockmore1999_article.pdf, typinski2014_slides.pdf, ahrens2020_article.pdf, richard2021_slides.pdf, elte2026_webpage.html. `citations_seed.json` generálva (nlm_uuid null -- NLM után töltendő). |
| 3 | 2026-05-26 | 🤖 | **Implicit feltételezés:** `test_sources/dft/` meglévő fájlokat vettem alapul; nem futottam új web-keresést, mert az anyag már adott volt. Ha hiányzó/gyenge forrás van, az 01 skill §3.2 alapján WebSearch futtatandó. |
| 4 | 2026-05-26 | 🤖 | **02 lépés kész (teljesen automatikus).** Notebook ID: 92ecc692. 5 forrás feltöltve. Prompt B aktív (longer mód). Mindmap ID: 9dfdd37e. citations_seed.json UUID-ekkel frissítve. |
| 5 | 2026-05-26 | 🤖 | **Pitfall #új:** `nlm chat configure` -- a `--prompt` argumentumban a belső idézőjelek (`"`) szétbontják a PowerShell argument-parseolást még `@'...'@` heredoc esetén is. Megoldás: belső idézőjeleket eltávolítani a Prompt B szövegéből. Dokumentálni kell pitfalls.md-be. |
| 6 | 2026-05-26 | 🤖 | **Bug #új -- 03_run_mineru_pipeline.py:** Hiányzott a `if __name__ == "__main__": main()` belépési pont. A script csendesen visszatért 0-val anélkül, hogy bármit futtatott volna. Javítva in-place. |
| 7 | 2026-05-26 | 🤖 | **03 lépés -- MinerU háttérben fut** (PowerShell Start-Job #1). Q1-Q4 lekérdezések (04) párhuzamosan indítva, mert azok nem igénylik a 2_clean_inputs tartalmát. |
| 8 | 2026-05-26 | 🤖 | **04 lépés -- HIBÁS MEGKÖZELÍTÉS.** Csak 4 generikus queryt futtattam a mindmap 2. szintjéből. Helyes: DFS az egész mindmapen (27 csomópont: root + 1 level-1 + 5 level-2 + 20 level-3). Javítás: 04_nlm_dfs_queries.py scripttel. |
| 8b | 2026-05-26 | 🤖 | **Architekturális gap azonosítva:** A 04_nlm_query_runner.md §3 Q1-Q4 keretrendszere nem tükrözi a pipeline.md §3 DFS-elvét. A skill frissítendő. |
| 9  | 2026-05-26 | 😎 | Mindmap manuálisan exportálva (Export-Tool). Az első (CLI-workaround) mindmap angolul generálódott; a második manuálisan generált már magyar. Átnevezve: nlm_mindmap_export.md. |
| 10 | 2026-05-26 | 😎 | MinerU vizuális visszajelzés hiányzik háttérben futáskor. Rich progress bar háttérben nem működik; csak szöveges log (mineru_run.log) elérhető. ⚠️ User nem tudott tájékozódni a futás állapotáról. |
| 11 | 2026-05-26 | 😎 | Q1-Q4 célja és szerepköre nem volt kommunikálva -- a user nem tudta, mire valók. Pipeline-szintű dokumentációs gap. |
| 12 | 2026-05-26 | 😎 | A Studio panel bal oldalán a forrásnevek NLM által generáltak (nem az eredeti fájlnév). Nem blokkoló, de zavaró. |
| 13 | 2026-05-26 | 😎 | Az egész mindmapet végig kell kérdezni DFS-sel -- nem csak 4 top-level queryt. Pipeline.md ezt jelzi de a skill és Claude eddig csak 4-et futtatott. |
| 14 | 2026-05-26 | 😎 | Token-korlát miatt minden visszajelzést dokumentálni kell folyamatosan. |
| 15 | 2026-05-26 | 😎 | Nem volt felkérés arra, hogy a mindmap-ben az msc szintű kérdéseket felcímkézzem! Egyébként azt hogy kéne címkézni?|
| 16 | 2026-05-26 | 😎 | a Mindmap-be bekereült egy fura karakter `蝶`, ennek oka ismeretlen |
| 17 | 2026-05-26 | 😎 | a  test_outputs\DFT_teszt\1_het\1_raw_inputs mappa tartalmának mineru feldolgozása félbeszakadt, ahogy a Claude kifogyott a limitekből. |
| 15 | 2026-05-26 | 🤖 | **04 DFS futás részlegesen sikeres.** Q01-Q06 OK (5-7 KB), Q07-Q29 RESOURCE_EXHAUSTED (330 B, napi NLM kvóta kimerítve). Gyökérok: 6 query ~2 perc alatt -> kvóta limit. Megoldás: `--resume --sleep 5` flag hozzáadva; pitfalls §2.8 dokumentálva. Újrafuttatás: holnap. |
| 16 | 2026-05-26 | 🤖 | **04_nlm_dfs_queries.py v1.1:** `--resume` (meglévő >500B fájlok skip), `--sleep` (konfig. szünet), RESOURCE_EXHAUSTED detektálás (nem írja felül a meglévő valid fájlokat hibás válasszal). |
