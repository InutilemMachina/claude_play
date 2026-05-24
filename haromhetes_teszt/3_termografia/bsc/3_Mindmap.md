---
title: 3_MINDMAP.MD -- Infravörös termográfia
type: output
het: 3
updated: 2026-05-24
status: DRAFT
notebook: 2af3a356-2a36-47f1-8adc-1da4bc44de72
---

# 3. Mindmap -- Infravörös termográfia

```mermaid
flowchart LR
  TERMO["Infravörös termográfia"]
  TERMO --> FIZIKA["Fizikai alapok"]
  FIZIKA --> STEFAN["Stefan-Boltzmann: W=εσT⁴"]
  FIZIKA --> EMISSZ["Emisszivitás ε ∈ [0,1]"]
  TERMO --> KAMERA["Hőkamera felépítése"]
  KAMERA --> OBJEKT["IR objektív (germánium)"]
  KAMERA --> BOLOM["Mikrobolométer (nem hűtött)"]
  TERMO --> MERESHIBAK["Mérési korlátok"]
  MERESHIBAK --> REFLEXIO["Reflexió (alacsony ε)"]
  MERESHIBAK --> ATMO["Atmoszférikus ablakok"]
  MERESHIBAK --> UVEG["Üveg: átlátszatlan >5 μm"]
  TERMO --> APP["Alkalmazások"]
  APP --> VILLAMOS["Villamos diagnosztika"]
  APP --> EPULET["Épületgépészet"]
  APP --> GEPESZET["Gépészeti PM"]
```


## Forrás

- Generálta: `nlm_query.py` (2026-05-24)
- Notebook: 2af3a356-2a36-47f1-8adc-1da4bc44de72
- Raw: `clean_sources/nlm_q1_raw.txt`

# Változásnapló

- 2026-05-24 -- 1.1: Újragenerálva -- ékezetek javítva (05_mindmap_manager)
