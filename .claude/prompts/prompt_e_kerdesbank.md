---
title: Prompt E -- NLM CLI Kérdésbank query
type: prompt
tags: [meta, prompt]
pipeline_step: 13_question_bank_collector
updated: 2026-05-29
---

# Prompt E -- NLM CLI Kérdésbank query

**Hova:** `nlm query notebook $NB $promptE --json`

**Mikor:** 13_question_bank_collector lépésben.

## ASCII prompt (PowerShell heredoc)

```powershell
$promptE = @'
Generalj 10 feleletvalasztos kerdest a forrasok alapjan, novekvo nehezsegi sorrendben.
Minden kerdeshez:
- Kerdes szovege (**K[N]** SZINT:[2-5] formaban, ahol SZINT 2=alap, 3=alkalmazas, 4=melyebb elemzes, 5=kutatas)
- A) B) C) D) valaszlehetosegek
- Helyes valasz betuje (**Helyes:** X)
- Forras-hivatkozas (*Forras: fajlnev.pdf: oldal*)
- MSc szintu (SZINT 4-5) kerdeseket <!-- MSc --> ... <!-- /MSc --> blokkba foglald.
'@
$NB = "<notebook_id>"
nlm query notebook $NB $promptE --json | Out-File 3_raw_outputs/nlm_qquiz_raw.txt -Encoding utf8
```
