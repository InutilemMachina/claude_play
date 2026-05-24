---
title: 1_JEGYZET.MD -- Matrix Profile
type: output
het: 1
updated: 2026-05-24
status: DRAFT
notebook: 013ea69e-ee02-4a13-9389-7f46d7fb37ae
---

# 1. Heti Jegyzet -- Matrix Profile

**Hét:** 1. hét | **Dátum:** 2026-05-24 | **Státusz:** DRAFT

## Tanulási célok

1. Megérteni a Matrix Profile definícióját és térkomplexitásának előnyét.
2. Megmagyarázni a z-normalizálás szerepét a részsorozat-hasonlóság számításában.
3. Azonosítani a motívum és az anomália fogalmát a Matrix Profile alapján.
4. Összehasonlítani a STOMP és Brute Force algoritmus komplexitását.


<!-- Q:1 -->
## 2. Definíció és adatstruktúra

A **Matrix Profile** egy $O(n)$ méretű vektor, amely minden $m$ hosszú részsorozathoz tárolja a legközelebbi szomszéd z-normalizált euklideszi távolságát [1].

> **💡 Lényeg:** A Matrix Profile csak a távolságmátrix minimumait tartja meg -- az $O(n^2)$ mátrix helyett $O(n)$ vektort. Ez teszi lehetővé a nagy idősorok hatékony kezelését.

<!-- Q:2 -->
## 3. z-normalizált euklideszi távolság

A hasonlóság alapmértéke: $D_{i,j} = \sqrt{\sum_{k=0}^{m-1}(\hat{T}_{i+k} - \hat{T}_{j+k})^2}$, ahol $\hat{T}$ z-normalizált. [1]

> **💡 Lényeg:** A z-normalizálás amplitúdófüggetlen összehasonlítást tesz lehetővé. Azonos formájú, de különböző méretű részsorozatok is hasonlónak minősülnek.

> **🗺️ Fejezet összegzés -- 3. z-normalizálás**

<!-- Q:3 -->
## 4. Motívum és anomália

A Matrix Profile **globális minimuma** a leghasonlóbb részsorozat-párt (motívum) jelöli; **globális maximuma** a legritkább, legszokatlanabb részsorozatot (anomália / discord) azonosítja. [1]

> **💡 Lényeg:** Egyetlen Matrix Profile számítással mind a motívumkeresés, mind az anomáliadetektálás elvégezhető -- nincs szükség külön modellekre.


> **🗺️ Fejezet összegzés -- 4. Motívum és anomália**

<!-- Q:4 -->
## 5. Algoritmusok

| Algoritmus | Időkomplexitás | Memória | Megjegyzés |
|:-----------|:---------------|:--------|:-----------|
| Brute Force | $O(n^2 m)$ | $O(n^2)$ | Naiv; 5 év adat: 4,4 év gépidő [1] |
| **STOMP** | $O(n^2)$ | $O(n)$ | Egzakt; STUMPY magja; GPU/Dask [1] |
| SCRUMP | $O(n^2)$ közelítő | $O(n)$ | Gyors közelítő; sebesség-kritikus esetekre [1] |

> **💡 Lényeg:** A STOMP a Brute Force belső hurkát vektorizálással váltja ki, drasztikusan csökkentve a számítási időt.

> **🗺️ Fejezet összegzés -- 5. Algoritmusok**


---

## Tárgymutató

- [2. Definíció és adatstruktúra](#2-definicio-es-adatstruktura)
- [3. z-normalizált euklideszi távolság](#3-z-normalizalt-euklideszi-tavolsag)
- [4. Motívum és anomália](#4-motivum-es-anomalia)
- [5. Algoritmusok](#5-algoritmusok)

---

## Hivatkozások

<a name="ref-1"></a>[1] STUMPY Documentation (2024). *STUMPY Basics Tutorial*. stumpy2024_webpage.


# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-24 | 1.1 | Újragenerálva -- ékezetek javítva (01-07 pipeline) |
