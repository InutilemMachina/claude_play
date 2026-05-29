---
title: Prompt C -- NLM Data Tables Studio
type: prompt
pipeline_step: 01_references_collector / 09_figure_mapper / 13_question_bank_collector
updated: 2026-05-29
---

# Prompt C — NLM Data Tables Studio (ceruza ikon)

**Hova:** NotebookLM → Studio panel → Data Tables → ceruza ikon → "Customize Data Table" szövegmező

**Mikor:** Minden Data Table generáláskor — az alapértelmezett generálás helyett mindig adjuk meg.

**Elérhetőség:** ✅ minden felhasználónak elérhető (2026 elejétől minden tier-re kirolloutra)

> **Képpipeline fallback (`09_figure_mapper` előkészítése):** Ha a `--vlm` (API kulcs) és a `--qfig` CLI (NLM kvóta) nem elérhető, a Studio Data Tables manuálisan generál ábra-listát keywords-szel. Kimenet → Export-Tool → `3_raw_outputs/nlm_qfig_raw.txt` → `03-1_qfig_parser.py`. Ez az **elsődleges ajánlott fallback** VLM/Qfig nélkül. Részletek: [09_figure_mapper.md §6](../skills/09_figure_mapper.md).

## Export workflow (Studio outputok → projektmappa)

Az NLM Studio által generált tartalmak (Data Tables, Gondolattérkép, Tanulókártyák) a NotebookLM-Export-Tool bővítménnyel exportálhatók:

| Output típus | Exportálható formátum | Eszköz |
|:-------------|:----------------------|:-------|
| Data Tables | CSV, Markdown, Word, PDF | Export-Tool |
| Gondolattérkép | PNG, SVG, Markdown | Export-Tool |
| Tanulókártyák | CSV, Markdown, Anki | Export-Tool |
| Kvíz | ❌ fejlesztés alatt | -- |
| Csevegési előzmény | Markdown, Word, PDF | Export-Tool |

**Telepítés:** https://github.com/cced3000/NotebookLM-Export-Tool

**Workflow:**
1. Studio tab → Data Tables kártya
2. Kattints a **ceruza ikonra** (ne a sima "Generate"-re!)
3. Másold be az alábbi promptot, szükség szerint adaptálva
4. Generate → Export-Tool gomb → Markdown/CSV letöltés → `3_raw_outputs/`

**Mentési lehetőségek (MCP nélkül):**
1. **Export-Tool bővítmény** (https://github.com/cced3000/NotebookLM-Export-Tool) — automatikus letöltés
2. **Kézi másolás** — a Studio chat-ablakban megjelenő táblázat szövegét közvetlenül be lehet másolni `3_raw_outputs/`-ba

Az MCP automatizálás ismeretlen okokból angol kimenetet ad — ez a mindmapre és a Data Tables generálásra egyaránt vonatkozik. A **generálás** tehát emberi lépés, de a **mentés** mindig elvégezhető manuálisan, Export-Tool nélkül is.

---

## C.1 — Forrásáttekintő táblázat (általános, pipeline-hoz)

**Mikor:** Minden új notebook indulásakor — a feltöltött forrásokat térképezi fel.  
**Pipeline lépés:** 01_references_collector

```
Készíts strukturált forrásáttekintő táblázatot a feltöltött dokumentumokból.

Oszlopok:
1. Forrás neve (fájlnév, kiterjesztéssel — pontosan ahogy a Sources panelen látható)
2. Szerzők és év (pl. "Kovács J., 2019")
3. Forrástípus (könyv / folyóiratcikk / konferenciacikk / előadásanyag / webes forrás / kézirat)
4. Fő témakör (1-2 mondatos összefoglalás)
5. BSc szintű kulcsfogalmak (max. 5, vesszővel)
6. MSc szintű kiegészítés (mi az, ami BSc-n felül kerül elő — max. 3 pont)
7. Kulcsadatok és tipikus paraméterek (mért értékek, tartományok, képletek, ha van)
8. Pipeline felhasználhatóság (Kivonat / Prezentáció / Kérdésbank / Mindhárom)
```

---

## C.2 — Fogalomtérkép táblázat (terminológia-audithoz)

**Mikor:** Adott heti téma kulcsfogalmainak kétnyelvű összegyűjtésére.  
**Pipeline lépés:** 07_citations_maker (szószedet-alapként)

```
Készíts kétnyelvű terminológiai táblázatot a feltöltött forrásokból az adott témakörre.

Oszlopok:
1. Magyar terminus
2. Angol terminus
3. Definíció (max. 1 mondat, forrás alapján)
4. Kontextus / alkalmazási terület
5. Kapcsolódó fogalmak
6. Forrás neve (fájlnév kiterjesztéssel)
7. Szint (BSc / MSc / mindkettő)

Csak olyan fogalmakat vegyél fel, amelyek legalább egy feltöltött forrásban explicit megjelennek.
```

---

## C.3 — Ábrajegyzék kulcsszavakkal (képpipeline fallback)

**Mikor:** Ha `--vlm` (API kulcs) és `--qfig` CLI (NLM kvóta) nem elérhető.  
**Pipeline lépés:** 09_figure_mapper előkészítése  
**Kimenet:** Export-Tool → Markdown → `3_raw_outputs/nlm_qfig_raw.txt` → `03-1_qfig_parser.py`

```
Sorold fel az összes ábrát, diagramot, táblázatot és grafikont a forrásokban.
Minden elemhez add meg:
1. Forrás neve (fájlnév kiterjesztéssel, pontosan ahogy a Sources panelen látható)
2. Ábra száma (ha van, pl. "Figure 3")
3. Caption szövege (ha van, szó szerint)
4. 3-5 angol kulcsszó vesszővel elválasztva, amelyek leírják a vizuális tartalmat

Formátum minden elemhez:
FORRAS: <fajlnev.pdf>
SZAM: <abra szama vagy 'nincs'>
CAPTION: <caption szovege vagy 'nincs'>
KEYWORDS: <kulcsszavak>
---
```

---

## C.4 — Kérdésbank-alap táblázat (13_question_bank_collector előkészítője)

**Mikor:** 13_question_bank_collector lépés előtt — nyers kérdésanyag generálása.  
**Különbség a Studio Kvíztől:** Strukturált nyers adat → Claude BSc/MSc szűrése, nem kész fogyasztói formátum.

```
Készíts vizsgakérdés-alap táblázatot 20-30 kérdéssel a feltöltött forrásokból.

Oszlopok:
1. Téma / fejezet
2. Kulcsállítás vagy tény (tesztelendő tudáselem)
3. Helyes válasz (rövid, 1-2 mondat)
4. Nehézségi szint (1=alapfogalom, 2=alkalmazás, 3=elemzés, 4=értékelés, 5=szintézis)
5. Szint (BSc / MSc)
6. Forrás neve (fájlnév kiterjesztéssel)

Minden sorhoz legyen megadva a forrás.
```

## Változásjegyzék

| Dátum | Leírás |
|-------|--------|
| 2026-05-29 | Kiemelve `nlm_prompts.md`-ből; C.3 ábrajegyzék fallback hozzáadva; C.4 kérdésbank |
| 2026-05-21 | Létrehozva (Prompt C §3.1–3.3) |
