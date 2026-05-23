---
title: 1_MINDMAP.MD -- Matrix Profile: Alapok es Alkalmazasok
type: output
tags: [mindmap, matrixprofil]
het: 1
updated: 2026-05-22
status: DRAFT
---

# 1. Mindmap -- Matrix Profile: Alapok es Alkalmazasok

```mermaid
flowchart LR
  MP["Matrix Profile"]

  MP --> ALAP["MP Alapfogalmak"]
  ALAP --> TS["Idosor (Time Series, n hosszu)"]
  ALAP --> SUB["Reszsorozat (Subsequence, m hosszu)"]
  ALAP --> EDIST["Euklideszi tavolsag (z-normalizalt)"]
  ALAP --> DP["Tavolságprofil (Distance Profile)"]
  ALAP --> TMATCH["Trivialis egyezes (Trivial match)"]
  ALAP --> EZ["Kizarasi zona (Exclusion Zone, m/2)"]

  MP --> STRUCT["MP Struktura"]
  STRUCT --> PV["MP vektor P -- legkozelebbi tavolsag"]
  STRUCT --> IV["MP Index I -- legkozelebbi szomszed indexe"]

  MP --> ALGO["Alapveto Algoritmusok"]
  ALGO --> MASS["MASS -- FFT-alapu tavolsagprofil szamitas"]
  MASS --> SDP["FFT skalaris szorzat, O(n log n)"]
  ALGO --> STAMP["STAMP -- anytime, veletlen mintavetel"]
  ALGO --> STOMP["STOMP -- rendezett kereses, O(n^2)"]
  STOMP --> GPUSTOMP["[MSc] GPU-STOMP"]
  ALGO --> SCRIMP["[MSc] SCRIMP / SCRIMP++ -- interaktiv sebesseg"]
  ALGO --> STAMPI["[MSc] STAMPI / STOMPI -- streaming, inkrementalis"]

  MP --> VARIANTS["Variansok"]
  VARIANTS --> MSTAMP["[MSc] mSTAMP / mSTOMP -- multidimenzios MP"]
  VARIANTS --> STUMPY["STUMPY -- Python konyvtar"]

  MP --> APP["Fo Alkalmazasok"]
  APP --> MOTIF["Motivum kereses (Motif Discovery)"]
  APP --> DISCORD["Diszkord kereses (Anomalia detekcia)"]
  APP --> FLUSS["[MSc] Szemantikai szegmentacio (FLUSS)"]
  APP --> SHAPE["[MSc] Shapelet felfedezes"]
  APP --> CHAINS["[MSc] Idosor lancok (Time Series Chains)"]

  MP --> PROPS["Jellemzok es Elonyok"]
  PROPS --> EXACT["Egzakt -- nincs teves negatív"]
  PROPS --> PARAM["Parametermentes"]
  PROPS --> MEM["Helytakarékos -- O(n) memoria"]
  PROPS --> DET["Determinisztikus -- futaside kiszamithato"]
  PROPS --> SCALE["Skalazható -- 100M+ adatpont"]
```

# 2. Forras

- Generalta: `nlm query notebook ff49ac69-0750-4773-bd4d-42536e96be3f` (2026-05-22)
- NLM mindmap ID: `d74b759b-81dc-432d-9229-ccc13331ff89`
- Raw output: `forrasok/nlm_mindmap_raw.txt`

# Valtozasnaplo

- 2026-05-22 -- Letrehozva (05_mindmap_manager, NLM CLI query alapjan)
