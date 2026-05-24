---
title: 1_KERDESEK.MD -- Matrix Profile
type: output
het: 1
updated: 2026-05-24
status: DRAFT
---

# 1. Kérdések -- Matrix Profile

**Hét:** 1. hét | **Dátum:** 2026-05-24 | **Státusz:** DRAFT

## 1. BSc kérdések (SZINT:2-3)

**K1** SZINT:2
Mit tárol a Matrix Profile minden eleme?
A) Az idősor adott pontjának értékét
B) A részsorozat és legközelebbi szomszédja közötti z-normalizált euklideszi távolságot
C) A részsorozat átlagát és szórását
D) Az idősor globális minimumát

**Helyes:** B

**K2** SZINT:2
Mire utal a Matrix Profile globális minimuma?
A) A leghosszabb monoton szakaszra
B) A legismétlődőbb mintapárra (motívumra)
C) A legzajosabb adatpontra
D) Az idősor trendjére

**Helyes:** B

**K3** SZINT:3
Miért előnyös a z-normalizált euklideszi távolság a nyers euklideszi távolsággal szemben?
A) Gyorsabb számítani
B) Amplitúdófüggetlen: azonos formájú, de különböző skálájú részsorozatok is hasonlónak minősülnek
C) Kevesebb memóriát igényel
D) Pontosabb anomáliadetektáláshoz vezet

**Helyes:** B

**K4** SZINT:3
Mi a különbség a STOMP és a Brute Force algoritmus komplexitása között?
A) Mindkettő $O(n^2)$, de különböző konstanssal
B) STOMP $O(n^2)$, Brute Force $O(n^2 m)$ -- STOMP a belső hurkot vektorizálással kerüli el
C) STOMP $O(n \log n)$, Brute Force $O(n^2)$
D) STOMP párhuzamos, Brute Force szekvenciális -- egyébként azonos

**Helyes:** B

## 2. MSc kérdések (SZINT:4-5)

**K5** SZINT:4
Miben tér el a SCRUMP a STOMP-tól?
A) SCRUMP egzakt, STOMP közelítő
B) SCRUMP közelítő (approximate) és gyorsabb; STOMP egzakt, de lassabb
C) SCRUMP csak GPU-n fut; STOMP CPU-n is
D) SCRUMP csak anomáliadetektálásra, STOMP csak motívumkeresésre alkalmas

**Helyes:** B

**K6** SZINT:5
Mit tárol a Profile Index, és mire használható?
A) A részsorozatok amplitúdóját; normalizáláshoz
B) Minden elemhez a legközelebbi szomszéd indeksét; visszakeresésre és vizualizációhoz
C) Az egyes elemek kiszámítási sorrendjét; párhuzamosításhoz
D) A távolságmátrix sávszélességét; memóriaoptimalizáláshoz

**Helyes:** B


# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-24 | 1.1 | Újragenerálva -- ékezetek javítva (09_question_bank_collector) |
