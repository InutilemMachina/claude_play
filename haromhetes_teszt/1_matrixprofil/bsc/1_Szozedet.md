---
title: 1_SZOZEDET.MD -- Matrix Profile
type: output
het: 1
updated: 2026-05-24
status: DRAFT
---

# 1. Szójegyzék -- Matrix Profile

**Hét:** 1. hét | **Dátum:** 2026-05-24 | **Státusz:** DRAFT

| Magyar terminus | Angol terminus | Definíció | Szint |
|:----------------|:---------------|:----------|:------|
| *Matrix Profile* | *Matrix Profile* | Vektor, amely minden részsorozat és legközelebbi szomszédja közötti z-normalizált euklideszi távolságot tárolja; $O(n)$ térkomplexitás. | BSc |
| *részsorozat* | *subsequence* | Az idősor $m$ hosszúságú ablakkal kivágott szegmense: $T[i:i+m]$. | BSc |
| *motívum* | *motif* | Visszatérő minta: a Matrix Profile globális minimumát adó részsorozat-pár. | BSc |
| *anomália* | *anomaly / discord* | Ritka, szokatlan részsorozat: a Matrix Profile globális maximumát adó elem. | BSc |
| *euklideszi távolság* | *Euclidean distance* | $D_{i,j} = \sqrt{\sum_{k=0}^{m-1}(T_{i+k}-T_{j+k})^2}$; a részsorozatok hasonlóságának alapmértéke. | BSc |
| *z-normalizálás* | *z-normalization* | Középre igazítás és egységnyi szórásra skálázás; amplitúdófüggetlen összehasonlítást tesz lehetővé. | BSc |
| *STOMP* | *STOMP (Scalable Time series Ordered Matrix Profile)* | 2016-os egzakt algoritmus; $O(n^2)$ idő, $O(n)$ memória; STUMPY magja. | MSc |
| *SCRUMP* | *SCRUMP* | Közelítő, gyors Matrix Profile számítás; sebesség-kritikus esetekre. | MSc |
| *Profile Index* | *Profile Index* | A Matrix Profile kísérőtömbje: minden elemhez tárolja a legközelebbi szomszéd indeksét. | MSc |

## Irodalomjegyzék

[1] STUMPY Documentation (2024). *STUMPY Basics Tutorial*. stumpy2024_webpage.

# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-24 | 1.1 | Újragenerálva -- ékezetek javítva (04_citations_maker) |
