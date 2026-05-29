---
title: Prompt C.3 -- Ábrajegyzék kulcsszavakkal
type: prompt
pipeline_step: 09_figure_mapper
updated: 2026-05-29
---

# Prompt C.3 — Ábrajegyzék kulcsszavakkal (képpipeline fallback)

**Hova:** NLM Studio → Data Tables → ceruza ikon  
**Mikor:** Ha `--vlm` (API kulcs) és `--qfig` CLI (NLM kvóta) nem elérhető.  
**Pipeline lépés:** [09_figure_mapper](../skills/09_figure_mapper.md) előkészítése — **elsődleges fallback**  
**Kimenet:** Export-Tool / kézi másolás → `3_raw_outputs/nlm_qfig_raw.txt` → `scripts/03-1_qfig_parser.py`

> Ez az **A prioritású fallback** VLM és Qfig CLI nélkül.  
> Részletek: [09_figure_mapper.md §6](../skills/09_figure_mapper.md)

```
Sorold fel az összes ábrát, diagramot, táblázatot és grafikont a forrásokban.
Minden elemhez add meg:
1. Forrás neve (fájlnév kiterjesztéssel, pontosan ahogy a Sources panelen látható)
2. Ábra száma (ha van, pl. "Figure 3")
3. Caption szövege (ha van, szó szerint)
4. 3-5 angol kulcsszó vesszővel elválasztva, amelyek leírják a vizuális tartalmat

Formátum minden elemhez:
FORRAS: <fajlnev.pdf>
SZAM: <abra szama vagy 'nincs'>
CAPTION: <caption szovege vagy 'nincs'>
KEYWORDS: <kulcsszavak>
---
```

**Feldolgozás mentés után:**
```powershell
python scripts/03-1_qfig_parser.py --week-dir test_outputs/<Tantargy>/N_het
python scripts/09_figure_mapper.py 3_raw_outputs/figure_catalog.json 4_wip_outputs/N_Jegyzet.md
```
