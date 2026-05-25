---
name: 00c_mineru_extractor
title: 00C_MINERU_EXTRACTOR -- MinerU Figure Extractor
type: skill
tags: [meta, skill, figures]
status: active
version: 2.0
updated: 2026-05-24
description: MinerU futtatása forrasok/*.pdf-re. figure_catalog.json építése content_list.json alapján. Helye a pipeline-ban: 00_references_collector utan, 00b_nlm_notebook_setup elott (vagy párhuzamosan).
---

# 00C_MINERU_EXTRACTOR.MD -- MinerU Figure Extractor
_00c. lepes_

# 1. Cel es helye a pipeline-ban

```
00_references_collector → 00c_mineru_extractor 🐍 → 00b_nlm_notebook_setup 🔌 → ...
```

Minden forrás-PDF-ből kinyeri a képeket, táblázatokat és egyenleteket,
majd egy `figure_catalog.json`-t épít, amelyet a `05b_figure_mapper` használ.

# 2. Futtatas

**Ajánlott:** `scripts/run_mineru_pipeline.py` -- vizuális progress, notebook/fájl számláló,
nagy fájl kérdés, összefoglaló tábla. A claude_play gyökeréből futtatandó.

```powershell
# Teljes tantárgy (minden N_*/raw_inputs/*.pdf)
conda run -n mineru python scripts/run_mineru_pipeline.py --root haromhetes_teszt

# Nagy fájl figyelmeztetési határ módosítása (alapértelmezett: 20 MB)
conda run -n mineru python scripts/run_mineru_pipeline.py --root haromhetes_teszt --warn-mb 50
```

**Manuális (egy hét, egy PDF):**

```powershell
# 1. MinerU: PDF-ek feldolgozasa -> kepek/ mappa
conda run -n mineru python scripts/mineru_pdf.py N_[tema]/raw_inputs/ --output N_[tema]/clean_inputs/kepek/

# 2. Katalogus epitese
conda run -n mineru python scripts/build_figure_catalog.py N_[tema]/clean_inputs/kepek/
# output: N_[tema]/clean_inputs/figure_catalog.json
```
# 3. figure_catalog.json epites

A katalógust `scripts/build_figure_catalog.py` építi (önálló script, futtatható).
A `*_content_list.json` fájlok minden PDF-re tartalmazzák:
- `type`: image, table, chart, equation, seal
- `page_idx`: 0-alapú oldalszám
- `img_path`: relatív útvonal az images/ mappán belül
- caption mezők: `image_caption`, `table_caption`, `chart_caption` (lista)
- fallback: `text` mező (inline szöveg)

Generált kulcs formátuma: `{source_stem}-{type}-{n}-p{page}`

# 4. Kimenet

| Fájl | Tartalom |
|:-----|:--------
| 2026-05-23 | 1.2 | §2 Futtatás: run_mineru_pipeline.py ajánlottá téve; manuális parancsok megtartva |
| 2026-05-23 | 1.1 | Útvonalak frissítve: forrasok/ → clean_inputs/; raw_inputs/ junction dokumentálva |-|
| `clean_inputs/kepek/SOURCE/images/*.jpg` | Átnevezett képek |
| `clean_inputs/kepek/SOURCE/SOURCE.md` | Teljes paper MinerU-Markdown-ban |
| `clean_inputs/figure_catalog.json` | Egységes katalógus (minden PDF-ből) |

# 5. Ismert korlatok

- Kéthasábos akadémiai PDF-nél a caption és a kép párosítása nem mindig pontos.
- Egyenlet-képek (`equation_N_pP.jpg`) általában nem kerülnek a Jegyzetbe
  (a Jegyzetben LaTeX-képletként szerepelnek).
- MinerU futása lassú: 1-5 perc/PDF; párhuzamosítható a 00b lépéssel.
- `SKIP_FILES` a `mineru_pdf.py`-ban: ismételt futtatás esetén kihagyja a kész PDF-eket.
- A `scripts/` mappa a playground gyökerén van; más tantárgymappából is innen kell hívni.

# Valtozasnaplo

- 2026-05-22 -- Létrehozva (PoC tapasztalat: ábrák hiányoznak a Jegyzetből)
- 2026-05-23 -- Parancsszintaxis javítva (--output arg); build_figure_catalog.py kiszervezve

# Ismert hibák

→ [pitfalls.md §4.1](../pitfalls.md) -- MinerU extra auto/ könyvtárszint
→ [pitfalls.md §4.2](../pitfalls.md) -- MinerU HTML forrást nem tud feldolgozni
→ [pitfalls.md §4.3](../pitfalls.md) -- conda run + Start-Job: nem vár
→ [pitfalls.md §4.4](../pitfalls.md) -- Hosszú PDF-ek futási idő

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------
| 2026-05-23 | 1.2 | §2 Futtatás: run_mineru_pipeline.py ajánlottá téve; manuális parancsok megtartva |
| 2026-05-23 | 1.1 | Útvonalak frissítve: forrasok/ → clean_inputs/; raw_inputs/ junction dokumentálva ||--------
| 2026-05-23 | 1.2 | §2 Futtatás: run_mineru_pipeline.py ajánlottá téve; manuális parancsok megtartva |
| 2026-05-23 | 1.1 | Útvonalak frissítve: forrasok/ → clean_inputs/; raw_inputs/ junction dokumentálva ||

# Képpipeline részletek (átvéve kepek_workflow.md-ből)

_Forrás: .claude/kepek_workflow.md -- 2026-05-24 beolvasztva_

## 4. figure_catalog.json

A scripts/build_figure_catalog.py a *_content_list.json fájlokból épít katalógust.

```json
{
  "yeh2016-img-1-p3": {
    "source": "yeh2016_paper.pdf",
    "page": 3,
    "type": "image",
    "caption": "Figure 1: An example matrix profile P and matrix profile index I...",
    "path": "forrasok/kepek/yeh2016_paper/auto/images/fig_001_p003_matrix_profile.jpg",
    "keywords": []
  }
}
```

Helye: N_het/forrasok/figure_catalog.json


## 5. NLM Q5 ábra-lekérdezés

Az 01_nlm_query_runner Q5 queryjét ábra-azonosításra is használjuk.

Q5 prompt minta:
```
Melyik ábra/diagram/táblázat illusztrálja legjobban a következő témákat:
(1) MP vektor és index felépítése, (2) STAMP/STOMP összehasonlítás?
Nevezd meg a szerzőt és az ábra feliratát pontosan.
```

NLM visszaad pl.: "Yeh et al. (2016), Figure 1: 'An example matrix profile...'"
Ez egyeztethető a figure_catalog.json caption mezőivel.

Output: forrasok/nlm_q5_raw.txt

Egyeztetési stratégiák prioritása:
1. NLM Q5 caption match (legmegbízhatóbb)
2. Caption kulcsszó-egyezés (automatikus fallback)
3. Oldalszám-alapú egyezés
4. Kézi mapping


## 6. 05b_figure_mapper lépés

figure_catalog.json + nlm_q5_raw.txt alapján REVIEW flaggel jelölt placeholdereket szúr be:

```markdown
<!-- FIG:yeh2016-img-1-p3:REVIEW -->
![Matrix Profile P és I vektor](forrasok/kepek/yeh2016_paper/auto/images/fig_001_p003.jpg)
*ábra: Matrix Profile P és I vektor felépítése* [ref]
<!-- /FIG -->
```

FIG:auto = kulcsszó-egyezés alapján; FIG:nlm = NLM Q5 javasolta.
Felhasználó elfogadja vagy elveti a REVIEW flaggel jelölt blokkokat.


## 7. Kép-hivatkozás formátumok

## 7.1. Inline kép

```markdown
![Figure 3: Matrix profile (P)](forrasok/kepek/fig_003_p003_matrix_profile_overview.jpg)
*Figure 3. Forrás: Matrix Profile I.pdf, 18. o.*
```

## 7.2. Placeholder (MinerU még nem futott)

```markdown
![PLACEHOLDER: Figure 3](forrasok/kepek/PLACEHOLDER_fig_003.png)
*[Kép betöltendő: Matrix Profile I.pdf, Figure 3, 18. o.]*
```

## 7.3. MSc-jelölt kép blokk

```markdown
<!-- MSc -->
![Figure 7: GPU-STOMP](forrasok/kepek/fig_007_p007_gpu_stomp.jpg)
*Figure 7. Forrás: Matrix Profile II.pdf*
<!-- /MSc -->
```


## 8. Placeholder csere valódi képre

👤 Manuális lépés, egyszer PDF-enként:
TODO: A mineru-t te is tudod automatizáltan futtatni. 
TODO: CRITICAL ezt a képorientált workflow-t kialakítani.
1. mineru_pdf.py futtatása
2. mineru_rename.py futtatása
3. Képek másolása forrasok/kepek/-be
4. PLACEHOLDER hivatkozások cseréje valódi fájlnevekre


