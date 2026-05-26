---
name: 05_source_controller
title: 05_SOURCE_CONTROLLER — Source controller
type: skill
tags: [meta, skill]
status: active
version: 1.1
updated: 2026-05-26
description: Forrásrészek azonosítása és összeállítása az adott hét forrasok/ mappájából. Checkpoint: 👤 jóváhagyás szükséges.
---

# 05_SOURCE_CONTROLLER.MD — SOURCE CONTROLLER
_02. lépés_

# 1. Cél
Az adott hét `forrasok/` mappájának tartalmát feltérképezni, a `context.md` tematikájával összevetni, és a releváns részeket azonosítani — a 03_excerpt_block_maker–09_question_bank_collector lépések számára.

# 2. Folyamat
1. `context.md` N. heti témájának beolvasása
2. `N_het/forrasok/*.md` fájlok fejezeteinek áttekintése
3. Releváns fejezetek/szakaszok azonosítása
4. Összefoglaló lista készítése (nem fájl — Claude belső kontextusa)
5. ⚠️ Jóváhagyás kérése — **🛑 nélküle nem folytatja**

# 3. Jóváhagyáshoz megjelenítendő összefoglaló
```
N. hét témája: [téma]
Felhasznált forrásrészek:
- vezeteknev2024.md → 2. fejezet: Kavitáció (Kivonat + Jegyzet)
- chattopadhyay2013.md → Intro + Types (Kivonat + Kérdésbank)
```

# 4. Szabályok
- Ha a `forrasok/` mappa üres vagy hiányzik: **🛑 leáll, feltöltést kér**
- Ha egy fejezet nem releváns az adott héthez: ne szerepeljen
- Egy fejezet több héten is felhasználható — minden hétnél újra azonosítandó
- Pipeline NLM esetén: `tema_nev.md` (01_html_to_md kimenet) az egyetlen forrás
- Pipeline PDF esetén: egy vagy több `vezeteknev2024.md` fájl

# 5. Nincs `forrasok.md` fájl
A 02_source_controller nem hoz létre `forrasok.md` fájlt — az összefoglaló csak a Claude munkamenetben él. A döntés rögzítése opcionálisan a `project_status.md`-be kerülhet.


# Ismert hibák

Nincs ismert, skill-specifikus pitfall. Általános: [pitfalls.md](../pitfalls.md)

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
