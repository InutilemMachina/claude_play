---
name: 00c_mineru_extractor
title: 00C_MINERU_EXTRACTOR -- MinerU Figure Extractor
type: skill
tags: [meta, skill, figures]
status: active
version: 1.0
updated: 2026-05-23
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
# Teljes tantárgy (minden N_*/raw_sources/*.pdf)
conda run -n mineru python scripts/run_mineru_pipeline.py --root haromhetes_teszt

# Nagy fájl figyelmeztetési határ módosítása (alapértelmezett: 20 MB)
conda run -n mineru python scripts/run_mineru_pipeline.py --root haromhetes_teszt --warn-mb 50
```

**Manuális (egy hét, egy PDF):**

```powershell
# 1. MinerU: PDF-ek feldolgozasa -> kepek/ mappa
conda run -n mineru python scripts/mineru_pdf.py N_[tema]/raw_sources/ --output N_[tema]/clean_sources/kepek/

# 2. Katalogus epitese
conda run -n mineru python scripts/build_figure_catalog.py N_[tema]/clean_sources/kepek/
# output: N_[tema]/clean_sources/figure_catalog.json
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
| 2026-05-23 | 1.1 | Útvonalak frissítve: forrasok/ → clean_sources/; raw_sources/ junction dokumentálva |-|
| `clean_sources/kepek/SOURCE/images/*.jpg` | Átnevezett képek |
| `clean_sources/kepek/SOURCE/SOURCE.md` | Teljes paper MinerU-Markdown-ban |
| `clean_sources/figure_catalog.json` | Egységes katalógus (minden PDF-ből) |

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
| 2026-05-23 | 1.1 | Útvonalak frissítve: forrasok/ → clean_sources/; raw_sources/ junction dokumentálva ||--------
| 2026-05-23 | 1.2 | §2 Futtatás: run_mineru_pipeline.py ajánlottá téve; manuális parancsok megtartva |
| 2026-05-23 | 1.1 | Útvonalak frissítve: forrasok/ → clean_sources/; raw_sources/ junction dokumentálva ||

