---
title: Pipeline Next Steps -- End-to-end teszt reflexió és következő teendők
type: meta
tags: [meta, audit, reflexio]
updated: 2026-05-22
description: Az első teljes end-to-end pipeline-teszt (MP 1. hét) tanulságai, javaslatok, és prioritizált következő lépések. Jelöli, hol volt bypass.
---

# Pipeline Next Steps -- End-to-end Teszt Reflexió

_2026-05-22, matrixprofil_teszt/1_het/ alapján_

---

# 1. Önreflexió -- Mi működött, mi nem

## 1.1. Ami jól működött

- **NLM CLI lekérdezés** (Prompt B aktív): strukturált, citációval ellátott válaszok, LaTeX képletekkel, táblázatokkal. A 4 db level-2 query lefedta az anyag egészét.
- **05_mindmap_manager**: az Export-Tool által letöltött MD mindmap → Mermaid `flowchart LR` konverzió egyszerű és megbízható.
- **06_notes_collector**: anchor-link generálás ékezetes magyar szövegnél is helyes.
- **03_excerpt_block_maker**: Python-alapú injektálás robusztus, 13+4 blokk rendesen bekерült.
- **07_typesetter**: a Rule D (blockquote üres sor) a legtöbb javítást igényelte (21 db) -- ez előre jelzi, hogy az NLM válaszok blockquote-ai elé automatikusan kellene üres sort generálni már a Jegyzet-összeállítás fázisában.
- **09_question_bank_collector + NLM**: az NLM kiváló A/B/C/D kérdéseket generált forráspontos helyes válaszokkal, BSc/MSc szintre differenciálva.
- **10_bsc_filter**: a `<!-- MSc -->` blokk + Mermaid `[MSc]` node + SZINT:4-5 hármas szűrés egyből jól működött.

## 1.2. Problémák és tanulságok

| Probléma | Gyökérok | Javaslat |
|:---|:---|:---|
| **Citation globális atsorszámozás** | NLM minden query-nél [1]-től számoz | 04_citations_maker: UUID-alapú dedup + globális sorrend; vagy egyetlen összevont NLM query |
| **01_html_to_md feleslegessé vált** | NLM CLI direkten lekérdez, nincs HTML export szükség | Lépés megszüntetése; CLI query = 01 helyettese |
| **NLM Q2 ékezet-probléma** | CLI ékezetes query-nél csonkított output volt | Workaround: ASCII query (működött); vagy idézőjelbe tenni a kérdést |
| **Rule D sok javítás (21 db)** | 03_excerpt_block_maker nem tesz üres sort blockquote elé | 03 skill javítás: `\n\n>` injektálás helyett `\n> ` mintát fix-elje |
| **pptx_gyarto.py LaTeX nem renderel** | python-pptx nem tud LaTeX-et | Elfogadott korlát -- prezentációs tool (pl. Marp CLI) kezelné; vagy egyszerűsített jelölés |
| **Képek hiánya** | PDF-ek nem álltak rendelkezésre | Placeholder rendszer megtervezve (kepek_workflow.md); MinerU futtatandó ha PDF elérhető |
| **pptx_gyarto.py body szöveg egyszerű** | Marp-ból plain text, MD formázás elvész | Részleges Markdown → PPTX formázás: bullet parse, bold → font.bold |

---

# 2. Javasolt lépés-átszervezések

## 2.1. 01_html_to_md megszüntetése / átalakítása

**Jelenlegi helyzet:** A step azt feltételezi, hogy az NLM Studio HTML exportot adunk át. De a tesztelt workflow-ban NLM CLI direkten generálja a tartalmat.

**Javaslat:** Lépés neve legyen `01_nlm_query_runner`, tartalma:
```
NLM notebook → nlm query (level-2 mindmap témánként) → JSON válaszok forrasok/-ba
```
Az eredeti HTML-import út megmaradhat alternatívként (ha valaki mégis HTML exportot használ).

## 2.2. 04_citations_maker redesign

**Jelenlegi helyzet:** A skill `citations.json`-t épít és `<sup>[n]</sup>` linkeket cserél. De az NLM válaszok query-lokális [1..n] számokat használnak.

**Javaslat -- két opció:**

**A opció (egyszerűbb):** Egyetlen összevont NLM query az egész hét anyagára → egyetlen citáció-namespace. Hátrány: hosszú válasz, token-limit.

**B opció (robusztus):** UUID-alapú dedup a `citations.json`-ban (jelenleg is UUID-ek vannak), + post-processing pass a Jegyzeten: minden inline `[N]`-et cseréljük UUID-alapú globális számra.

**Ajánlás: B opció.** Megvalósítható 04_citations_maker kiegészítéssel.

## 2.3. 03_excerpt_block_maker és 07_typesetter összevonása

A 03 mindig termel Rule D problémákat (blockquote üres sor). Egyszerűbb, ha a 03 a blockquote-okat eleve `\n\n> ` mintával írja -- ekkor a 07-es D szabály 0 javítást végez.

**Javaslat:** 03 skill frissítése, hogy beépített whitespace-t generáljon blockquote elé/mögé.

## 2.4. pptx_gyarto.py fejlesztési roadmap

A script alap-szintű de működő. Prioritizált fejlesztések:
1. Bullet point parse: `- ` → python-pptx `bullet` formázás
2. Táblázat parse: MD táblázat → python-pptx Table shape
3. LaTeX egyszerűsítés: `$formula$` → plain text közelítés (pl. szimbólum-csere map)
4. Template betöltés: ha `du_template.pptx` elérhető, layout-ok átvétele

---

# 3. Prioritizált következő teendők

## 3.1. Azonnali (következő session)

| # | Feladat | Felelős | Bypass volt? |
|:--|:--------|:--------|:-------------|
| 1 | **04_citations_maker skill megírása** (B opció: UUID-dedup + globális atsorszámozás) | 🤖 | Nem (először csináljuk) |
| 2 | **01_nlm_query_runner skill átírása** (HTML import → CLI query adapter) | 🤖 | -- |
| 3 | **03_excerpt_block_maker blockquote whitespace fix** | 🤖 | -- |
| 4 | **du_template.pptx** megszerkesztése és feltöltése | 👤 **HIÁNYZOTT** -- bypass: default python-pptx blank template | -- |
| 5 | **PDF-ek feltöltése** (Matrix Profile I, II) + MinerU futtatása | 👤 **HIÁNYZOTT** -- bypass: kepek_workflow.md placeholder rendszer, képek kihagyva | -- |

## 3.2. Rövid táv (1-2 session)

| # | Feladat | Felelős | Megjegyzés |
|:--|:--------|:--------|:-----------|
| 6 | pptx_gyarto.py bullet + táblázat parse fejlesztése | 🤖 | |
| 7 | NLM ékezetes query stabilizálása (idézőjel wrap vagy ASCII fallback) | 🤖 | |
| 8 | Prompt B beállítása többi notebookban (DFT, Termográfia stb.) | 👤 | |
| 9 | Második tantárgy (pl. DFT) pipeline-tesztje | 🤖+👤 | du_template.pptx után |
| 10 | `nlm mindmap` CLI parancs tesztelése (Export-Tool alternatíva) | 🤖 | |

## 3.3. Középtáv

| # | Feladat | Megjegyzés |
|:--|:--------|:-----------|
| 11 | Cookie megújítás automatizálása (2-4 hetente) | Windows Task Scheduler + `nlm login` |
| 12 | bsc_export.py PPTX generálás (BSc Marp → BSc PPTX) | pptx_gyarto.py integrálása |
| 13 | vizsga/ mappa workflow (összesített kérdésbank, SZINT:2-5) | 09_question_bank_collector kiterjesztése |

---

# 4. Bypass összefoglaló (ahol Te hiányoztál)

| Lépés | Mi hiányzott | Bypass megoldás | Hatás |
|:------|:------------|:----------------|:------|
| 08_presentation_maker | `du_template.pptx` feltöltve | Default python-pptx blank template, kék/fehér akadémiai színséma | PPTX megvan, de nem az intézményi sablon |
| 03_excerpt_block_maker (kép) | PDF-ek (Matrix Profile I, II) nem álltak rendelkezésre, MinerU nem futott | Képek teljesen kihagyva; `kepek_workflow.md` dokumentálja a helyes workflow-t | Képek hiányoznak a Jegyzetből |
| NLM Q2 | Ékezetes query csonkult | ASCII query küldve a CLI-nek | Működött, de törékeny -- stabilizálni kell |

---

# Változásjegyzék
- 2026-05-22 -- Fájl létrehozva az első teljes end-to-end teszt alapján
