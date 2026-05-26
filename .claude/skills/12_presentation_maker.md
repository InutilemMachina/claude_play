---
name: 12_presentation_maker
title: 12_PRESENTATION_MAKER — Presentation maker
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-05-21
description: N_Jegyzet.md → N_Prezentacio.md (Marp) + N_Prezentacio.pptx (python-pptx). du_template.pptx sablont használ.
---
# 12_PRESENTATION_MAKER.MD — PRESENTATION MAKER
_08. lépés_

# 1. Cél
`N_Jegyzet.md` → `N_Prezentacio.md` (Marp) + `N_Prezentacio.pptx` (python-pptx)

# 2. Struktúra (minden hétnél)
Bevezetés → Főtémák (fejezetenként 1-2 dia) → Összefoglalás → Kérdések

# 3. Marp sablon
```
---
marp: true
theme: default
paginate: true
---
# [Heti téma]
### N. hét
---
## [Fejezet]
...
---
<!-- MSc -->
## [MSc] Témacím
...
<!-- /MSc -->
```

# 4. PPTX generálás
```bash
python scripts/12_pptx_gyarto.py N_Prezentacio.md --template templates/du_template.pptx
```
⚠️ `templates/du_template.pptx` — te töltöd fel egyszer. **🛑 Nélküle nem generál PPTX-t.**

# 5. MSc diák
- Marp: `<!-- MSc -->` blokkon belül
- PPTX: külön dia MSc felirattal — `bsc_export.py` kihagyja

# 6. Ismert hiányosság
`pptx_gyarto.py` script még nem létezik — PPTX generálás egyelőre manuális.


# Ismert hibák

Nincs ismert, skill-specifikus pitfall. Általános: [pitfalls.md](../pitfalls.md)

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
