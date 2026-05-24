---
title: 2_JEGYZET.MD -- DFT és FFT
type: output
het: 2
updated: 2026-05-24
status: DRAFT
notebook: 9447f8a8-d261-4522-8cc6-862befe1aabe
---

# 2. Heti Jegyzet -- DFT és FFT

**Hét:** 2. hét | **Dátum:** 2026-05-24 | **Státusz:** DRAFT

## Tanulási célok

1. Leírni a DFT matematikai definícióját és a Fourier-mátrix kapcsolatát.
2. Megmagyarázni az FFT számítási előnyét a közvetlen DFT-vel szemben.
3. Vázolni a Cooley-Tukey rekurzív felbontás elvét.
4. Felsorolni a DFT/FFT legalább 3 mérnöki alkalmazási területét.
5. [MSc] Bemutatni a konvolúciós tétel és a digitális szűrés kapcsolatát.


<!-- Q:1 -->
## 2. DFT definíciója és Fourier-mátrix

A DFT $N$ hosszú diszkrét jelet frekvenciatartományba transzformál: $\hat{X}(k) = \sum_{j=0}^{N-1} X(j) W_N^{jk}$, ahol $W_N = e^{2\pi i/N}$. [1]

Mátrix formában: $\hat{X} = W_N \cdot X$, ahol $W_N$ az egységgyökök unitér Fourier-mátrixa. Az IDFT: $X(j) = \frac{1}{N}\sum_{k=0}^{N-1} \hat{X}(k) W_N^{-jk}$. [1]

> **💡 Lényeg:** Az IDFT számítása lényegében megegyezik a DFT-ével (csak $W_N^{-jk}$ és $1/N$ faktorral). Ugyanaz az implementáció mindkét irányban használható.

<!-- Q:2 -->
## 3. FFT és Cooley-Tukey

Az FFT $O(N^2)$-ről $O(N \log N)$-re csökkenti a DFT számítási igényét. A Cooley-Tukey (1965) algoritmus $N = N_1 N_2$ esetén az $N$-pontos DFT-t két $N/2$-pontos DFT-re bontja rekurzívan. [1]

> **💡 Lényeg:** Az FFT nem egy új transzformáció -- ugyanolyan eredményt ad, mint a közvetlen DFT. Csak a számítást csinálja gyorsabban.

> **[MSc]** A butterfly-diagram az FFT adatfolyam-grafikonja: megmutatja, mely elemeket kell összevonni az egyes rekurzív lépésekben. [1]

> **🗺️ Fejezet összegzés -- 3. FFT és Cooley-Tukey**

<!-- Q:3 -->
## 4. Alkalmazások

A DFT/FFT nélkülözhetetlen a következő területeken [1]:

- **Jelfeldolgozás**: rezgésdiagnosztika, modemek, MP3 kódolás
- **Képfeldolgozás**: MRI rekonstrukció, mintázatfelismerés
- **Geofizika**: szeizmológiai idősorok, nukleáris tesztek detektálása
- **[MSc]** Csillagászat: LIGO gravitációs hullámok, aszteroida-pályák interpolációja

> **💡 Lényeg:** A digitális jelfeldolgozás legtöbb ága közvetve az FFT hatékonyságára épül -- nélküle a modern kommunikáció és orvosi képalkotás nem lenne megvalósítható.

> **🗺️ Fejezet összegzés -- 4. Alkalmazások**

<!-- Q:4 -->
## 5. [MSc] Konvolúciós tétel

Időtartomány konvolúció $\leftrightarrow$ frekvenciatartomány szorzat: $(f * g)(t) \xrightarrow{\mathcal{F}} F(\omega) \cdot G(\omega)$. [1]

Ez lehetővé teszi a digitális szűrést $O(N^2)$ helyett $O(N \log N)$-nel: FFT → szorzás → IFFT.

> **💡 Lényeg:** A konvolúciós tétel az oka, hogy az FFT a digitális szűrés (és így a rezgésdiagnosztika, audiofeldolgozás, képszűrés) alapeszközévé vált.

> **🗺️ Fejezet összegzés -- 5. Konvolúciós tétel**


---

## Tárgymutató

- [2. DFT definíciója és Fourier-mátrix](#2-dft-definicioja-es-fourier-matrix)
- [3. FFT és Cooley-Tukey](#3-fft-es-cooley-tukey)
- [4. Alkalmazások](#4-alkalmazasok)
- [5. Konvolúciós tétel](#5-konvolucios-tetel)

---

## Hivatkozások

<a name="ref-1"></a>[1] Rockmore, D. N. (1999). "The FFT -- An Algorithm the Whole Family Can Use." *Computing in Science & Engineering*, 1(1), 24--30. rockmore1999_article.pdf.


# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-24 | 1.1 | Újragenerálva -- ékezetek javítva (01-07 pipeline) |
