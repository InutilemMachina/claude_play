---
name: 05b_figure_mapper
title: 05B_FIGURE_MAPPER -- Figure Mapper
type: skill
tags: [meta, skill, figures]
status: active
version: 1.0
updated: 2026-05-22
description: figure_catalog.json + NLM Q5 → REVIEW placeholder-ek a Jegyzetbe. Helye: 05_mindmap_manager utan, 06_notes_collector elott.
---

# 05B_FIGURE_MAPPER.MD -- Figure Mapper
_05b. lepes_

# 1. Cel es helye a pipeline-ban

```
05_mindmap_manager → 05b_figure_mapper 🤖 → 06_notes_collector → ...
```

Összeköti a `figure_catalog.json` képeit a `N_Jegyzet.md` szekciójával.
Minden javasolt ábra `<!-- FIG:... -->` REVIEW placeholder-ként kerül be;
a felhasználó elfogadja vagy törli őket.

# 2. Bemenetek

| Fájl | Honnan |
|:-----|:-------|
| `forrasok/figure_catalog.json` | 00c_mineru_extractor |
| `forrasok/nlm_q5_raw.txt` | 01_nlm_query_runner Q5 |
| `N_het/N_Jegyzet.md` | 06 előtti állapot |

# 3. NLM Q5 ábra-query (01_nlm_query_runner bővítése)

Az `01_nlm_query_runner` Q5 queryjét ábra-azonosításra kell hangolni:

```
Prompt: "Melyik ábra, diagram vagy táblázat illusztrálja legjobban
az alábbi témákat? Adj meg szerzőt, figure-számot és idézd a pontos
feliratát.
Témák: [mindmap 2. szintű csomópontjai]"
```

Az NLM válasza pl.:
"Yeh et al. (2016), Figure 1: 'An example matrix profile P and matrix
profile index I for time series T' -- jól mutatja az MP alapstruktúráját."

# 4. Egyeztetési logika

## 4.1. NLM Q5 alapú egyeztetés (prioritás: 1)

```python
import re, json
from pathlib import Path
from difflib import SequenceMatcher

catalog = json.loads(Path("forrasok/figure_catalog.json").read_text())
q5_text = Path("forrasok/nlm_q5_raw.txt").read_text(encoding="utf-8-sig")

# NLM valasz parsed: "Figure N" + szerzo + caption-reszlet
fig_refs = re.findall(
    r'(?:Figure|Fig\.?)\s*(\d+)[:\.]?\s*[\'"]?([^\'"\n]{10,80})',
    q5_text, re.IGNORECASE
)

def best_match(caption_fragment, catalog):
    best_key, best_score = None, 0
    for k, v in catalog.items():
        score = SequenceMatcher(None,
            caption_fragment.lower(), v["caption"].lower()).ratio()
        if score > best_score:
            best_score, best_key = score, k
    return best_key if best_score > 0.4 else None
```

## 4.2. Kulcsszó-egyezés (fallback, prioritás: 2)

Ha Q5 nem ad elég pontot:
- Minden `figure_catalog` bejegyzés `caption` szavait egyeztetjük
  a Jegyzet `##`/`###` fejlécszavaival
- Threshold: ≥2 közös érdemi szó (stopwordok kizárva)

# 5. REVIEW placeholder formátum

```markdown
<!-- FIG:yeh2016-img-1-p3:nlm -->
![Matrix Profile P és I vektor (Yeh et al., 2016)](forrasok/kepek/yeh2016_paper/images/image_1_p3.jpg)
*ábra: Matrix Profile P és I vektor felépítése* <sup>[[3]](#ref-3)</sup>
<!-- /FIG -->
```

Jelölők:
- `:nlm` -- NLM Q5 javasolta (megbízhatóbb)
- `:auto` -- kulcsszó-egyezés eredménye (felülvizsgálandó)

A REVIEW placeholder-ek a megfelelő `###` alfejezet UTÁN, a `> 💡 Lényeg`
blockquote ELŐTT kerülnek be.

# 6. Felhasználói review

A placeholder-ek beillesztése után 😎 feladat:
1. Megnyitja a Jegyzetet
2. Minden `<!-- FIG:...:nlm -->` vagy `<!-- FIG:...:auto -->` helyen
   megnézi az ajánlott képet
3. Ha megfelelő: csak a `<!-- FIG:... -->` és `<!-- /FIG -->` kommenteket törli
4. Ha nem megfelelő: az egész blokkot törli

Ez nem kemény checkpoint (nincs 🛑) -- a Jegyzet placeholder nélkül is helyes.

# 7. 07_typesetter kapcsolat

A `07_typesetter` Szabály C (`![` előtt üres sor) automatikusan kezeli
a bekezdéstöréseket a beillesztett ábráknál -- nincs külön teendő.

# 8. Nyitott kerdesek

- Ha a figura-catalog üres (MinerU nem futott): 05b kihagyható, figyelmeztet.
- Táblázatok (`table_N_pP.jpg`) kezelése: más placeholder-típus kell?
- Beágyazott ábra Markdown vs. HTML `<figure>` tag?

# Valtozasnaplo

- 2026-05-22 -- Létrehozva (figure pipeline design alapján)

# Ismert hibák

→ [pitfalls.md §4.1](../pitfalls.md) -- MinerU extra auto/ könyvtárszint

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
