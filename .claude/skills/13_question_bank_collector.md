---
name: 13_question_bank_collector
title: 13_QUESTION_BANK_COLLECTOR -- Question Bank Collector
type: skill
tags: [meta, skill]
status: active
version: 2.0
updated: 2026-05-26
description: NLM-query alapú kérdésbank generálás. N_Kerdesek.md feleletválasztós kérdések BSc/MSc szintezéssel. Pipeline 13. lépése.
---

# 13_QUESTION_BANK_COLLECTOR

## 1. Cél

Az NLM notebookból tematikus, feleletválasztós kérdéseket generál (`N_Kerdesek.md`) a mindmap csomópontjai alapján.

## 2. Bemenetek

- NLM notebook ID (02_nlm_notebook_setup kimenet)
- `4_wip_outputs/N_Mindmap.md` -- BSc/MSc határ meghatározásához

## 3. Eljárás

### 3.1. NLM lekérdezés (preferált)

Az NLM forrásokból citált, reprodukálható kérdéseket generál. Prompt minta:

```powershell
$qquiz = "Generalj N feleletvalasztos kerdest a forrasok alapjan, novekvo nehezsegi sorrendben. Minden kerdeshez: kerdes szovege, A/B/C/D valaszlehetosegek, helyes valasz betuje, es forras-hivatkozas (fajlnev.pdf: oldal)."
nlm query notebook $NB $qquiz --json | Out-File 3_raw_outputs/nlm_qquiz_raw.txt -Encoding utf8
```

### 3.2. Kérdés formátum

```markdown
**K[N]** SZINT:[2-5]
[Kérdés szövege?]
A) ...
B) ...
C) ...
D) ...
**Helyes:** [betű]
*Forrás: [fajlnev.pdf: oldal]*
```

### 3.3. Szintezés

| SZINT | Típus | Célközönség |
|-------|-------|-------------|
| 2 | Definíció, alapfogalom | BSc |
| 3 | Összefüggés, alkalmazás | BSc |
| 4 | Mélyebb elemzés | MSc |
| 5 | Kutatási szint, modell | MSc |

MSc kérdések: `<!-- MSc -->` blokkon belül -- `14_bsc_filter` kihagyja.

### 3.4. Mennyiség

Min. 4 BSc kérdés + min. 2 MSc kérdés hetente.

## 4. Kimenetek

- `4_wip_outputs/N_Kerdesek.md` -- kérdésbank (draft)
- `3_raw_outputs/nlm_qquiz_raw.txt` -- NLM nyers output

## 5. Ellenőrzés

- [ ] Legalább 4 BSc + 2 MSc kérdés
- [ ] Minden kérdéshez forrás-hivatkozás
- [ ] MSc kérdések `<!-- MSc -->` blokkban
- [ ] Kérdések szintjei egyenletesen elosztva (2-3-4-5)
- [ ] 😎 **MSc/BSc határ manuális review:** a `<!-- MSc -->` blokkokat és `SZINT` mezőket manuálisan kell kitölteni; a pipeline nem dönt automatikusan

## 6. Hibakezelés

- Tünet: generált kérdések forrás-hivatkozás nélküliek
- Gyökérok: Prompt B nem aktív, vagy a query nem kért hivatkozásokat
- Megoldás: Prompt B ellenőrzés; a query szövegébe expliciten belefoglalva legyen a hivatkozáskérés

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [04_nlm_query_runner.md](04_nlm_query_runner.md) -- NLM CLI használat
- [14_bsc_filter.md](14_bsc_filter.md) -- MSc kérdések szűrése

## 8. Visszajelzések

- 💬 NOTE: Az eddigi teszten a kérdésbank Claude-feladatként (`N_Jegyzet.md` alapján) lett generálva -- nem NLM-queryből. Ez nem reprodukálható és nem auditálható. A §3.1-ben leírt NLM-alapú módszer a következő iterációban tesztelendő.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-26 | 2.0 | Overhaul: template-alapú átírás; NLM-alapú workflow §3.1; §8 Visszajelzések; lépésszám javítva (09→13) |
| 2026-05-21 | 1.0 | Létrehozva |
