---
title: CONTEXT.MD — Háromhetes teszt
type: meta
tags: [meta, teszt]
updated: 2026-05-23
description: 3 hetes pipeline-teszt. Session elején Claude olvassa be. Tartalmazza a pipeline státuszt és blokkolókat.
---
# CONTEXT.MD — Háromhetes Teszt

_Frissítve: 2026-05-23 -- [SIM] teljes pipeline lefutott_

# 1. Alapadatok

- **Tantárgy neve:** Háromhetes pipeline-teszt
- **Szint:** BSc + MSc (kétszintű)
- **Félév:** 3 hetes teszt, heti 1 téma
- **Célcsoport:** Gépészmérnök BSc/MSc (tesztkörnyezet)
- **Mappa:** `haromhetes_teszt/` (gyökér)

## 1.1. Célok

- BSc szint: Pipeline-lépések end-to-end tesztelése mindhárom témán; egységes outputformátum validálása.
- MSc szint: Kétszintű szűrés (10_bsc_filter) és kérdésbank-differenciálás tesztelése.

# 2. Pipeline státusz

A fejléc számok pipeline lépésszámok (`00b` = NLM notebook setup, `01` = forrásfeldolgozás, `02` = kivonatolás, `03-05` = excerpt/szójegyzet/mindmap, `06-07` = jegyzetek összeállítása, `08` = prezentáció, `09` = kérdésbank, `10` = BSc-szűrő).

| Hét | Téma | NLM notebook | 00b | 01 | 02 | 03-05 | 06-07 | 08 | 09 | 10 |
|-----|------|--------------|-----|----|----|-------|-------|----|----|-----|
| 1 | Matrix Profile | MatrixProfil_teszt | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 | Diszkrét Fourier-transzformáció | DFT_teszt | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3 | Termográfia | Termografia_teszt | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

_Státuszok: ❌ TODO · ⚙️ folyamatban · ✅ kész_

# 3. NLM notebook konfiguráció

| Hét | Notebook neve | Notebook ID | Prompt B |
|-----|--------------|-------------|----------|
| 1 | MatrixProfil_teszt | 6d6525ba-4804-4d78-b771-9bf1278e85e9 | ✅ |
| 2 | DFT_teszt | 231a232e-6620-41a0-b30b-03a8a6c187b8 | ✅ |
| 3 | Termografia_teszt | 21de071f-0bf0-4c31-b4c2-e24f9d6d542a | ✅ |

# 4. Mappastruktúra

```
haromhetes_teszt/
├── context.md              (ez a fájl)
├── 1_matrixprofil/
│   ├── raw_sources/        (junction → test_sources/matrixprofil/forrasok/)
│   ├── clean_sources/
│   └── bsc/
├── 2_dft/
│   ├── raw_sources/        (junction → test_sources/dft/forrasok/)
│   ├── clean_sources/
│   └── bsc/
└── 3_termografia/
    ├── raw_sources/        (junction → test_sources/termografia/forrasok/)
    ├── clean_sources/
    └── bsc/
```

# 5. Blokkolók

- du_template.pptx hiányzik (bypass él).

# 6. Stílusirányelvek

- Nyelv: magyar szöveg, kétnyelvű terminológia
- Prezentáció sablon: `templates/du_template.pptx`
- Kérdésbank: feleletválasztós A/B/C/D, SZINT:2-5

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-23 | 1.0 | Létrehozva: 3 hetes pipeline-teszt init |
| 2026-05-23 | 2.0 | project_status.md beolvasztva; mappastruktúra frissítve; NLM ID-k hozzáadva |
