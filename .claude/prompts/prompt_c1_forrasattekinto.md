---
title: Prompt C.1 -- Forrásáttekintő táblázat
type: prompt
pipeline_step: 01_references_collector
updated: 2026-05-29
---

# Prompt C.1 — Forrásáttekintő táblázat

**Hova:** NLM Studio → Data Tables → ceruza ikon  
**Mikor:** Minden új notebook indulásakor — a feltöltött forrásokat térképezi fel.  
**Kimenet:** Export-Tool / kézi másolás → `1_raw_inputs/` vagy `3_raw_outputs/`

```
Készíts strukturált forrásáttekintő táblázatot a feltöltött dokumentumokból.

Oszlopok:
1. Forrás neve (fájlnév, kiterjesztéssel — pontosan ahogy a Sources panelen látható)
2. Szerzők és év (pl. "Kovács J., 2019")
3. Forrástípus (könyv / folyóiratcikk / konferenciacikk / előadásanyag / webes forrás / kézirat)
4. Fő témakör (1-2 mondatos összefoglalás)
5. BSc szintű kulcsfogalmak (max. 5, vesszővel)
6. MSc szintű kiegészítés (mi az, ami BSc-n felül kerül elő — max. 3 pont)
7. Kulcsadatok és tipikus paraméterek (mért értékek, tartományok, képletek, ha van)
8. Pipeline felhasználhatóság (Kivonat / Prezentáció / Kérdésbank / Mindhárom)
```
