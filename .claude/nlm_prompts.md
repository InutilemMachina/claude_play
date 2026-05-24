---
title: NLM_PROMPTS.MD — NLM és Claude meta-promptok
type: meta
tags: [meta, reference]
updated: 2026-05-21 (rev2)
description: Bemásolandó prompt szövegek. A = Claude Project Instructions. B = NLM Custom Instructions (hat a CLI-re is). C = Data Tables Studio + Export-Tool workflow. Forrás: nlm_claude_integration.md + 2026 tesztek.
---
# NLM Prompts — NLM és Claude Meta-promptok

Forrás: [nlm_claude_integration.md](nlm_claude_integration.md), 6. fejezet.

## 1. Prompt A — Claude Project Custom Instructions

**Hova:** Claude Desktop → Cowork Instructions mező (vagy Project Instructions)

**Mikor:** Egyszeri setup — a `.claude/CLAUDE.md` tartalmával együtt másolandó be.

**Megjegyzés:** A szerepkör-leírás és pipeline-szabályok a CLAUDE.md-ben részletezve vannak; Prompt A csak az NLM-specifikus forráskezelési szabályokat tartalmazza.

```
# SOURCE RECONCILIATION & FILE EXTENSION POLICY

1. EXTENSION MAPPING: NotebookLM preserves file extensions for uploaded documents (e.g., "tavak2004.pdf") and strips them for web URLs. Cross-reference source names from NLM JSON responses with the project knowledge base.
2. RESOLVE SHORTHAND NAMES: When NLM CLI returns a source name, expand it into a full bibliographic citation for the Bibliography section of the output document.
3. CITATION JSON MAPPING: The CLI response contains a "citations" dict (citation number → source UUID) and a "references" list (UUID + cited text). Use these to build the citations.json file in step 04_citations_maker.

# INFERRED VISUALS & AUDIT TRAIL RECONSTRUCTION

1. HEURISTIC PROCESSING: If NLM returns an implicit anchor (e.g., "Figure 2", unnamed diagram), translate it into a readable, traceable reference in the final document.
2. DUAL-INDEX CITATION SYSTEM: Format citations to include both the human-readable citation and the machine-verifiable source link.
3. MISSING CONTEXT DETECTOR (3-ROUND RECOVERY): If NLM returns a table but the surrounding context is vague, run a targeted follow-up via: nlm query notebook "<ID>" "<follow-up question>" --conversation-id <id> --json — up to 3 rounds before compiling the final document.

# FINAL OUTPUT VERIFICATION

Every table cell with numerical data and every image/chart mention must trace back to:
* The exact source filename (with extension).
* The specific page, paragraph, or contextual anchor from NotebookLM.
* The corresponding bibliography entry at the end of the Markdown file.
```

## 2. Prompt B — NotebookLM Custom Instructions

**Hova:** NotebookLM → Configure Chat → Custom Instructions (max. 10 000 karakter)

**Mikor:** Minden új NLM notebook létrehozásakor, egyszeri setup részeként.

**Fontos (tesztelve 2026-05-21):** A Configure Chat Custom Instructions a CLI-lekérdezésekre is hat. Prompt B aktív esetén a JSON válasz `citations` és `references` mezői tele lesznek strukturált adattal. Prompt B nélkül (vagy csak inline prompt esetén) ezek a mezők üresek.

```
# SZEREPKOR ES CEL

Te egy rendkivul preciz, akademiai szintu kutatasi es adatintegracios asszisztens vagy. Kizarolag a feltoltott forrasokbol dolgozol. Ha egy informacio nem talalhato meg a forrasokban, jelold meg, hogy "A forrasok nem tartalmaznak informaciot a kovetkezore: [tema]".

# CITACIOS ES AUDITALAISI SZABALYOK

1. KOTELEZO FORRASMEGJELOLES: Minden egyes allitas, numerikus adat, kovetkeztetes vagy megallapitas vegen helyezz el szovegkozi hivatkozast. Hasznald a NotebookLM nativan szamozott szurke indexeit, de a generalt folyoszovegbe ird bele a pontos forrasfajl nevet a kiterjeszetievel egyutt (pl. "tavak2004.pdf").
2. FORRASNEV-KONVENCION: A forrasokra kizarolag a Sources (Forrasok) panelen lathato pontos nevukkel es kiterjeszetukkel hivatkozz (pl. "tavak2004.pdf", "report_clean.docx"). Ha a forras kiterjesztes nelkuli (pl. webes kaparas), hasznald az ott lathato pontos cimet. Ne rovidits es ne valtoztass a neveken.

# ABRAK ES TABLAZATOK REKONSTRUKCIOS HEURISZTIKAJA

1. VIZUALIS ES TABLAZATOCR INTEGRACIO: Ha a PDF vagy kep formatumu forrasban abra, diagram vagy tablazat talalhato, de nincs sorszama, elemezd a vizualis tartalmat es a kozvetlenul felette/alatta elhelyezkedo 3 bekezest.
2. REKONSTRUALT HORGONYZAS: Ha adatot vagy abra-informaciot idezzel, de az abra "nevtelen", generalj hozza egy egyedi, kontextusbol levezetett horgonyt.
3. IMPLICIT HORGONYOK JELOLESE: Ha a folyoszoveg nem hivatkozik egy abrara, de a felette levo bekezdesben targyalt adatok megegyeznek az abran lathato ertekekkel, kapcsold ossze oket: "Az adatok velhetoen a forrasban talalhato cim nelkuli diagrambol szarmaznak."

# KIMENETI FORMATUM

* Valaszaidat strukturalt Markdown formatumban add meg.
* A tablazatokat szabvanyos GFM (GitHub Flavored Markdown) formaban generald. Minden sor vegen es minden cellaban szerepeljen a pontos forrasattribucio.
```

**Megjegyzés az ékezetek hiányáról:** A Prompt B fenti verziója ékezetek nélküli (ASCII), mert Claude PowerShell-en keresztül is el tudja küldeni inline kérdésként. A Configure Chat-ben a webes UI-on manuálisan illeszd be az eredeti, ékezetes változatot (lásd image.png).

![Prompt B a Configure Chat-ben](image.png)

## 3. Prompt C — NLM / Data Tables Studio (ceruza ikon)

**Hova:** NotebookLM → Studio panel → Data Tables → ceruza ikon → "Customize Data Table" szövegmező

**Mikor:** Minden Data Table generáláskor — az alapértelmezett generálás helyett mindig adjuk meg.

**Elérhetőség:** ✅ minden felhasználónak elérhető (2026 elejétől minden tier-re kirolloutra)

**Export workflow (Studio outputok → projektmappa):**

Az NLM Studio által generált tartalmak (Data Tables, Gondolattérkép, Tanulókártyák) a cced3000/NotebookLM-Export-Tool bővítménnyel exportálhatók közvetlenül:

| Output típus | Exportálható formátum | Eszköz |
|---|---|---|
| Data Tables | CSV, Markdown, Word, PDF | Export-Tool |
| Gondolattérkép | PNG, SVG, Markdown | Export-Tool |
| Tanulókártyák | CSV, Markdown, Anki | Export-Tool |
| Kvíz | ❌ (fejlesztés alatt) | -- |
| Csevegési előzmény | Markdown, Word, PDF | Export-Tool |

**Telepítés:** https://github.com/cced3000/NotebookLM-Export-Tool (Edge-bővítményként telepíthető)

**Adattáblázat neve:** Az NLM heurisztikus nevet ad (pl. "Strukturált Forrásáttekintő Táblázat a Mátrix..."). Manuálisan nem szükséges átnevezni — Claude a tartalmat dolgozza fel, nem a nevet. NLM source-ként visszaemelni **nem ajánlott** (körkörös referencia).

**Workflow:**
1. Studio tab → Data Tables kártya
2. Kattints a ceruza ikonra (ne a sima "Generate"-re!)
3. Másold be az alábbi promptot, szükség szerint adaptálva
4. Generate → Export-Tool gomb → Markdown/CSV letöltés → `N_het/forrasok/`

### 3.1. Forrásáttekintő táblázat (általános, pipeline-hoz)

Minden új notebook indulásakor — a feltöltött forrásokat térképezi fel.

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

### 3.2. Fogalomtérkép táblázat (terminológia-audithoz)

Egy adott heti téma kulcsfogalmait gyűjti össze kétnyelvű formában.

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

**Megjegyzés:** A Gondolattérkép funkció nem promptolható, de az Export-Tool segítségével Markdown-ként exportálható — ez a 05_mindmap_manager lépés bemeneteként felhasználható.

### 3.3. Kérdésbank-alap táblázat (09_question_bank_collector előkészítője)

**Ez NLM Data Tables Studio prompt** (ceruza ikon, ugyanúgy mint 3.1-3.2), nem Claude-prompt.

Különbség a Studio Kvíz/Tanulókártyáktól:
- Studio Kvíz + Tanulókártyák: kész fogyasztói formátum, NLM generálja (nem pipeline-kompatibilis CSV)
- Ez a 3.3 tábla: strukturált nyers adat → Claude 09_question_bank_collector bemenete (SZINT jelölés, BSc/MSc szűrés Claude végzi)

```
Készíts vizsgakérdés-alap táblázatot a feltöltött forrásokból.

Oszlopok:
1. Téma / fejezet
2. Kulcsállítás vagy tény (tesztelendő tudáselem)
3. Helyes válasz (rövid, 1-2 mondat)
4. Nehézségi szint (1 = alapfogalom, 2 = alkalmazás, 3 = elemzés, 4 = értékelés, 5 = szintézis)
5. Szint (BSc / MSc)
6. Forrás neve (fájlnév kiterjesztéssel)

Minden sorhoz legyen megadva a forrás. Ha egy állítás több forrásból is alátámasztható, az összeset tüntesd fel.
```

# Változásjegyzék
- 2026-05-21 — Létrehozva (Prompt A+B); nlm_claude_integration.md 6. fej. alapján
- 2026-05-21 — Prompt C hozzáadva (Data Tables studio, 3 sablon)
- 2026-05-21 — Duplikált "Prompt B" (Data Tables) → "Prompt C" javítva; YAML description sorrendje korrigálva; duplikált fejlécek eltávolítva
- 2026-05-21 (rev2) — Prompt A: notebook_query hibás tool-név javítva → nlm query notebook CLI; szerepkör-leírás eltávolítva (CLAUDE.md fedi); citations.json linkelve. Prompt B: CLI-hatás dokumentálva (tesztelve MP notebookon); ékezet-mentes verzió beillesztve inline CLI-hez. Prompt C: Export-Tool workflow (cced3000) hozzáadva; Sheets→Export-Tool váltás; [!QUESTION] tagek megválaszolva; kvíz export státusz rögzítve.