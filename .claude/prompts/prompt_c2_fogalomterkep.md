---
title: Prompt C.2 -- Fogalomtérkép táblázat
type: prompt
pipeline_step: 07_citations_maker
updated: 2026-05-29
---

# Prompt C.2 — Fogalomtérkép táblázat (terminológia-audit)

**Hova:** NLM Studio → Data Tables → ceruza ikon  
**Mikor:** Adott heti téma kulcsfogalmainak kétnyelvű összegyűjtésére.  
**Pipeline lépés:** 07_citations_maker szószedet-alapként  
**Kimenet:** Export-Tool / kézi másolás → `4_wip_outputs/N_Szozedet.md`

```
Készíts kétnyelvű terminológiai táblázatot a feltöltött forrásokból az adott témakörre.

Oszlopok:
1. Magyar terminus
2. Angol terminus
3. Definíció (max. 1 mondat, forrás alapján)
4. Kontextus / alkalmazási terület
5. Kapcsolódó fogalmak
6. Forrás neve (fájlnév kiterjesztéssel)
7. Szint (BSc / MSc / mindkettő)

Csak olyan fogalmakat vegyél fel, amelyek legalább egy feltöltött forrásban explicit megjelennek.
```
