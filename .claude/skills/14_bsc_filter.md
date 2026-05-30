---
name: 14_bsc_filter
title: 14_BSC_FILTER -- BSc Filter
type: skill
tags: [meta, skill]
status: active
version: 2.0
updated: 2026-05-26
description: MSc blokkokat kiszűri, BSc verziót generál 5_clean_outputs/-ba _bsc suffixszel. Script: 14_bsc_filter.py ✅. Pipeline 14. lépése.
---

# 14_BSC_FILTER

## 1. Cél

A `4_wip_outputs/N_*.md` fájlokból eltávolítja az MSc blokkokat, és BSc-szűrt végtermékeket (`_bsc` suffix) a `5_clean_outputs/`-ba ment.

## 2. Bemenetek

- `4_wip_outputs/N_Jegyzet.md`
- `4_wip_outputs/N_Szozedet.md`
- `4_wip_outputs/N_Mindmap.md`
- `4_wip_outputs/N_Kerdesek.md`
- `4_wip_outputs/N_Prezentacio.md`

**Előfeltétel:** Az adott hét összes 4_wip_outputs fájlja kész.

## 3. Eljárás

### 3.1. Szűrési logika

- `<!-- MSc -->` ... `<!-- /MSc -->` blokkok → kihagyva
- Mermaid `[MSc]` node-ok → kihagyva
- `SZINT:4-5` kérdések → kihagyva

### 3.2. Futtatás (ha script elérhető)

```bash
python scripts/14_bsc_filter.py --het N --tantargy <mappa>
```

✅ **Script kész** -- `scripts/14_bsc_filter.py` (2026-05-26).

### 3.3. MSc jelölés felelőssége

⚠️ Az MSc/BSc határ **emberi döntés** -- a pipeline nem dönt automatikusan. A `<!-- MSc -->` blokkokat és a Mermaid `[MSc]` node-okat manuális review után kell kitölteni (04_nlm_query_runner, 08_mindmap_manager, 13_question_bank_collector).

## 4. Kimenetek

BSc fájlok `_bsc` suffixszel a `5_clean_outputs/`-ban (lapos struktúra, nem almappában):

- `5_clean_outputs/N_Jegyzet_bsc.md`
- `5_clean_outputs/N_Szozedet_bsc.md`
- `5_clean_outputs/N_Mindmap_bsc.md`
- `5_clean_outputs/N_Kerdesek_bsc.md`
- `5_clean_outputs/N_Prezentacio_bsc.pptx` (ha MSc-szűrés a PPTX-generálásban is támogatott)

**`5_clean_outputs/` addig üres -- ez helyes, nem hibajelzés.**

## 5. Ellenőrzés

- [ ] Minden `_bsc` fájl létrejött
- [ ] `<!-- MSc -->` blokkok nem szerepelnek a BSc fájlokban
- [ ] Mermaid `[MSc]` node-ok hiányoznak a BSc mindmap-ből
- [ ] `SZINT:4-5` kérdések hiányoznak a BSc kérdésbankból
- [ ] `5_clean_outputs/` tartalmaz camera-ready végtermékeket

## 6. Hibakezelés

- Tünet: BSc Jegyzetben 0 karakter eltávolítva
- Gyökérok: `<!-- MSc -->` jelölések nem kerültek a Jegyzet szövegébe (csak Mindmap és Kérdésbankban)
- Megoldás: 04_nlm_query_runner MSc-szintű tartalmait `<!-- MSc -->` blokkokba kell zárni

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [scripts/14_bsc_filter.py](../../scripts/14_bsc_filter.py) ✅
- [08_mindmap_manager.md](08_mindmap_manager.md) -- `[MSc]` node-ok
- [13_question_bank_collector.md](13_question_bank_collector.md) -- SZINT:4-5 kérdések

## 8. Visszajelzések

- 💬 NOTE: `_bsc` suffix döntés: laposabb `5_clean_outputs/` struktúra, kevesebb mappanavigáció. A `bsc/` almappa elhagyva (2026-05-26 döntés). Az összes érintett script egyszerre frissítendő, ha ez változik.
- 💬 NOTE: Camera-ready scope: a `5_clean_outputs/` nemcsak a Prezentációt tartalmazza, hanem minden végterméket (Jegyzet, Szószedet, Mindmap, Kérdések BSc verziói).
- 💬 NOTE: A Mindmap camera-ready hiányzik: `N_Mindmap.md` DRAFT státuszban marad -- a pipeline-nak `5_clean_outputs/`-ba is kell egy renderelt vagy exportált verziót előállítani (12. vagy 14. lépés felelőssége definiálandó).

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-30 | 2.1 | K0 cleanup: ✅ (script elkészült) → §9 |
| 2026-05-26 | 2.0 | Overhaul: template-alapú átírás; §8 Visszajelzések; lépésszám javítva (10→14) |
| 2026-05-26 | 1.1 | Camera-ready scope: minden végtermék `5_clean_outputs/`-ba |
| 2026-05-25 | 1.0 | Létrehozva; `_bsc` suffix konvenció rögzítve |
