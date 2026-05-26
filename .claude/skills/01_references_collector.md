---
name: 01_references_collector
title: 01_REFERENCES_COLLECTOR — References Collector
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-05-22
description: Forrásgyűjtés Deep Research-sel. Naming convention alkalmazása, open-access PDF letöltés kísérlet, citations.json alapozása, NLM feltöltési útmutató. Pipeline 00. lépése.
---

# 01_REFERENCES_COLLECTOR.MD — References Collector
_00. lépés -- Pipeline belépési pontja_

# 1. Célja és helye a pipeline-ban

Az NLM forráskezelése instabil, ha a forrásokat manuálisan töltik fel: az UUID-ek
ismeretlenek maradnak, a naming nem egységes, és a citáció-renumber nem tud
visszakeresni. Ez a lépés orvosolja a problémát azzal, hogy **Claude gyűjti össze
a forrásokat** a tantárgy témakörének megfelelően.

```
00_references_collector  →  [forrasok/ feltöltve, citations_seed.json kész]
  → 01_nlm_query_runner  →  ...
```

**Előfeltétel:** Nincs. Ez az első lépés.
**Output:** `N_het/forrasok/` feltöltött PDF-ek + `citations_seed.json`.

# 2. Naming convention

## 2.1. Alap séma

```
<szerzo><ev>_<tipus>.<ext>
```

| Mező | Szabály | Példa |
|:-----|:--------|:------|
| `<szerzo>` | Első szerző vezetékneve, kisbetű, ékezet nélkül | `yeh`, `oppenheim` |
| `<ev>` | Megjelenési év (4 jegy) | `2016`, `1999` |
| `_<tipus>` | Lásd típustáblázat alább | `_paper`, `_book` |
| `.<ext>` | `pdf`, `html`, `epub` -- lehetőleg `pdf` | `.pdf` |

## 2.2. Típuskódok

| Kód | Mit jelent |
|:----|:-----------|
| `paper` | Folyóirat- vagy konferenciacikk |
| `book` | Teljes könyv |
| `chapter` | Könyvfejezet |
| `slides` | Előadásdiasor (PDF) |
| `webpage` | Weboldal (HTML mentés vagy URL) |
| `report` | Technikai jelentés, white paper |
| `thesis` | Disszertáció, szakdolgozat |
| `NA` | Hiányzó adat (pl. szerző ismeretlen) |

## 2.3. Egyedi esetek

| Eset | Megoldás | Példa |
|:-----|:---------|:------|
| Azonos szerző + év, két forrás | `a`/`b`/`c` suffix az év után | `yeh2016a_paper.pdf` |
| Ismeretlen szerző | `NA` a szerző helyén | `NA2020_webpage.pdf` |
| Ismeretlen év | `NA` az év helyén | `smith_NA_book.pdf` |
| Több szerző | Csak az első szerző | `mueen2015_paper.pdf` |
| Intézményi szerző | Rövidítés | `ucr2024_webpage.html` |

## 2.4. Példák

```
yeh2016_paper.pdf          Matrix Profile I (Yeh et al., 2016)
zhu2016a_paper.pdf         Matrix Profile II (Zhu et al., 2016a)
zhu2016b_slides.pdf        MP II előadásdiák
mathworks2024_webpage.html MATLAB matrixProfile dokumentáció
mueen2015_paper.pdf        MASS algoritmus (Mueen, 2015)
ucr2024_webpage.html       UCR Matrix Profile Page
```

# 3. Workflow

## 3.1. Téma és hét meghatározása

Claude megkapja:
- `tantargy`: pl. `matrixprofil_teszt`
- `het`: pl. `1`
- `tema`: pl. `Mátrix Profil -- Elmélet és Alkalmazások`
- (opcionális) `meglevo_forrasok`: már feltöltött fájlok listája

QUESTION: nem tudom, hogy ez itt miért releváns. Az adott hét raw_sources mappáját töltjük fel közösen fájlokkal. 

## 3.2. Deep Research keresés

Claude WebSearch-szel felkutatja a releváns forrásokat. Keresési stratégia:

1. **Kulcscikkek:** a téma leggyakrabban hivatkozott alapcikkei (Google Scholar, Semantic Scholar, arXiv).
2. **Oktatási anyagok:** lecture notes, tutorial, review cikk -- didaktikailag hasznosabb.
3. **Hazai/intézményi forrás:** ha van, preferált.

Minden talált forráshoz rögzíti:
```json
{
  "file": "yeh2016_paper.pdf",
  "title": "Matrix Profile I...",
  "authors": ["Yeh, C-C. M.", "Zhu, Y.", "..."],
  "year": "2016",
  "venue": "IEEE ICDM 2016",
  "doi": "10.1109/ICDM.2016.0069",
  "url_open": "https://arxiv.org/abs/...",
  "url_closed": "https://ieeexplore.ieee.org/...",
  "access": "open",
  "type": "paper",
  "relevance": "Alap -- az MP eredeti definíciója és STAMP algoritmus",
  "didactic_value": "magas -- sok ábra, példa"
}
```

## 3.3. Open-access letöltés

Ha `access == "open"`:
- `WebFetch` az arXiv / PMC / nyílt repó URL-re
- Mentés: `N_het/forrasok/<naming>.pdf`
- Ha a letöltés sikertelen (closed access, JS-rendered): jelzés a listában

Ha `access == "closed"`:
- Nem tölt le (jogi/etikai korlát)
- Listázza a DOI-t és a letöltési URL-t --> 👤 manuálisan tölti le

## 3.4. citations_seed.json generálása

A letöltött (és manuálisan feltöltendő) forrásokból generálja a
`forrasok/citations_seed.json`-t -- ezt a `04_citations_maker` mint alapot
használja, az NLM UUID-ek nélkül (azok csak az NLM lekérdezés után tölthetők):

```json
{
  "1": {
    "title": "Matrix Profile I...",
    "authors": "Yeh, C-C. M. et al.",
    "year": "2016",
    "venue": "IEEE ICDM 2016",
    "doi": "10.1109/ICDM.2016.0069",
    "file": "yeh2016_paper.pdf",
    "url": "https://arxiv.org/abs/...",
    "nlm_uuid": null,
    "type": "paper",
    "note": "Alap -- STAMP algoritmus, MASS szubrutin"
  }
}
```

`nlm_uuid` null marad -- a `01_nlm_query_runner` / `04_citations_maker` tölti ki.

## 3.5. NLM feltöltési útmutató

Claude listát készít a letöltött / feltöltendő fájlokról:

```
✅ Letöltve (open access):
  - yeh2016_paper.pdf   (arXiv:1602.01187)
  - zhu2016a_slides.pdf (cs.ucr.edu közvetlen link)

👤 Manuálisan töltsd le és töltsd fel az NLM-be:
  - zhu2016b_paper.pdf  DOI: 10.1109/ICDM.2016.0096
                        URL: https://ieeexplore.ieee.org/...

NLM notebook feltöltési sorrend (preferált):
  1. yeh2016_paper.pdf
  2. zhu2016a_slides.pdf
  3. [manuálisak]
```

Aztán 👤 feltölti az NLM notebookba, majd a `nlm_uuid`-eket a `04_citations_maker`
visszatölti a JSON-ba a Prompt B kimenetéből.

TODO A user nem tud nlm_uuid-kat és JSON-t szerkeszteni. Amikor minden forrás rendelkezésre áll, akkor azokat egyben feltöltjük

# 4. Takarékossági szabály

**PoC teszteknél:** Max. 3-5 forrás kereső és letöltése. Nem kell teljes irodalomjegyzék.
A cél az, hogy az NLM-nek legyen legalább 2-3 jó minőségű, didaktikailag értékes forrása.

# 5. Kapcsolódó fájlok és lépések

| Fájl | Keletkezik | Felhasználja |
|:-----|:-----------|:-------------|
| `forrasok/<naming>.pdf` | 00 | 01, NLM |
| `forrasok/citations_seed.json` | 00 | 04_citations_maker |
| `forrasok/citations.json` | 04 (seed alapján) | 04, 06 |
| `forrasok/nlm_q*_raw.txt` | 01 | 04 |


# Ismert hibák

Nincs ismert, skill-specifikus pitfall. Általános: [pitfalls.md](../pitfalls.md)

# NOTE-ok (tesztelés visszajelzések)

- NOTE 💬 **01-02 lépés szoros függősége -- seed skip:** Ha a user saját forrásokat hoz (01. lépés kihagyódik), a `citations_seed.json` nem jö