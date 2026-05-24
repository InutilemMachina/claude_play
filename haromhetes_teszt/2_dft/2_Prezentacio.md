---
title: 2_PREZENTACIO.MD -- DFT és FFT
type: output
het: 2
updated: 2026-05-24
status: DRAFT
notebook: 9447f8a8-d261-4522-8cc6-862befe1aabe
---

# 2. Prezentáció -- DFT és FFT

**Hét:** 2. hét | **Dátum:** 2026-05-24 | **Státusz:** DRAFT

## 1. dia -- DFT: idő- és frekvenciatartomány

Az idő→frekvencia transzformáció alapja:

$$\hat{X}(k) = \sum_{j=0}^{N-1} X(j) \cdot W_N^{jk}, \quad W_N = e^{2\pi i/N}$$

- $N$ komplex szám → $N$ frekvenciakomponens
- Mátrixszorzatként: $\hat{X} = W_N \cdot X$

---

## 2. dia -- FFT: az algoritmikus forradalom

Közvetlen DFT vs. FFT:

| Módszer | Műveletek |
|:--------|:----------|
| Közvetlen DFT | $N^2$ |
| **FFT (Cooley-Tukey)** | $N \log N$ |

$N = 10^6$: $10^{12}$ → $2 \cdot 10^7$ művelet (**50 000-szeres gyorsulás**).

---

## 3. dia -- Cooley-Tukey: rekurzív felbontás

$N$-pontos DFT → két $N/2$-pontos DFT:

$$\hat{X}(k) = \hat{X}_{\text{páros}}(k) + W_N^k \cdot \hat{X}_{\text{páratlan}}(k)$$

- "Oszd meg és uralkodj" elv
- **[MSc]** Butterfly-diagram vizualizálja az adatfolyamot

---

## 4. dia -- Alkalmazások: mérnöki területek

| Terület | Példa |
|:--------|:------|
| Jelanalízis | Rezgésdiagnosztika, spektrumelemzés |
| Hang/kép | MP3 tömörítés, MRI rekonstrukció |
| Geofizika | Szeizmológia, nukleáris teszt-detektálás |
| **[MSc]** Csillagászat | LIGO gravitációs hullámok, interferometria |

---

## 5. dia -- [MSc] Konvolúciós tétel

Időtartomány konvolúció $\leftrightarrow$ frekvenciatartomány szorzat:

$$(f * g)(t) \xrightarrow{\mathcal{F}} F(\omega) \cdot G(\omega)$$

**Szűrés $O(N^2)$ helyett $O(N \log N)$-re csökkentve.**

---

## 6. dia -- Összefoglalás

1. DFT: $N$ pont → $N$ frekvenciakomponens; $O(N^2)$
2. FFT: ugyanaz, $O(N \log N)$; Cooley-Tukey 1965
3. IDFT: visszatranszformálás; számítása = DFT($\hat{X}(-k)$)
4. **[MSc]** Konvolúciós tétel → gyors digitális szűrés alapja


# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-24 | 1.1 | Újragenerálva -- ékezetek javítva (08_presentation_maker) |
