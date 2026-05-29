---
name: 09_figure_mapper
title: 09_FIGURE_MAPPER -- Figure Mapper
type: skill
tags: [meta, skill, figures]
status: active
version: 3.0
updated: 2026-05-26
description: figure_catalog.json keywords × N_Jegyzet.md bekezdések → inserted_after_paragraph mező kitöltése. Script: 09_figure_mapper.py. Pipeline 09. lépése.
---

# 09_FIGURE_MAPPER

## 1. Cél

A `figure_catalog.json` kulcsszavait a `N_Jegyzet.md` bekezdéseivel veti össze, és minden képhez meghatározza a legjobb beillesztési pozíciót (`inserted_after_paragraph`). A tényleges beillesztés a 10_notes_collector feladata.

## 2. Bemenetek

- `3_raw_outputs/figure_catalog.json` -- 03_mineru_extractor + 03-1_qfig_parser kimenet
- `4_wip_outputs/N_Jegyzet.md` -- 06-08 kimenet (összefüggő próza + szekciók)

**Előfeltétel:** `figure_catalog.json` `keywords` mezői NEM üresek (03-1_qfig_parser lefutott). Ha `keywords == []` minden entrynél, a mapper figyelmeztet és kilép.

## 3. Eljárás

### 3.1. Futtatás

```powershell
python scripts\09_figure_mapper.py `
    test_outputs\<Tantargy>\N_het\3_raw_outputs\figure_catalog.json `
    test_outputs\<Tantargy>\N_het\4_wip_outputs\N_Jegyzet.md

# Opciók:
--min-matches 2    # minimum egyező token (alap: 1)
--dry-run          # csak kiírja a matcheket, nem ment
```

### 3.2. Kulcsszó-egyeztetés algoritmusa

**Bekezdés tokenizálás (stopword-szűréssel):**
```python
STOPWORDS = {"a", "az", "és", "vagy", "hogy", "ez", "egy", "is", "nem",
             "van", "volt", "lesz", "de", "ha", "the", "of", "in", "on", ...}

def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-záéíóöőúüű\w]+", text.lower())
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}
```

**Kizárt blokkok** (nem kerülnek a bekezdés-listába):
- `#` (fejléc), `![` (képhivatkozás), `<!--` (HTML komment), `>` (blockquote), `---`

**Egyeztetési logika:**
- Minden képnél: a legtöbb token-egyezést adó bekezdés indexe → `inserted_after_paragraph`
- Ha `match_score < MIN_MATCHES`: `inserted_after_paragraph = null`

### 3.3. Output mező séma

```json
{
  "yeh2016-img-1-p3": {
    "inserted_after_paragraph": 4,
    "match_score": 3
  }
}
```

| Mező | Típus | Leírás |
|:-----|:------|:-------|
| `inserted_after_paragraph` | `int \| null` | 0-bázisú bekezdés-index; `null` = nem illeszthető |
| `match_score` | `int` | Egyező tokenek száma |

## 4. Kimenetek

- `3_raw_outputs/figure_catalog.json` -- in-place frissítve (`inserted_after_paragraph`, `match_score` mezők)

## 5. Ellenőrzés

- [ ] Script lefutott figyelmeztetés nélkül
- [ ] `figure_catalog.json`-ban `inserted_after_paragraph` mezők kitöltve (nem mind null)
- [ ] `--dry-run` output logikus bekezdés-indexeket mutat

## 6. Hibakezelés

### Keywords-hiány: 3 útvonal prioritás szerint

Ha a `09_figure_mapper.py` lefut de nem talál egyezést (vagy korábban `vlm_done` miatt blokkolt), az oka mindig az, hogy `figure_catalog.json` entries-einek `keywords` mezeje üres. Három lehetséges javítás:

| # | Módszer | Előny | Hátrány |
|---|---------|-------|---------|
| **A** | **NLM Studio Data Tables (Prompt C, manuális)** | Ingyenes, kontextuálisan gazdag, nem igényel API kulcsot vagy CLI kvótát | Manuális lépés (UI) |
| **B** | **`04_nlm_dfs_queries.py --qfig` (CLI)** | Automatizált, ingyenes | NLM napi kvóta terhére, RESOURCE_EXHAUSTED lehetséges |
| **C** | **`03_util_figure_catalog.py --from-caption`** | Teljesen offline, script | Caption-minőségtől függ, EN→HU mismatch |

**A útvonal részletek (NLM Studio Data Tables):**

1. NLM notebook → Studio fül → Data Tables kártya → ceruza ikon
2. Prompt:
```
Sorold fel az összes ábrát, diagramot és táblázatot a forrásokban.
Minden elemhez add meg:
- Forrás neve (fájlnév kiterjesztéssel)
- Ábra száma (ha van)
- Caption (ha van)
- 3-5 angol kulcsszó vesszővel elválasztva
```
3. Generate → NotebookLM-Export-Tool → Markdown export → `3_raw_outputs/nlm_qfig_raw.txt`-be mentés
4. `python scripts/03-1_qfig_parser.py --week-dir ...`

Ez a legmegbízhatóbb útvonal VLM és CLI kvóta nélkül. **Mindig ezt kell javasolni elsőként, ha a VLM és a Qfig CLI nem elérhető.**

### Egyéb hibaesetek

- Tünet: minden `inserted_after_paragraph: null`
- Gyökérok: `keywords` üres (03-1_qfig_parser 0 egyezés -- BOM + szabad NLM formátum)
- Megoldás: 03-1_qfig_parser v2 futtatása (lásd §6 következő sor)
- Tünet: `03-1_qfig_parser` 0 egyezést ad (BOM + Markdown-bold formátum)
- Gyökérok: FIELD_RE nem kezeli `*   **Forrás:**` formátumot; `utf-8-sig` decode hiányzik
- Megoldás: FIELD_RE `r'^\*?\s*\*{0,2}(MEZŐ)\s*:\*{0,2}\s*(.*)'`; `read_bytes().decode("utf-8-sig")` ✅ javítva v2

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [03_mineru_extractor.md](03_mineru_extractor.md) -- figure_catalog forrása
- [10_notes_collector.md](10_notes_collector.md) -- tényleges beillesztés

## 8. Visszajelzések

- 💬 NOTE: Ha több kép ugyanarra a bekezdésre illeszkedik (`inserted_after_paragraph` azonos), a beillesztési sorrend `match_score` szerint csökkenő -- a 10_notes_collector kezeli.
- ✅ A 03-1_qfig_parser BOM + Markdown-bold formátum hiba javítva (2026-05-26, B1 fix). A képpipeline (09, 10) újra teljes -- Termografia_teszt_v3-on verifikálandó.
- ✅ **Blokkoló feltétel lazítva (2026-05-29).** `vlm_done=True` feltétel helyett `keywords != []` elegendő. A `09_figure_mapper.py` most fut Qfig- és caption-alapú keywords-szel is. A §2 és §6 frissítve.
- ✅ **ToC kizárva a paragraph matchingből (2026-05-29).** `is_preserved_block()` mostantól kizárja a `- [...]` link-listából álló blokkokat (>50% link-sor). Korábban a ToC kapta a legtöbb keywordhitett és minden kép oda kerülhetett.
- ✅ **`--from-caption` fallback (2026-05-29).** `03_util_figure_catalog.py --from-caption`: caption tokenizálás EN→HU szinoníma-bővítéssel, API kulcs és NLM kvóta nélkül.
- 💬 **TANULSÁG: NLM Studio Data Tables (Prompt C) mint elsődleges manuális fallback** — nem volt dokumentálva ebben a skillben, holott ez a legmegbízhatóbb út ha VLM és Qfig CLI nem elérhető. Felvéve a §6 Hibakezelés táblába A-prioritással.
- 🔲 TODO: **Előfeltétel pontatlan a skill §2-ban (tesztelve 2026-05-28).** A §2 szerint a blokkoló feltétel `keywords == []`, de a script (line 133-136) `vlm_done=True` hiányát ellenőrzi és kilép. Ha `vlm_done=False` (pl. VLM nem futott), a script "No entries with vlm_done=True. Run 03_util_figure_catalog.py --vlm first." üzenettel exitál -- a `keywords`-t meg sem nézi. A §2 szövegét frissíteni kell: "Előfeltétel: `vlm_done=True` legalább egy entrynél (03_util_figure_catalog.py --vlm lefutott)."
- 🔲 TODO: **Nincsenek képek a wip Jegyzetben (user feedback, 2026-05-28, 1_het).** A `4_wip_outputs/1_Jegyzet.md` nem tartalmaz egyetlen képet sem. Gyökérok: (1) `09_figure_mapper` blokkolt (`vlm_done=False`), így `inserted_after_paragraph` mezők üresek; (2) `10_notes_collector --no-figures` opcióval futott (képbeillesztés szándékosan kihagyva). A teljes kép-pipeline (03-1 Qfig → 09 mapper → 10 inserter) blokkolt a `vlm_done` és a Qfig formátum-eltérés miatt. Következmény: a Jegyzet szöveg-only -- a forrás PDF-ek vizuális tartalma (ábrák, táblázatok) elvész.
- ✅ **VLM lépés pipeline-ban dokumentálva (javítva 2026-05-28).** `pipeline.md §1` IO táblájába felvéve: `03_util_figure_catalog.py --vlm` a 03-1_qfig_parser után, 03-2_dedup előtt.
- ✅ **03_util_figure_catalog.py syntax hiba javítva (2026-05-28).** `2_clean_inputs_dir` → `clean_inputs_dir` (line 119 + 128). A `--vlm` flag most futtatható.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-26 | 3.0 | Overhaul: template-alapú átírás; §8 Visszajelzések; archív Q5-szekció eltávolítva |
| 2026-05-25 | 2.0 | Teljes újraírás: VLM keywords → inserted_after_paragraph; script 09_figure_mapper.py |
| 2026-05-22 | 1.0 | Létrehozva (figure pipeline design) |
