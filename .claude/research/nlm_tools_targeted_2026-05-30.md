---
title: NLM integrációs eszközök célzott kutatása — 2026-05-30
type: research
tags: [research, nlm, mcp, integration]
branch: test-mcp-research
updated: 2026-05-30
description: BibCit, Mindmap Extractor, notebooklm-cowork és kiegészítő eszközök valós állapotfelmérése. Eszköz-mátrix, ajánlások, pipeline-relevanciák.
---

# NLM integrációs eszközök célzott kutatása

**Dátum:** 2026-05-30  
**Branch:** `test-mcp-research`  
**Kontextus:** Out of scope (A2 kutatás) — a-klaszter-3-graceful-sprout.md  
**Háttér:** [nlm-claude_integration_research.md](../archive/nlm-claude_integration_research.md)

---

## 1. Eszköz-mátrix

| Eszköz | Típus | Verzió / Állapot | Stars | Felhasználók | Ár | Telepítés | Kockázat |
|--------|-------|-----------------|-------|-------------|-----|-----------|---------|
| **BibCit (Markdown Capturer)** | Chrome ext. | v2.5, 2026-05-09 | — | 9 000 | Ingyenes | Chrome Web Store | Alacsony |
| **NLM Mindmap Extractor (Corrected Hierarchy)** | Chrome ext. | CWS, aktív | — | n/a | Ingyenes | Chrome Web Store | Alacsony |
| **Ovler-Young Mindmap Extractor** | Chrome ext. | 6 commit, 0★ | 0 | — | Ingyenes | Dev mode (zip) | Közepes |
| **notebooklm-cowork** | Cowork plugin | 6 commit, 7★ | 7 | — | Ingyenes* | Cowork app | Magas |
| **jacob-bd/notebooklm-mcp-cli** | MCP szerver (Python) | v0.6.13, 2026-05-27 | 4 700 | — | Ingyenes | pip/uv | Közepes |
| **PleasePrompto/notebooklm-mcp** | MCP szerver (Node.js) | v2.0.0, 2026-05-01 | 2 600 | — | Ingyenes | npx | Közepes |
| **proyecto26/notebooklm-ai-plugin** | Claude Code plugin | 21 commit, 48★ | 48 | — | Ingyenes | npx/Claude Code | Közepes |

*\*A notebooklm-cowork a Claude Cowork alkalmazást igényli: Pro plan $20/hó + Windows 10 22H2+ Hyper-V (VM-alapú futtatás).*

---

## 2. Részletes értékelés — 3 prioritás

### P1 — BibCit (Markdown Capturer)

**Mit tud valójában:**
- NLM válaszokat exportál Markdownba, Word (.docx) vagy PDF formátumba
- Citációs stílusok: APA, MLA, Harvard, Chicago, Vancouver, **IEEE**, OSCOLA + 10 000+ stílus
- v2.5 óta NotebookLM-kompatibilis: a DOM-ból olvassa a NLM számozott hivatkozásait és IEEE-re (vagy más stílusra) konvertálja
- REST API elérhető (fejlesztői integráció elvben lehetséges)

**Amit a dokumentáció állított vs. valóság:**
- Az eredeti research doc szerint "automatikusan átalakítja" a citációkat IEEE-re → **részben igaz**, de csak manuálisan: a felhasználónak rá kell kattintani az extension gombra az NLM chatben.
- Az extwise.com review szerint az IEEE támogatás **nincs expliciten dokumentálva** a Chrome Web Store leírásban, csak a bibcit.com website-on van felsorolva. Ez ellentmondást jelez — valószínűleg az exportálás működik, de a megbízhatóság kérdéses (4.0/5, 16 értékelés, vegyes visszajelzések, "getting failed frequently").
- **Nem CLI-automatizálható**: nincs parancssori vagy programatikus belépési pont — kizárólag böngészős interakcióhoz kötött.

**Pipeline-relevancia (Klaszter 2 — IEEE refaktor):**
> **⛔ NEM váltja ki az Opció A megközelítést (07-2_ieee_renderer.py).**
>
> A BibCit egy manuális export-eszköz. A pipeline CLI-automatizált, scriptelt — ott a BibCit nem kapcsolható be. Az Opció A (saját renderer) helyes döntés marad.
>
> BibCit hasznos lehet mint **manual verification tool**: az NLM Studio outputjából IEEE-re exportált Markdown összehasonlítható a pipeline által generált hivatkozásokkal — hibakeresési célra.

**Telepítési kockázat:** Alacsony (CWS, nem kell fejlesztői mód).  
**Kipróbálási javaslat:** ✅ Érdemes telepíteni a mini2-es tantárgyon manuális tesztelésre.

---

### P2 — NotebookLM Mindmap Extractor (Corrected Hierarchy)

**Két különböző extension létezik — fontos megkülönböztetni:**

| | **Corrected Hierarchy** (CWS) | **Ovler-Young** (GitHub, dev mode) |
|---|---|---|
| Chrome Web Store | ✅ Igen | ❌ Nem (kézi telepítés) |
| Export formátumok | FreeMind (.mm), OPML, XML | JSON, CSV, Markdown |
| Auto-expand | Nem ismert | ✅ Igen |
| Interaktív viewer | Nincs | ✅ React viewer |
| Stars | — | 0 |
| Megbízhatóság | Valószínűbb (CWS) | Kísérleti |

**Mit tud a Corrected Hierarchy (CWS verzió):**
- NLM mindmap SVG-jéből X-koordináta + összeköttetés elemzéssel rekonstruálja a szülő-gyermek hierarchiát
- FreeMind (.mm) → Claude-ba beolvasható XML; OPML → strukturált outline formátum
- Minden feldolgozás lokálisan fut, nincs adatküldés
- Ingyenes

**Mit tud az Ovler-Young (GitHub):**
- Auto-expand: automatikusan kinyitja az összes csomópontot
- JSON + CSV export (Google Sheets-kompatibilis)
- Interaktív vizuális viewer
- Manifest V3, d3.js + React

**Pipeline-relevancia (A3 — Vision bypass):**
> **⚠️ RÉSZLEGES alternatíva a vision bypass helyett, de nem teljes automatizálás.**
>
> A mindmap extractor MANUÁLIS lépést igényel: Chrome-ot kell megnyitni, az NLM-ben ki kell terjeszteni a mindmapet, majd rákattintani az extensionre. Ez kiváltja a képernyőképezést/vision-t, de nem küszöböli ki az emberi beavatkozást.
>
> **Tényleges előny:** Strukturált .mm vagy OPML fájlt ad, amit a `08_mindmap_manager.py` olvashat — a vision-bypass flow (PNG → Claude API → struktúra) helyett megbízhatóbb, és nem igényel Claude API hívást a hierarchia-kinyeréshez.
>
> **Javaslat:** A 08-as skillben opcionális "mindmap_source: extractor" ágként dokumentálni (nem kötelező, de a vision bypass mellett ajánlott alternatíva).

**Telepítési kockázat:** Alacsony (Corrected Hierarchy CWS-en van).  
**Kipróbálási javaslat:** ✅ A CWS verzió telepíthető, mini2-re tesztelendő.

---

### P3 — notebooklm-cowork (gfsaaser24)

**Valós állapot:**
- **7 stars, 1 fork, 6 commit** — rendkívül kis közösségi alap
- A plugin **nem önálló**: a jacob-bd/notebooklm-mcp-cli MCP szerverre épít (azt wrappeli egy Cowork playbook-ba)
- **Súlyos függőség:** Claude Cowork alkalmazást igényel
  - Pro: $20/hó (vagy $17/hó éves számlázásnál)
  - Windows 10 22H2+ + **Hyper-V virtualizáció** kötelező (a Cowork VM-ben fut)
  - Windows Home editionon NEM fut (Hyper-V Pro/Enterprise/Education kizárólag)
- Limitációk: ~50 lekérdezés/nap (NLM free tier), cookie-k 2-4 hetes megújítása
- Dokumentáció: "undocumented Google internal APIs — not officially supported"

**A kritikus felismerés:**
> **A notebooklm-cowork plugin feleslegessé válik, ha a jacob-bd MCP CLI közvetlenül telepítve van.**
>
> A 39 "eszköz" valójában a jacob-bd MCP CLI ~35 natív tool-ja + a Cowork skill playbook-réteg. Ha a pipeline már Claude Code-dal fut (ami itt az eset), a jacob-bd MCP CLI közvetlenül integrálható — Cowork nélkül, $0 extra költséggel.

**Klaszter 3 (CLI↔UI hibrid) feloldásának valódi útja:**
> ✅ **jacob-bd/notebooklm-mcp-cli közvetlenül**, nem a notebooklm-cowork wrapperén át.

**Telepítési kockázat:** Magas (Cowork Pro, Hyper-V, VM overhead, 7 csillag).  
**Kipróbálási javaslat:** ⛔ Elvethető mint önálló megoldás. A jacob-bd MCP CLI kipróbálása javasolt helyette.

---

## 3. Újonnan feltárt, ígéretes eszközök

### jacob-bd/notebooklm-mcp-cli ⭐⭐⭐ — LEGFONTOSABB

**Miért ez a legígéretesebb:**
- **4 700 stars, 731 fork** — messze a legnépszerűbb NLM integrációs projekt
- **v0.6.13 (2026-05-27)** — 3 napja frissítve, aktív karbantartás
- **Windows-kompatibilis**: explicit Windows támogatás (UTF-8, icacls fixek dokumentálva)
- **35 MCP tool** a Claude Code-hoz: `notebook_query`, `source_add`, `studio_create`, `cross_notebook_query`, `batch`, `pipeline`, stb.
- **Telepítés:** `uv tool install notebooklm-mcp-cli` + `nlm login` (Chrome ablak)
- **Autentikáció:** Chrome/Edge/Brave cookie-k, 2-4 hetes lejárat, automata refresh
- **Rate limit:** ~50 query/nap free tier (multi-profil lehetséges)
- **Ár:** Ingyenes

**Pipeline-relevancia (Klaszter 3):**
> **Ez oldja fel a Klaszter 3-at.** Claude Code + notebooklm-mcp-cli = CLI↔UI hibrid, Cowork nélkül. A 04_nlm_dfs_queries.py-t ki lehetne egészíteni MCP-hívásokkal (jelenleg browser-automatizációt vagy kézi lépéseket igényel).

**Telepítési kockázat:** Közepes (undocumented API, cookie-management, rate limit).

---

### PleasePrompto/notebooklm-mcp ⭐⭐ — Alternatíva

- **2 600 stars, 368 fork**, Node.js alapú
- **v2.0.0 (2026-05-01)** — "multilingual rewrite, async audio, MCP-spec descriptions"
- Telepítés: `npx notebooklm-mcp@latest` vagy `claude mcp add notebooklm -- npx notebooklm-mcp@latest`
- 30+ tool, kicsit kevesebb mint a jacob-bd
- **WSL1 nem támogatott** (WSL2 ajánlott) — Windows-on ez problémás lehet
- Előnye: npm-alapú, könnyebb frissítés

**Javaslat:** jacob-bd az elsődleges jelölt (Python, uv, több star, Windows-kompatibilis). PleasePrompto backup.

---

### proyecto26/notebooklm-ai-plugin ⭐ — Speciális eset

- **48 stars, 12 fork**, TypeScript/Bun
- 9 artifact típus generálása: diák, audio, videó, mindmap, flashcard, kvíz, infografika, jelentés, adattáblázat
- Claude Code plugin + CLI (`npx`)
- **Korlát:** Audio/videó letöltés kézi böngésző-hozzáférést igényel
- **Data Tables** funkció még fejlesztés alatt
- **Relevancia:** Studio artifact generálás automatizálásához hasznos (ez a jacob-bd CLI-ban is megvan `studio_create` toolként)

**Javaslat:** Nem prioritás, jacob-bd lefedi a lényeget.

---

### notebooklm-mcp-2026 (julianoczkowski) — Figyelendő

- PyPI csomag, cross-platform (macOS, Linux, Windows)
- Dokumentáció korlátozott, fiatalabb projekt
- **Relevancia:** Ha a jacob-bd nem működne Windows-on tökéletesen, backup opció

---

## 4. Összesített ajánlás

### Melyikre érdemes építeni

| Prioritás | Eszköz | Miért | Következő lépés |
|-----------|--------|-------|-----------------|
| 🥇 **Elsődleges** | jacob-bd/notebooklm-mcp-cli | 4.7k★, aktív, Windows-kompatibilis, 35 MCP tool, Cowork-mentes | Telepítés: `uv tool install notebooklm-mcp-cli` + `nlm login` Windows-on |
| 🥈 **Másodlagos** | BibCit v2.5 | Ingyenes, CWS, manuális IEEE export teszteléshez | Telepíteni mini2-re, manuális spot-check |
| 🥉 **Opcionális** | NLM Mindmap Extractor (CWS) | A3 bypass strukturált alternatívája | Telepíteni, .mm fájl exportálása mini2 mindmapből |

### Elvethető

| Eszköz | Miért |
|--------|-------|
| notebooklm-cowork | 7★ wrapper, $20/hó Cowork Pro + Hyper-V kötelező; a jacob-bd MCP CLI ezt kiváltja |
| Ovler-Young Mindmap Extractor | 0★, dev mode install, CWS verzió elegendő |
| proyecto26/notebooklm-ai-plugin | jacob-bd lefedi; studio_create az MCP CLI-ban megvan |

### Pipeline-döntések megerősítése

- **Klaszter 2 (IEEE):** Opció A (07-2_ieee_renderer.py saját renderer) helyes marad. BibCit nem CLI-automatizálható.
- **A3 (Vision bypass):** Mindmap Extractor manuális alternatíva, de nem küszöböli ki az emberi lépést. A terv szerinti NOTE megközelítés + opcionális extractor dokumentáció elegendő.
- **Klaszter 3 (CLI↔UI hibrid):** **jacob-bd MCP CLI** feloldja, ha Windows-on telepíthető. Ez a tényleges POC feladat.

---

## 5. POC-terv (mini2 tantárgyon)

### Fázis 1 — jacob-bd MCP CLI telepítés (becsült: 1-2 óra)

```powershell
# 1. uv telepítése (ha még nincs)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. notebooklm-mcp-cli telepítése
uv tool install notebooklm-mcp-cli

# 3. Google bejelentkezés (Chrome ablak)
nlm login

# 4. Notebooks listázása (ellenőrzés)
nlm notebook list

# 5. Claude Code MCP integráció
claude mcp add notebooklm -- uv run notebooklm-mcp
```

### Fázis 2 — mini2 lekérdezés tesztelése

```powershell
# CLI teszt: 1 query a mini2 notebookból
nlm query --notebook "mini2" "Mi a tantárgy fő témái?"

# MCP teszt Claude Code-on keresztül:
# (Claude Code-ban) @notebooklm notebook_query "mini2" "Főbb témák?"
```

### Fázis 3 — BibCit és Mindmap Extractor manuális teszt

1. Chrome-ban megnyitni a mini2 NLM notebookot
2. BibCit gombra kattintani → IEEE export → elmenteni mint `bibcit_test_ieee.md`
3. Studio panel → Mindmap → Corrected Hierarchy extension → OPML export → `mini2_mindmap.opml`
4. Az OPML fájlt a `08_mindmap_manager.py`-val feldolgozni (vision bypass helyett)

### Sikerkritériumok

- [ ] `nlm notebook list` visszaadja a mini2 notebookot
- [ ] `nlm query` működik Windows-on (UTF-8 encoding OK)
- [ ] Claude Code MCP regisztrálva, `notebook_query` tool elérhető
- [ ] BibCit IEEE export: a számozott hivatkozások IEEE-re konvertálva (`[1] Author, Title, Year`)
- [ ] Mindmap Extractor: OPML fájl letöltve, parseable XML struktúrával

---

## 6. Kockázatok és korlátok

| Kockázat | Valószínűség | Hatás | Mitigáció |
|----------|-------------|-------|-----------|
| NLM UI változás → MCP megszakad | Közepes | Magas | April 2026-ban 24-72h alatt javítottak — aktív karbantartás |
| 50 query/nap limit | Magas | Közepes | Multi-profil (`nlm login --profile`); DFS query batching |
| Cookie lejárat 2-4 hét | Magas | Közepes | `nlm login` megújítás, automatizálható CI-ben |
| Windows UTF-8 encoding hiba | Közepes | Alacsony | v0.6.x már fix: explicit UTF-8 megadás |
| BibCit megbízhatóság | Közepes | Alacsony | Csak manuális tesztelésre, nem pipeline-kritikus |

---

## Felhasznált források

- [jacob-bd/notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) — v0.6.13, 2026-05-27
- [PleasePrompto/notebooklm-mcp](https://github.com/PleasePrompto/notebooklm-mcp) — v2.0.0, 2026-05-01
- [gfsaaser24/notebooklm-cowork](https://github.com/gfsaaser24/notebooklm-cowork)
- [proyecto26/notebooklm-ai-plugin](https://github.com/proyecto26/notebooklm-ai-plugin)
- [BibCit Chrome Web Store](https://chromewebstore.google.com/detail/markdown-capturer-bibcit/bbglkcgbhkhchpbbbcgpocnhplhdhnmc)
- [BibCit extwise review](https://extwise.com/extension/markdown-capturer-bibcit/)
- [bibcit.com](https://www.bibcit.com/en)
- [NLM Mindmap Extractor (CWS)](https://chromewebstore.google.com/detail/notebooklm-mindmap-extrac/ecikohbjgbjnlbldbjnceohmbhipipcp)
- [Ovler-Young Mindmap Extractor](https://github.com/Ovler-Young/notebookLM-mindmap-extractor)
- [XDA: Mindmap Extractor review](https://www.xda-developers.com/notebooklm-mindmap-extractor-extension/)
- [Claude Cowork pricing](https://www.sentisight.ai/how-much-cost-claude-cowork/)
- [Claude Cowork Windows](https://claudecowork.im/blog/claude-cowork-windows)
- [NLM MCP Windows guide](https://pasqualepillitteri.it/en/news/1598/connect-claude-code-notebooklm-mcp-zero-tokens-2026)
- [McpServers: jacob-bd](https://mcpservers.org/servers/github-com-jacob-bd-notebooklm-mcp-cli-blob-main-docs-mcpguide-md)
