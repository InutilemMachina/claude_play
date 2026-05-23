---
name: 10_bsc_filter
title: 10_BSC_FILTER — BSc filter
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-05-21
description: MSc blokkokat kiszűri, BSc verziót generál N_het/bsc/ mappába. Python script fut.
---
# 10_BSC_FILTER.MD — BSC FILTER
_10. lépés_

# 1. Cél
MSc blokkokat kiszűri, BSc verziót generál `N_het/bsc/` mappába.

# 2. Script
```bash
python _claude/scripts/bsc_export.py --het N --tantargy [mappa]
```
⚠️ Script még nem létezik — generálandó. Addig manuális.

# 3. Szűrési logika
- `<!-- MSc -->` ... `<!-- /MSc -->` blokkok → kihagyva
- Mermaid `[MSc]` node-ok → kihagyva
- SZINT:4-5 kérdések → kihagyva

# 4. Kimenet (`N_het/bsc/`)
- `N_Kivonat_BSc.md`
- `N_Jegyzet_BSc.md`
- `N_Kerdesek_BSc.md`
- `N_Prezentacio_BSc.pptx`

# 5. Mikor fut
Az adott hét összes outputja kész → BSc export → `bsc/` feltöltődik.
**`bsc/` addig üres — ez helyes, nem hibajelzés.**


# Ismert hibák

Nincs ismert, skill-specifikus pitfall. Általános: [pitfalls.md](../pitfalls.md)

# Nyitott kérdések

- bsc/ struktúra lapítása: N_Mindmap.md + N_Mindmap_bsc.md egyszintű forma -- jelenleg bsc/ almappában vannak a fájlok.

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
