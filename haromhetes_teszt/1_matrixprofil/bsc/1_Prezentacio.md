---
title: 1_PREZENTACIO.MD -- Matrix Profile
type: output
het: 1
updated: 2026-05-23
status: DRAFT
notebook: 6d6525ba-4804-4d78-b771-9bf1278e85e9
---

# 1. Prezentaciio -- Matrix Profile

**Het:** 1. het | **Datum:** 2026-05-23 | **Statusz:** DRAFT

## 1. dia -- Bevezetes: Mi a Matrix Profile?

Az idosor osszes reszsorozat-parjanak z-normalizalt tavolsaga.

- Egzakt
- Parameter-mentes
- $O(n)$ memoria

---

## 2. dia -- Alapfogalmak: Reszsorozat es tavolsag

- **Reszsorozat** $T_{i,m}$: $m$ hosszu ablak
- **Kizarasi zona**: trivialis egyezes kizarasa
- **MASS**: FFT-alapu tavolsagprofil $O(n\log n)$

---

## 3. dia -- MP Struktura: A $P$ vektor es $I$ vektor

$$P[i] = \min_{j \notin EZ(i)} d(T_{i,m}, T_{j,m})$$

- Alacsony ertek: motivum
- Magas ertek: diszkord

---

## 4. dia -- Algoritmusok: STAMP vs STOMP

| | STAMP | STOMP |
|---|---|---|
| Jelleg | anytime | rendezett |
| Komplexitas | $O(n^2)$ | $O(n^2)$ |
| Ido | lassabb | gyorsabb |

---


- Inkrementalis frissites
- Alkalmas streaming adatokra
- Valoszinusegi kozelites

---

## 6. dia -- Alkalmazasok: Motivum, Diszkord, Szegmentacio

- **Motivum**: ismetlodo minta (pl. EKG-ciklus)
- **Diszkord**: anomalia

---

## 7. dia -- Osszefoglalas: Tanulsagok

- Matrix Profile = 1 szamitasbol 3 feladat
- Python: STUMPY konyvtar
- Skala: 100M+ adatpont

---


# Valtozasnaplo

| Datum | Verzio | Leiras |
|-------|--------|--------|
| 2026-05-23 | 1.0 | [SIM] Letrehozva (08_presentation_maker szimulacio) |
