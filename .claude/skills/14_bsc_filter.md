---
name: 14_bsc_filter
title: 14_BSC_FILTER — BSc filter
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-05-21
description: MSc blokkokat kiszűri, BSc verziót generál N_het/bsc/ mappába. Python script fut.
---
# 14_BSC_FILTER.MD — BSC FILTER
_10. lépés_

# 1. Cél
MSc blokkokat kiszűri, BSc verziót generál `N_het/bsc/` mappába.

# 2. Script
```bash
python _claude/scripts/14_bsc_export.py --het N --tantargy [mappa]
```
⚠️ Script még nem létezik — generálandó. Addig manuális.

# 3. Szűrési logika
- `<!-- MSc -->` ... `<!-- /MSc -->` blokkok → kihagyva
- Mermaid `[MSc]` node-ok → kihagyva
- SZINT:4-5 kérdések → kihagyva

# 4. Kimenet (`5_clean_outputs/`)
BSc fájlok **nem almappában**, hanem `_bsc` suffixszel a `5_clean_outputs/`-ban:
- `N_Jegyzet_bsc.md`
- `N_Szozedet_bsc.md`
- `N_Mindmap_bsc.md`
- `N_Kerdesek_bsc.md`
- `N_Prezentacio_bsc.pptx` (ha a pptx-generálás MSc-szűrést is támogat)

# 5. Mikor fut
Az adott hét összes outputja kész → BSc export → `bsc/` feltöltődik.
**`bsc/` addig üres — ez helyes, nem hibajelzés.**


# NOTE-ok (tesztelés megfigyelések)

- NOTE 💬 **MSc jelölés emberi döntés:** A `<!-- MSc -->` blokkokat és a Mermaid `[MSc]` node-okat ember tölti ki review után -- a pipeline nem dönt automatikusan BSc/MSc határról. Ez szándékos: a pedagógiai szint megítélése tantárgy- és hallgató-specifikus.
- NOTE 💬 **1_Jegyzet.md 0 karakter eltávolítás:** Az első teszten a Jegyzet BSc-szűrésekor 0 karakter távolodott el -- a Jegyzet szövegébe nem kerültek `<!-- MSc -->` jelölések (csak a Kérdésbank és a Mindmap-mermaid tartalmazott ilyeneket). A jövőben a 04_nlm_query_runner MSc-szintű tartalmait `<!-- MSc -->` blokkokba kell zárni.
- NOTE 💬 **`bsc/` almappa vs. `_bsc` suffix -- döntés:** `_bsc` suffix választva (pl. `1_Jegyzet_bsc.md`). Indok: lapítottabb `5_clean_outputs/` struktúra, kevesebb mappanavigáció, konzisztens a többi kimeneti fájllal. A `bsc/` almappa elhagyandó; az összes érintett script egyszerre frissítendő (14_bsc_filter.py + pipeline.md mappastruktúra).
- NOTE 💬 **Camera-ready scope:** A `5_clean_outputs/` nemcsak a Prezentációt tartalmazza, hanem minden végterméket: `N_Jegyzet_bsc.md`, `N_Szozedet_bsc.md`, `N_Mindm