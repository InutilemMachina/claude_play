---
title: 2_MINDMAP.MD -- Diszkret Fourier-transzformacio
type: output
tags: [mindmap, sim]
het: 2
updated: 2026-05-23
status: DRAFT
---

# 2. Mindmap -- Diszkret Fourier-transzformacio

```mermaid
flowchart LR
  DFT["Diszkret Fourier-transzformacio"]
  DFT --> ALAP["Alapfogalmak"]
  ALAP --> SPEKTRUM["Frekvenciaspektrum"]
  ALAP --> AMPLITUD["Amplitudo es fazis"]
  ALAP --> NYQUIST["Nyquist-frekvencia (fs/2)"]
  ALAP --> ALIASING["Aliasing"]
  ALAP --> ABLAK["Ablakolas (Windowing)"]
  DFT --> MAT["Matematika"]
  MAT --> KEPLET["X[k] = sum x[n] e^-j2pi_kn/N"]
  MAT --> IDFT["Inverz DFT"]
  MAT --> PARSEVAL["[MSc] Parseval-tetel"]
  DFT --> FFT["Gyors Fourier-transzformacio (FFT)"]
  FFT --> COOLEY["Cooley-Tukey O(N log N)"]
  FFT --> RADIX2["[MSc] Radix-2 DIT/DIF"]
  DFT --> APP["Alkalmazasok"]
  APP --> VIBR["Rezgesdiagnosztika"]
  APP --> AUDIO["Audio-jelfeldolgozas"]
  APP --> FILTER["[MSc] Digitalis szures spektrumban"]
```

# 2. Forras

- Generalta: `nlm chat` szimulacio (2026-05-23)
- Notebook: 231a232e-6620-41a0-b30b-03a8a6c187b8
- Raw: `clean_sources/nlm_q1_raw.txt`

# Valtozasnaplo

- 2026-05-23 -- [SIM] Letrehozva (05_mindmap_manager szimulacio)
