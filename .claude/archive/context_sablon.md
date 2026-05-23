---
title: CONTEXT_SABLON.MD — Tantárgy context sablon
type: meta
tags: [meta, sablon]
updated: 2026-05-21
description: Új tantárgynál másolandó sablon. Kitöltendő: alapadatok, tematika/pipeline státusz, célok, stílusirányelvek, NLM konfiguráció.
---
# CONTEXT.MD — TANTÁRGY SABLON
_Másold ide: [TantargyNeve]/_claude/context.md_

# 1. Alapadatok
- **Tantárgy neve:**
- **Szint:** BSc / MSc / mindkettő
- **Félév:** X hetes, heti X óra
- **Célcsoport:** (szak, év)

# 2. Tematika és pipeline státusz
| Hét | Téma | NLM notebook | Input | NLM01 | C00 | C01 | C02 | C03-C05 | C06 | C07 | C08 |
|-----|------|--------------|-------|-------|-----|-----|-----|---------|-----|-----|-----|
| 1 | | | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 2 | | | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 3 | | | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

_Státuszok: ❌ TODO · ⚙️ folyamatban · ✅ kész_

# 3. Célok
- BSc szint:
- MSc szint:

# 4. Stílusirányelvek
- Nyelv: magyar szöveg, kétnyelvű terminológia
- Prezentáció sablon: `templates/du_template.pptx`
- Kérdésbank: feleletválasztós A/B/C/D, SZINT:2-5

# 5. NLM notebook konfiguráció
- Notebook neve:
- Notebook URL:
- B1 Custom Instructions: beállítva ❌/✅

---

# KITÖLTÖTT PÉLDA — Műszaki Diagnosztika

> _Ez egy kitöltött minta. A saját context.md-t a fenti sablon alapján, ennek analógiájára készítsd el._

## 1. Alapadatok
- **Tantárgy neve:** Műszaki Diagnosztika
- **Szint:** BSc + MSc (kétszintű)
- **Félév:** 14 hetes, heti 2 × 90 perc (előadás + labor)
- **Célcsoport:** Gépészmérnök BSc/MSc, 3-4. év

## 2. Tematika és pipeline státusz
| Hét | Téma | NLM notebook | Input | NLM01 | C00 | C01 | C02 | C03-C05 | C06 | C07 | C08 |
|-----|------|--------------|-------|-------|-----|-----|-----|---------|-----|-----|-----|
| 1 | Hőkamerás diagnosztika | Termografia_NLM | ✅ | ✅ | ✅ | ✅ | ✅ | ⚙️ | ❌ | ❌ | ❌ |
| 2 | Termográfia mérési módszerek | Termografia_NLM | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 3 | Rezgésdiagnosztika | Rezges_NLM | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## 3. Célok
- BSc szint: Diagnosztikai módszerek felismerése, alapvető mérési elvek ismerete, tipikus hibamódok azonosítása.
- MSc szint: Mérési adatok kiértékelése, statisztikai módszerek alkalmazása, rendszerszintű diagnosztika tervezése.

## 4. Stílusirányelvek
- Nyelv: magyar szöveg, kétnyelvű terminológia (pl. "termogram / thermogram")
- Prezentáció sablon: `templates/du_template.pptx`
- Kérdésbank: feleletválasztós A/B/C/D, SZINT:2-5

## 5. NLM notebook konfiguráció
- Notebook neve: Termografia_NLM
- Notebook URL: https://notebooklm.google.com/notebook/...
- B1 Custom Instructions: beállítva ✅

# Változásjegyzék
- 2026-05-21 — YAML header és változásjegyzék hozzáadva
