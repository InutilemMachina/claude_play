---
title: 1_PREZENTACIO.MD -- Matrix Profile
type: output
het: 1
updated: 2026-05-24
status: DRAFT
notebook: 013ea69e-ee02-4a13-9389-7f46d7fb37ae
---

# 1. Prezentáció -- Matrix Profile

**Hét:** 1. hét | **Dátum:** 2026-05-24 | **Státusz:** DRAFT

## 1. dia -- Mi a Matrix Profile?

Minden részsorozat-pár legjobb szomszédjának távolsága -- egyetlen vektorban.

- Távolságvektor: $O(n)$ méret
- z-normalizált euklideszi távolság
- Kísérő Profile Index: szomszéd indeksei

---

## 2. dia -- Motívum és anomália

A Matrix Profile két alapvető bányászati művelete:

| Érték | Interpretáció | Alkalmazás |
|:------|:--------------|:-----------|
| Globális **minimum** | Legismétlődőbb minta | Motívumkeresés |
| Globális **maximum** | Legszokatlanabb szakasz | Anomáliadetektálás |

---

## 3. dia -- z-normalizálás: miért szükséges?

Amplitúdófüggetlen összehasonlítás:

$$\hat{T}_i = \frac{T_i - \mu}{\sigma}$$

- Azonos alakú, különböző léptékű részsorozatok → hasonlónak ítélve ✓
- Nyers euklideszi távolság: amplitúdókülönbség dominál ✗

---

## 4. dia -- STOMP vs. Brute Force

| Algoritmus | Időkomplexitás | Memória |
|:-----------|:---------------|:--------|
| Brute Force | $O(n^2 m)$ | $O(n^2)$ |
| **STOMP** | $O(n^2)$ | $O(n)$ |

5 év adat brute force-szal: **4,4 év** számítási idő, **11,1 PB** memória.

---


- Numba JIT + Dask: CPU/GPU párhuzamosítás
- Akár 256 CPU mag vagy több GPU
- SCRUMP: közelítő, sebesség-kritikus esetekre

---

## 6. dia -- Alkalmazások

- **Motívumkeresés:** ismétlődő gépviselkedés-minták
- **Anomáliadetektálás:** ritkán előforduló hibaminták

---

## 7. dia -- Összefoglalás

1. Matrix Profile = távolságvektor + Profile Index
2. z-normalizálás → amplitúdófüggetlen összehasonlítás
3. STOMP: $O(n^2)$, egzakt, párhuzamosítható (STUMPY)
4. Min → motívum; Max → anomália


# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-24 | 1.1 | Újragenerálva -- ékezetek javítva (08_presentation_maker) |
