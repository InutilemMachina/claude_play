---
title: 1_MINDMAP.MD -- Matrix Profile
type: output
het: 1
updated: 2026-05-24
status: DRAFT
notebook: 013ea69e-ee02-4a13-9389-7f46d7fb37ae
---

# 1. Mindmap -- Matrix Profile

```mermaid
flowchart LR
  MP["Matrix Profile"]
  MP --> DEF["Definíció"]
  DEF --> VECT["Távolságvektor O(n)"]
  DEF --> IDX["Profile Index"]
  DEF --> ZNORM["z-normalizált euklideszi távolság"]
  MP --> ALGO["Algoritmusok"]
  ALGO --> STOMP["STOMP -- egzakt O(n²)"]
  ALGO --> SCRUMP["SCRUMP -- közelítő"]
  ALGO --> BF["[MSc] Brute Force O(n²m)"]
  MP --> MUVELET["Műveletek"]
  MUVELET --> MOTIV["Motívumkeresés (min)"]
  MUVELET --> ANOM["Anomáliadetektálás (max)"]
  MUVELET --> SZEGM["[MSc] Szemantikus szegmentáció"]
  MP --> IMPL["Implementáció"]
  IMPL --> STUMPY["STUMPY (Python)"]
  IMPL --> GPU["[MSc] GPU/Dask párhuzamosítás"]
```


## Forrás

- Generálta: `nlm_query.py` (2026-05-24)
- Notebook: 013ea69e-ee02-4a13-9389-7f46d7fb37ae
- Raw: `clean_sources/nlm_q1_raw.txt`

# Változásnapló

- 2026-05-24 -- 1.1: Újragenerálva -- ékezetek javítva (05_mindmap_manager)
