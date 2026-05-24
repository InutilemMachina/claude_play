---
title: 2_MINDMAP.MD -- DFT és FFT
type: output
het: 2
updated: 2026-05-24
status: DRAFT
notebook: 9447f8a8-d261-4522-8cc6-862befe1aabe
---

# 2. Mindmap -- DFT és FFT

```mermaid
flowchart LR
  DFT["DFT és FFT"]
  DFT --> DEFINICIO["Definíció"]
  DEFINICIO --> KEPLET["X̂(k) = Σ X(j)W_N^jk"]
  DEFINICIO --> MATRIX["Fourier-mátrix W_N"]
  DEFINICIO --> IDFT["Inverz DFT"]
  DFT --> FFT["FFT algoritmusok"]
  FFT --> CT["Cooley-Tukey (1965)"]
  FFT --> KOMPLEX["O(N²) → O(N log N)"]
  DFT --> ALKAL["Alkalmazások"]
  ALKAL --> JELFELDOLG["Jelfeldolgozás (MP3, modem)"]
  ALKAL --> KEPFELDOLG["Képfeldolgozás (MRI)"]
  DFT --> TULAJD["Tulajdonságok"]
```


## Forrás

- Generálta: `nlm_query.py` (2026-05-24)
- Notebook: 9447f8a8-d261-4522-8cc6-862befe1aabe
- Raw: `clean_sources/nlm_q1_raw.txt`

# Változásnapló

- 2026-05-24 -- 1.1: Újragenerálva -- ékezetek javítva (05_mindmap_manager)
