---
title: 2_PREZENTACIO.MD -- Diszkret Fourier-transzformacio
type: output
het: 2
updated: 2026-05-23
status: DRAFT
notebook: 231a232e-6620-41a0-b30b-03a8a6c187b8
---

# 2. Prezentaciio -- Diszkret Fourier-transzformacio

**Het:** 2. het | **Datum:** 2026-05-23 | **Statusz:** DRAFT

## 1. dia -- Bevezetes: Miert fontos a DFT?

Az idotartomany-jelet frekvenciatartomanyba kepezi le.

- Visszafordithato (IDFT)
- Alapja minden digitalis jelfeldolgozasnak

---

## 2. dia -- Matematika: A DFT keplete

$$X[k] = \sum_{n=0}^{N-1} x[n] e^{-j2\pi kn/N}$$

$k$: frekvenciaindex, $N$: mintaszam

---

## 3. dia -- Spektrum: Amplitudo es fazis

- $|X[k]|$: amplitudo
- $\angle X[k]$: fazis
- $\Delta f = f_s / N$: frekkvenciafelbontas

---

## 4. dia -- Nyquist es Aliasing: Mintaveteli teorema

- $f_{Nyquist} = f_s / 2$
- Aliasing: $f > f_{Nyquist}$ komponensek teves ertelmezese
- Megoldas: anti-aliasing szuro

---

## 5. dia -- FFT: Cooley-Tukey algoritmus

- DFT: $O(N^2)$
- FFT: $O(N \log N)$
- $N=1024$: ~100x gyorsabb

---


- Paros/paratlan indexek elvalasztasa
- Rekurziv kozelites
- Pillango (butterfly) muvelet

---

## 7. dia -- Alkalmazasok: Rezges, audio, szures

- Rezgesdiagnosztika: forgogepek hibafrekkvenciaia
- Audio: hangszinkez

---


# Valtozasnaplo

| Datum | Verzio | Leiras |
|-------|--------|--------|
| 2026-05-23 | 1.0 | [SIM] Letrehozva (08_presentation_maker szimulacio) |
