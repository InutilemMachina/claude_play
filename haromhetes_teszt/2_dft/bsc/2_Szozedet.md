---
title: 2_SZOZEDET.MD -- DFT és FFT
type: output
het: 2
updated: 2026-05-24
status: DRAFT
---

# 2. Szójegyzék -- DFT és FFT

**Hét:** 2. hét | **Dátum:** 2026-05-24 | **Státusz:** DRAFT

| Magyar terminus | Angol terminus | Definíció | Szint |
|:----------------|:---------------|:----------|:------|
| *Diszkrét Fourier-transzformáció* | *Discrete Fourier Transform (DFT)* | $N$ hosszú komplex vektort frekvenciatartományba képez: $\hat{X}(k)=\sum_{j=0}^{N-1}X(j)W_N^{jk}$. | BSc |
| *Gyors Fourier-transzformáció* | *Fast Fourier Transform (FFT)* | A DFT hatékony számítási algoritmusa; $O(N^2)$ helyett $O(N \log N)$ művelet. | BSc |
| *Fourier-mátrix* | *Fourier matrix* | $W_N = \exp(2\pi i/N)$ gyök egységei által alkotott unitér mátrix; DFT = $W_N \cdot X$. | BSc |
| *inverz DFT* | *IDFT* | $X(j) = \frac{1}{N}\sum_{k=0}^{N-1}\hat{X}(k)W_N^{-jk}$; frekvencia→idő visszatranszformálás. | BSc |
| *Cooley-Tukey algoritmus* | *Cooley-Tukey algorithm* | Az FFT legismertebb változata; $N = N_1 N_2$ felbontással rekurzív 2D DFT-vé alakítja az 1D DFT-t. | MSc |
| *butterfly-diagram* | *butterfly diagram* | Az FFT adatfolyam-grafikonja; jelzi, hogy mely elemeket kell összevonni az egyes lépésekben. | MSc |
| *spektrális szivárgás* | *spectral leakage* | Nem egész frekvenciánál megjelenő energiaszóródás; ablakfüggvényekkel csökkenthető. | MSc |
| *konvolúciós tétel* | *convolution theorem* | Időtartomány konvolúciója $\leftrightarrow$ frekvenciatartomány szorzat; $O(N^2)$ → $O(N \log N)$. | MSc |

## Irodalomjegyzék

[1] Rockmore, D. N. (1999). "The FFT -- An Algorithm the Whole Family Can Use." *Computing in Science & Engineering*, 1(1), 24--30. rockmore1999_article.pdf.

# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-24 | 1.1 | Újragenerálva -- ékezetek javítva (04_citations_maker) |
