---
title: 1_JEGYZET.MD -- Matrix Profile
type: output
het: 1
updated: 2026-05-23
status: DRAFT
notebook: 6d6525ba-4804-4d78-b771-9bf1278e85e9
---

# 1. Heti Jegyzet -- Matrix Profile

**Het:** 1. het | **Datum:** 2026-05-23 | **Statusz:** DRAFT

## Tanulasi celok

1. Megerteni a Matrix Profile matematikai definiciojat.
2. Azonositani a $P$ vektor es $I$ vektor szerepet.
3. Osszehasonlitani STAMP, STOMP es SCRIMP++ komplexitasat.
4. Felsorolni a fo alkalmazasi teruletek (motivum, diszkord, szegmentacio).


<!-- Q:1 -->
## 2. Atekindes es motivacio

A Matrix Profile (MP) egy idosor osszes reszsorozatparja kozotti tavolsagot tarolo vektor. Kizarolag a feltoltott forrasok alapjan: az MP egzakt, parameter-mentes es $O(n)$ memoriat igenyel. <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup>

> **💡 Lenyeg:** Az MP egyszerre kezeli a motivum-, diszkord- es szegmentacio-detekciiot anelkul, hogy elore meg kellene hatarozni a mintaszamot.

<!-- Q:2 -->
## 3. Alapfogalmak es MP-struktura

**Idosor** ($T$): $n$ hosszu valos szam-sorozat. **Reszsorozat** ($T_{i,m}$): $m$ hosszu ablak az $i$. poziciotol. **Kizarasi zona**: trivialis onegyezes megakadalyozasa. <sup>[[1]](#ref-1)</sup>

> **💡 Lenyeg:** A $P$ vektor minden reszsorozathoz a kizarasi zonan kivuli legkisebb tavolsagot tarolja.

> **🗺️ Fejezet osszegzes -- 3. Alapfogalmak**

<!-- Q:3 -->
## 4. Algoritmusok

**MASS** ($O(n \log n)$): FFT-alapu tavolsagprofil-szamitas. **STAMP**: veletlen sorrendu, anytime jelleggel. **STOMP**: rendezett, $O(n^2)$. <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>

> **💡 Lenyeg:** STOMP gyorsabb STAMP-nal, mert felhasznaalja az elozoleg szamolt tavolsagprofilokat.


> **🗺️ Fejezet osszegzes -- 4. Algoritmusok**

<!-- Q:4 -->
## 5. Alkalmazasok


> **💡 Lenyeg:** Egyetlen MP-szamitasbol motivum, diszkord es szegmentacio is kinyerheto.

> **🗺️ Fejezet osszegzes -- 5. Alkalmazasok**


---

## Targymutatoo

- [1. Heti Jegyzet -- Matrix Profile](#1-heti-jegyzet----matrix-profile)
  - [2. Atekindes es motivacio](#2-atekindes-es-motivacio)
  - [3. Alapfogalmak es MP-struktura](#3-alapfogalmak-es-mp-struktura)
  - [4. Algoritmusok](#4-algoritmusok)
  - [5. Alkalmazasok](#5-alkalmazasok)

---

## Hivatkozasok

<a name="ref-1"></a>[1] Yeh et al. (2016). *yeh2016_paper.pdf*.
<a name="ref-2"></a>[2] Yeh et al. (2018). *yeh2018_paper.pdf*.
<a name="ref-3"></a>[3] Zhu et al. (2016). *zhu2016_paper.pdf*.

# Valtozasnaplo

| Datum | Verzio | Leiras |
|-------|--------|--------|
| 2026-05-23 | 1.0 | [SIM] Letrehozva (01-07 pipeline szimulacio) |
