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

**Előfeltétel:** `figure_catalog.json` legalább egy entrynél `keywords != []` (03-1_qfig_parser, VLM, vagy `--from-caption` lefutott). Ha minden entry keywords üres, a mapper figyelmeztet és kilép. (`vlm_done=True` NEM szükséges feltétel -- tesztelve 2026-05-29.)

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
| **A** | **NLM Studio Data Tables ([Prompt C.3](../prompts/prompt_c3_abrajegyzek.md), manuális)** | Ingyenes, kontextuálisan gazdag, nem igényel API kulcsot vagy CLI kvótát | Manuális lépés (UI) |
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
- 💬 **TANULSÁG: NLM Studio Data Tables ([Prompt C.3](../prompts/prompt_c3_abrajegyzek.md)) mint elsődleges manuális fallback** — ha VLM és Qfig CLI nem elérhető, ez a legmegbízhatóbb út. Felvéve a §6 Hibakezelés táblába.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-30 | 3.1 | K0 cleanup: 6 ✅ → §9; §2 előfeltétel javítva (keywords != [] vs vlm_done); képbeillesztési pipeline működik (mini2/mini3 igazolja) |
| 2026-05-26 | 3.0 | Overhaul: template-alapú átírás; §8 Visszajelzések; archív Q5-szekció eltávolítva |
| 2026-05-25 | 2.0 | Teljes újraírás: VLM keywords → inserted_after_paragraph; script 09_figure_mapper.py |
| 2026-05-22 | 1.0 | Létrehozva (figure pipeline design) |
