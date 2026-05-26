---
name: 09_figure_mapper
title: 09_FIGURE_MAPPER -- Figure Mapper
type: skill
tags: [meta, skill, figures]
status: active
version: 2.0
updated: 2026-05-25
description: figure_catalog.json keywords × N_Jegyzet.md bekezdések → inserted_after_paragraph mező kitöltése. Előfeltétel: 03 VLM futás (keywords nem üres).
---

# 09_FIGURE_MAPPER.MD -- Figure Mapper

**Script:** `scripts/09_figure_mapper.py`

**Pipeline helye:**
```
03 (VLM keywords) → 09_figure_mapper → 10_notes_collector
```

⚠️ **Előfeltétel:** A `figure_catalog.json` `keywords` mezői NEM üresek (03 VLM futott).
Ha `keywords == []` minden entrynél, a mapper figyelmeztet és kilép.

# 1. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `3_raw_outputs/figure_catalog.json` | 03_mineru_extractor + VLM | 100 entry, `keywords` feltöltve |
| `4_wip_outputs/N_Jegyzet.md` | 06-08 kimenet | Összefüggő próza + szekciók |

# 2. Mit csinál pontosan

Minden `figure_catalog.json` entrynél (ahol `keywords` nem üres):

1. A Markdown bekezdéseit tokenizálja (stopword-szűréssel).
2. A kép `keywords` listáját a bekezdés-tokenekkel veti össze.
3. Legtöbb egyezést adó bekezdés indexét írja az entry `inserted_after_paragraph` mezőjébe.
4. A `match_score` mezőbe kerül az egyezések száma.
5. Ha `match_score < MIN_MATCHES` (default: 1): `inserted_after_paragraph = null` (nem illeszthető).

**Output:** `3_raw_outputs/figure_catalog.json` in-place frissítve.

# 3. Kulcsszó-egyeztetés algoritmusa

## 3.1. Bekezdés tokenizálás

```python
STOPWORDS = {
    "a", "az", "és", "vagy", "hogy", "ez", "egy", "is", "nem",
    "van", "volt", "lesz", "de", "ha", "the", "of", "in", "on",
    "at", "for", "with", "by", "from", "as", "an", "to", "are",
    "this", "that", "which", "can", "be", "it", "its"
}

def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-záéíóöőúüű\w]+", text.lower())
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}
```

## 3.2. Bekezdés-szűrés (megőrzött blokkok kizárva)

A következő sorokkal kezdődő blokkok NEM kerülnek be a bekezdés-listába:
- `#` (Markdown fejléc)
- `![` (képhivatkozás)
- `<!--` (HTML komment)
- `>` (blockquote)
- `---` (HR / YAML)

## 3.3. Egyeztetési logika

```python
for key, entry in catalog.items():
    kw_tokens = set()
    for kw in entry["keywords"]:          # pl. ["thermal camera", "emissivity"]
        kw_tokens.update(kw.lower().split())

    best_idx, best_score = -1, 0
    for idx, p_tokens in enumerate(para_tokens):
        score = len(kw_tokens & p_tokens)
        if score > best_score:
            best_score, best_idx = score, idx

    entry["inserted_after_paragraph"] = best_idx if best_score >= MIN_MATCHES else None
    entry["match_score"] = best_score
```

# 4. Output mezők (figure_catalog.json bővítése)

```json
{
  "11-Termografia-2-image-1-p2": {
    "source": "11-Termografia-2.pdf",
    "page": 2,
    "type": "image",
    "caption": "Infravörös hőkamera rendszerfelépítése...",
    "path": "2_clean_inputs/11-Termografia-2/auto/images/abc123.jpg",
    "keywords": ["thermal camera", "focal plane array", "detector"],
    "vlm_done": true,
    "inserted_after_paragraph": 4,
    "match_score": 3
  }
}
```

| Mező | Típus | Leírás |
|:-----|:------|:-------|
| `inserted_after_paragraph` | `int \| null` | 0-bázisú bekezdés-index a Markdown-ban; `null` = nem illeszthető |
| `match_score` | `int` | Egyező token-ek száma (0 = nincs egyezés) |

# 5. Beillesztés a Markdown-ba (10_notes_collector feladata)

A `09_figure_mapper` **csak a catalog-ot frissíti** -- nem módosítja a Markdown-ot.
A tényleges `![...]` beillesztés a 10_notes_collector lépés feladata:

```python
# 10_notes_collector: catalog -> Markdown insertion
for key, entry in sorted(catalog.items(),
                          key=lambda x: x[1].get("inserted_after_paragraph") or 9999):
    idx = entry.get("inserted_after_paragraph")
    if idx is None:
        continue
    fig_block = (
        f"\n![{entry['caption']}]({entry['path']})\n"
        f"*{entry['caption']}*\n"
    )
    paragraphs[idx] = paragraphs[idx] + fig_block
```

⚠️ **Fontos:** Ha több kép ugyanarra a bekezdésre illeszkedik (`inserted_after_paragraph` azonos),
a beillesztési sorrend `match_score` szerint csökkenő.

# 6. Futtatás

```powershell
python scripts\09_figure_mapper.py `
    test_outputs\<Tantargy>\N_het\3_raw_outputs\figure_catalog.json `
    test_outputs\<Tantargy>\N_het\4_wip_outputs\N_Jegyzet.md
```

Opcionális flag:
```powershell
--min-matches 2    # minimum egyező token (default: 1)
--dry-run          # csak kiírja a matcheket, nem ment
```

# 7. Régi Q5-alapú megközelítés (archív)

Az előző verzió NLM Q5 queryt (ábra-azonosítás) és caption-hasonlóságot használt.
Ez heurisztikus volt (figure-számok, "Figure N" regex) és csak akkor működött,
ha az NLM hivatkozott az ábrákra. Felváltotta a VLM keywords × paragraph egyezés.

Archív kód: [archive/05b_figure_mapper_v1.md](.claude/archive/) (ha archiválva)

# Ismert hibák

→ [pitfalls.md §4.1](../pitfalls.md) -- MinerU extra auto/ könyvtárszint
→ [pitfalls.md](../pitfalls.md) -- keywords üres ha VLM nem futott (P4 előfeltétel)

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-25 | 2.0 | Teljes újraírás: VLM keywords → inserted_after_paragraph; 09 számozás; régi Q5-logika archivált; script 09_figure_mapper.py dokumentálva |
| 2026-05-22 | 1.0 | Létrehozva (figure pipeline design, Q5 + caption-similarity) |
