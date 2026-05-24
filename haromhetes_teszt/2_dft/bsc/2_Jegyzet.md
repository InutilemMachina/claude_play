---
title: 2_JEGYZET.MD -- Diszkret Fourier-transzformacio
type: output
het: 2
updated: 2026-05-23
status: DRAFT
notebook: 231a232e-6620-41a0-b30b-03a8a6c187b8
---

# 2. Heti Jegyzet -- Diszkret Fourier-transzformacio

**Het:** 2. het | **Datum:** 2026-05-23 | **Statusz:** DRAFT

## Tanulasi celok

1. Megerteni a DFT matematikai definiciojat es a $X[k]$ komplex ertek fizikai jelenteset.
2. Meghatározni a Nyquist-frekvenciat es magyarazni az aliasing jelenseget.
3. Osszehasonlitani a DFT es FFT szamitasi komplexitasat.
4. Alkalmazni a DFT-t rezgesdiagnosztikai feladata megoldasara.


<!-- Q:1 -->
## 2. Atekindes es motivacio

A Diszkret Fourier-transzformacio (DFT) egy $N$ hosszu jelet a frekvenciatartomanyba kepez le. Kizarolag a feltoltott forrasok szerint: a DFT az idosor es frekvenciasor kozott bijektiv kapcsolatot teremt. <sup>[[1]](#ref-1)</sup>

> **💡 Lenyeg:** A DFT visszafordithato: az IDFT az eredeti jelet allitja vissza pontosan.

<!-- Q:2 -->
## 3. Matematikai definicio

$$X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j2\pi kn/N}, \quad k=0,1,\ldots,N-1$$

A spektrum $N$ komplex erteket tartalmaz. <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>

> **💡 Lenyeg:** Az $X[k]$ ertek amplitudoja es fazisa megadja a $k \cdot \Delta f$ frekvencian levo komponenst.

> **🗺️ Fejezet osszegzes -- 3. Matematikai definicio**

<!-- Q:3 -->
## 4. FFT algoritmus

A **Cooley-Tukey** FFT $O(N \log N)$ komplexitasal hajtja vegre a DFT-t divide-and-conquer elvvel. $N = 2^p$ eseten optimalis. <sup>[[3]](#ref-3)</sup>

> **💡 Lenyeg:** $N = 1024$ eset: DFT $\approx 10^6$ muvelet, FFT $\approx 10^4$ -- 100x gyorsabb.


> **🗺️ Fejezet osszegzes -- 4. FFT algoritmus**

<!-- Q:4 -->
## 5. Alkalmazasok

**Rezgesdiagnosztika**: forgogepek hibafrekkvenciainak azonositasa. **Audio**: hangszinkezeeles, kodolas. <sup>[[2]](#ref-2)</sup>

> **💡 Lenyeg:** A spektrum csuccsai a dominans frekkvencia-komponensekre mutatnak; a sidebandok modulaciora utalnak.


> **🗺️ Fejezet osszegzes -- 5. Alkalmazasok**


---

## Targymutatoo

- [2. Heti Jegyzet -- Diszkret Fourier-transzformacio](#2-heti-jegyzet----diszkret-fourier-transzformacio)
  - [2. Atekindes es motivacio](#2-atekindes-es-motivacio)
  - [3. Matematikai definicio](#3-matematikai-definicio)
  - [4. FFT algoritmus](#4-fft-algoritmus)
  - [5. Alkalmazasok](#5-alkalmazasok)

---

## Hivatkozasok

<a name="ref-1"></a>[1] Ahrens (2020). *ahrens2020_article.pdf*.
<a name="ref-2"></a>[2] Barszcz (2019). *barszcz2019_chapter.pdf*.
<a name="ref-3"></a>[3] Gentleman (1966). *gentleman1966_article.pdf*.
<a name="ref-4"></a>[4] Lerch (2012). *lerch2012_book.pdf*.
<a name="ref-5"></a>[5] Rockmore (1999). *rockmore1999_article.pdf*.

# Valtozasnaplo

| Datum | Verzio | Leiras |
|-------|--------|--------|
| 2026-05-23 | 1.0 | [SIM] Letrehozva (01-07 pipeline szimulacio) |
