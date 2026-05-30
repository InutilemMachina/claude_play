---
title: Prompt D -- NLM CLI Szószedet query
type: prompt
tags: [meta, prompt]
pipeline_step: 07_citations_maker
updated: 2026-05-29
---

# Prompt D -- NLM CLI Szószedet query

**Hova:** `nlm query notebook $NB $promptD --json`

**Mikor:** 07_citations_maker lépésben, 05_assemble.py után.

## ASCII prompt (PowerShell heredoc)

```powershell
$promptD = @'
Generalj szoszedetet (min. 15, max. 30 szakkifejezesbol) a forrasok alapjan. Minden bejegyzeshez ird meg:
1. Magyar terminus (H1 ##)
2. Angol terminus (Angol: ...)
3. Definicio (max. 1 mondat, forrasbol -- Definicio: ...)
4. Szint (BSc vagy MSc -- Szint: ...)
5. Forras-hivatkozas (forrasnev.pdf: oldal) szovegkozi hivatkozaskent

BSc szint: alapfogalmak, amelyek BSc tanulmanyok soran szuksegek.
MSc szint: melyebb elmelet, kutatasi szintu fogalmak.
Sorrend: ABC szerint magyarul.
'@
$NB = "<notebook_id>"
nlm query notebook $NB $promptD --json | Out-File 3_raw_outputs/nlm_szozedet_raw.txt -Encoding utf8
```

## Kimenet formátum (`N_Szozedet.md`-ben)

```markdown
## Magyar Terminus

**Angol:** English Term
**Definíció:** Egy mondatos definíció forrás alapján.<sup>[N]</sup>
**Szint:** BSc / MSc
```
