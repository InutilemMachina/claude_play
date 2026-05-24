---
title: 1_MINDMAP.MD -- Matrix Profile
type: output
tags: [mindmap, sim]
het: 1
updated: 2026-05-23
status: DRAFT
---

# 1. Mindmap -- Matrix Profile

```mermaid
flowchart LR
  MP["Matrix Profile"]
  MP --> ALAP["Alapfogalmak"]
  ALAP --> TS["Idosor (Time Series)"]
  ALAP --> SUB["Reszsorozat (m hosszu)"]
  ALAP --> EZ["Kizarasi zona (m/4)"]
  ALAP --> PV["MP vektor P"]
  ALAP --> IV["MP Index I"]
  MP --> ALGO["Algoritmusok"]
  ALGO --> MASS["MASS (FFT, O(n log n))"]
  ALGO --> STAMP["STAMP (anytime)"]
  ALGO --> STOMP["STOMP (O(n^2))"]
  ALGO --> SCRIMP["[MSc] SCRIMP++"]
  MP --> APP["Alkalmazasok"]
  APP --> MOTIF["Motivum kereses"]
  APP --> DISCORD["Anomalia detekcia"]
  APP --> FLUSS["[MSc] FLUSS szegmentacio"]
```

# 2. Forras

- Generalta: `nlm chat` szimulacio (2026-05-23)
- Notebook: 6d6525ba-4804-4d78-b771-9bf1278e85e9
- Raw: `clean_sources/nlm_q1_raw.txt`

# Valtozasnaplo

- 2026-05-23 -- [SIM] Letrehozva (05_mindmap_manager szimulacio)
