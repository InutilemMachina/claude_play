---
title: 3_MINDMAP.MD -- Termografia
type: output
tags: [mindmap, sim]
het: 3
updated: 2026-05-23
status: DRAFT
---

# 3. Mindmap -- Termografia

```mermaid
flowchart LR
  TERMO["Termografia"]
  TERMO --> FIZIKA["Fizikai alapok"]
  FIZIKA --> STEFAN["Stefan-Boltzmann torveny"]
  FIZIKA --> EMISSZ["Emisszivitas (epsilon, 0-1)"]
  FIZIKA --> PLANK["[MSc] Planck-sugarzasi torveny"]
  TERMO --> KAMERA["Hokamera felepitese"]
  KAMERA --> DETEKTOR["IR detektor"]
  DETEKTOR --> BOLOM["Mikrobolometer (nem hutott)"]
  DETEKTOR --> COOLED["[MSc] Hutott detektor (InSb, MCT)"]
  KAMERA --> OBJEKTIV["Germaniumulens"]
  TERMO --> APP["Alkalmazasok"]
  APP --> VILLAMOS["Villamos diagnosztika"]
  APP --> EPULET["Epuletdiagnosztika"]
  APP --> GEPHIBA["Gephiba-detekciio"]
  APP --> PPM["[MSc] Prevencio PM rendszerben"]
```

# 2. Forras

- Generalta: `nlm chat` szimulacio (2026-05-23)
- Notebook: 21de071f-0bf0-4c31-b4c2-e24f9d6d542a
- Raw: `clean_sources/nlm_q1_raw.txt`

# Valtozasnaplo

- 2026-05-23 -- [SIM] Letrehozva (05_mindmap_manager szimulacio)
