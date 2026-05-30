---
title: Prompt C.4 -- Kérdésbank-alap táblázat
type: prompt
tags: [meta, prompt]
pipeline_step: 13_question_bank_collector
updated: 2026-05-29
---

# Prompt C.4 — Kérdésbank-alap táblázat

**Hova:** NLM Studio → Data Tables → ceruza ikon  
**Mikor:** 13_question_bank_collector lépés előtt — nyers kérdésanyag generálása.  
**Pipeline lépés:** [13_question_bank_collector](../skills/13_question_bank_collector.md)  
**Kimenet:** Export-Tool / kézi másolás → `3_raw_outputs/` → Claude feldolgozza

**Különbség a Studio Kvíz/Tanulókártyáktól:**  
Studio Kvíz = kész fogyasztói formátum, nem pipeline-kompatibilis.  
Ez a tábla = strukturált nyers adat → Claude végzi a BSc/MSc szűrést.

```
Készíts vizsgakérdés-alap táblázatot 20-30 kérdéssel a feltöltött forrásokból.

Oszlopok:
1. Téma / fejezet
2. Kulcsállítás vagy tény (tesztelendő tudáselem)
3. Helyes válasz (rövid, 1-2 mondat)
4. Nehézségi szint (1=alapfogalom, 2=alkalmazás, 3=elemzés, 4=értékelés, 5=szintézis)
5. Szint (BSc / MSc)
6. Forrás neve (fájlnév kiterjesztéssel)

Minden sorhoz legyen megadva a forrás.
Ha egy állítás több forrásból is alátámasztható, az összeset tüntesd fel.
```
