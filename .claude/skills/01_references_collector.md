---
name: 01_references_collector
title: 01_REFERENCES_COLLECTOR -- References Collector
type: skill
tags: [meta, skill]
status: active
version: 2.0
updated: 2026-05-26
description: Forrásgyűjtés és naming convention alkalmazása. Open-access PDF letöltés, citations_seed.json generálása, NLM feltöltési útmutató. Pipeline 01. lépése.
---

# 01_REFERENCES_COLLECTOR

## 1. Cél

A user által az `1_raw_inputs/` mappába helyezett (és opcionálisan Deep Research-sel kiegészített) forrásokból `citations_seed.json`-t generál, és NLM feltöltési útmutatót ad.

## 2. Bemenetek

- `1_raw_inputs/*.pdf`, `*.html`, `*.docx` -- user által feltöltött források
- (opcionális) téma és hét meghatározása Deep Research-hez

**Előfeltétel:** Nincs. Ez az első lépés.

## 3. Eljárás

### 3.1. Naming convention

```
<szerzo><ev>_<tipus>.<ext>
```

| Mező | Szabály | Példa |
|:-----|:--------|:------|
| `<szerzo>` | Első szerző vezetékneve, kisbetű, ékezet nélkül | `yeh`, `oppenheim` |
| `<ev>` | Megjelenési év (4 jegy) | `2016` |
| `_<tipus>` | Lásd típustáblázat | `_paper`, `_book` |
| `.<ext>` | Lehetőleg `pdf` | `.pdf` |

| Kód | Mit jelent |
|:----|:-----------|
| `paper` | Folyóirat- vagy konferenciacikk |
| `book` | Teljes könyv |
| `chapter` | Könyvfejezet |
| `slides` | Előadásdiasor (PDF) |
| `webpage` | Weboldal |
| `report` | Technikai jelentés |
| `thesis` | Disszertáció |
| `NA` | Hiányzó adat |

Azonos szerző + év: `a`/`b`/`c` suffix (pl. `yeh2016a_paper.pdf`).

### 3.2. Forrásgyűjtés (opcionális Deep Research)

Ha a user kéri, Claude WebSearch-szel felkutat releváns forrásokat:
1. Kulcscikkek: leggyakrabban hivatkozott alapcikkek
2. Oktatási anyagok: lecture notes, tutorial, review -- didaktikailag hasznosabb
3. Hazai/intézményi forrás: ha van, preferált

Ha `access == "open"`: WebFetch-szel letölti és elmenti `1_raw_inputs/`-ba.
Ha `access == "closed"`: DOI + letöltési URL listázása → 😎 manuálisan tölti le.

### 3.3. citations_seed.json generálása

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
    "note": "Alap -- STAMP algoritmus"
  }
}
```

`nlm_uuid` null marad -- a `02_nlm_notebook_setup` tölti ki.

### 3.4. NLM feltöltési útmutató (kimenet)

Claude listát ad a feltöltendő fájlokról:

```
✅ Letöltve (open access):
  - yeh2016_paper.pdf

😎 Manuálisan töltsd le:
  - zhu2016b_paper.pdf  DOI: 10.1109/ICDM.2016.0096
```

## 4. Kimenetek

- `1_raw_inputs/` -- PDF-ek és egyéb források
- `1_raw_inputs/citations_seed.json` -- metaadatok, `nlm_uuid: null` mezőkkel

## 5. Ellenőrzés

- [ ] Minden forrás fájlneve a naming convention szerint van
- [ ] `citations_seed.json` létezik, minden forráshoz bejegyzés van
- [ ] `nlm_uuid` mezők null-ok (feltöltés előtt helyes)
- [ ] Closed access forrásokhoz DOI / URL listázva van

## 6. Hibakezelés

- Tünet: `citations_seed.json` hiányzik, mert a user saját forrásokat hozott (01 kihagyva)
- Gyökérok: a `02_nlm_notebook_setup` feltételezi a seed meglétét
- Megoldás: manuálisan generáld a seed-et az `1_raw_inputs/` tartalmából; `nlm_uuid` marad null
- Megjegyzés: ha a seed manuálisan generált, a `nlm_uuid` mezők null-ok maradnak 02-ig

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [02_nlm_notebook_setup.md](02_nlm_notebook_setup.md)

## 8. Visszajelzések

- 🔲 TODO: A user nem kell hogy manuálisan töltse fel a forrásokat az NLM-be. Ha a 02_nlm_notebook_setup CLI-automatizmusa megbízhatóan működik, ez a lépés automatizálható.
- 💬 NOTE: Ha a user saját forrásokat hoz és az 01. lépés kihagyódik, a `citations_seed.json` nem jön létre automatikusan -- a 02_nlm_notebook_setup manuális seed-et igényel. Ez elfogadott workaround.
- 🔲 TODO: Claude a fájlneveket elemzi és a naming convention kérdéseket ebből vezeti le -- de a struktúrát (szerző, év, típus) a saját elemzéséből kell kitöltenie, nem a user-rel kérdeztetni. A visszakérdezés csak akkor indokolt, ha az elemzés egyértelműen nem elegendő.
- 🔲 TODO: Minden begyűjtött forrás eredetét rögzíteni kell: ki szerezte (user/Claude), honnan (URL/feltöltés), átnevezés előtti és utáni név. Tároló fájl: `1_raw_inputs/input_audit_trail.md`. Ez a skill §4 kimenetéhez tartozik -- a `citations_seed.json` mellé kötelező output.
- 💬 NOTE: Open access DOCX fájl akadémiai témában (pl. DFT/jelfeldolgozás) gyakorlatilag nem elérhető -- egyetemek PDF-et publikálnak, Scribd/ResearchGate/Academia.edu letöltéshez login kell. Ha a pipeline DOCX-tesztet igényel, a user-nek kell feltöltenie saját DOCX forrást.
- 🔲 TODO: Claude nem kérdezett vissza, hogy az adott héthez keressen-e még forrásokat (§3.2 Deep Research opció). A skill belépési pontján explicit prompt kell: "Keressek még releváns forrásokat ehhez a héthez?"
- 🔲 TODO: **Weblapok mentési módjai dokumentálandók -- képvesztés pipeline-következménnyel (tesztelve 2026-05-30, mini2).** Egyszerű HTML-mentéssel a képek elvesznek → `03_util_source_extractor.py` 0 képet ad → `figure_catalog.json`-ba nem kerülnek be → `09_figure_mapper` nem tudja beilleszteni → `03-1_qfig_parser.py` "nincs katalógus-bejegyzés" warninggal kihagyja (pl. techmonitor: 4 Qfig entry kihagyva). Ajánlott mentési módok: (1) **SingleFile Chrome bővítmény** -- képeket base64-be ágyazza, lokálisan kinyerhetők; (2) **PDF-print** (`msedge --headless --print-to-pdf`) -- MinerU feldolgozható, képeket megőrzi; (3) egyszerű HTML-mentés -- csak szöveg, képek nélkül (leggyengébb). Ajánlott sorrend: SingleFile > PDF-print > egyszerű HTML-mentés.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-30 | 2.1 | K0 cleanup: ❔ belépési pont lezárva (pipeline.md a kanonikus indítási dokumentum) |
| 2026-05-26 | 2.0 | Overhaul: template-alapú átírás; §8 Visszajelzések; pipeline diagram eltávolítva; TODO/NOTE/QUESTION konszolidálva |
| 2026-05-26 | 1.1 | NOTE: 01-02 seed függőség workaround dokumentálva |
| 2026-05-24 | 1.0 | Létrehozva (01-14 átszámozás) |
