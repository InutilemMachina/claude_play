---
name: 10_notes_collector
title: 10_NOTES_COLLECTOR -- Notes Collector
type: skill
tags: [meta, skill]
status: active
version: 2.0
updated: 2026-05-26
description: Tartalomjegyzék (ToC) generálása és képek beillesztése a Jegyzetbe. Script: generate_index.py ✅ + 09_figure_mapper catalog alapján. Pipeline 10. lépése.
---

# 10_NOTES_COLLECTOR

## 1. Cél

A `N_Jegyzet.md` elejére `## Tárgymutató` ToC-ot szúr be, és a `figure_catalog.json` `inserted_after_paragraph` mezői alapján beilleszti a képeket.

## 2. Bemenetek

- `4_wip_outputs/N_Jegyzet.md` -- 06-09 kimenet
- `3_raw_outputs/figure_catalog.json` -- 09_figure_mapper által frissítve

## 3. Eljárás

### 3.1. Tartalomjegyzék generálása

Minden `##`, `###`, `####` szintű fejléc anchor-linkkel szerepel, behúzással:

```markdown
## Tárgymutató

- [Fejezet neve](#fejezet-neve)
  - [Alfejezet neve](#alfejezet-neve)
    - [Részfejezet neve](#reszfejezet-neve)
```

**Anchor-link szabályok (GFM):**
- Kisbetűsítés, `#` eltávolítása
- Speciális karakterek (`(`, `)`, `.`, `,`, `!`, `?`, `:`, `*`) eltávolítása
- Szóközök → `-`
- Magyar ékezetes betűk **megmaradnak** (`é`, `á`, `ő`, `ű`)
- Duplikált fejlécek: `-1`, `-2` suffix

Kizárt szekciók: `# Főcím`, `## Tárgymutató`, `## Forrásjegyzék`.

### 3.2. Képbeillesztés

A `figure_catalog.json` alapján:

```python
for key, entry in sorted(catalog.items(),
                          key=lambda x: x[1].get("inserted_after_paragraph") or 9999):
    idx = entry.get("inserted_after_paragraph")
    if idx is None:
        continue
    fig_block = (
        f"\n![{entry['caption']}]({entry['path']})\n"
        f"*{entry['caption']}*\n"
    )
    paragraphs[idx] = paragraphs[idx] + fig_block
```

Ha több kép ugyanarra a bekezdés-indexre illeszkedik: `match_score` szerint csökkenő sorrend.

### 3.3. Kulcsszavas mélylink (opcionális)

Ha a felhasználó kulcsszó-listát ad meg, a skill `<a id="idx-kulcsszó"></a>` horgonyokat szúr be, és hozzáadja a ToC-hoz.

**Kulcsszó-stratégia célközönség szerint:**
- BSc kezdő: fizikai alapfogalmak, törvények neve, mérési fogalmak
- Haladó/mérnök: ritkán előforduló specifikus szakkifejezések
- Általános dokumentum: csak fejléc-alapú ToC, kulcsszavak nélkül

## 4. Kimenetek

- `4_wip_outputs/N_Jegyzet.md` -- ToC hozzáadva + képek beillesztve (in-place)

## 5. Ellenőrzés

- [ ] `## Tárgymutató` blokk a főcím (`#`) után megjelent
- [ ] Fejléc-linkek anchor-jai helyesek (manuális ellenőrzés 2-3 linken)
- [ ] Képek beillesztve a megjelölt bekezdések után
- [ ] Nincs duplikált `## Tárgymutató` blokk

## 6. Hibakezelés

- Tünet: ToC linkek leading spaces-szel kezdődnek
- Gyökérok: `###` fejlécek `##` szülő nélkül (heading hierarchia hiba, 06_excerpt_block_maker §8)
- Megoldás: `05_assemble.py` Q1-hez `## Bevezetés` szülőt generáljon

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [09_figure_mapper.md](09_figure_mapper.md) -- képek pozícionálása
- [11_typesetter.md](11_typesetter.md) -- Rule G (fejléc-számozás)

## 8. Visszajelzések

- 💬 NOTE: ToC hierarchikus számozás: a ToC linkek nem tartalmazzák a sorszámokat, mert a `##` fejlécek sem voltak egységesen számozva. `11_util_heading_numberer.py` futtatása a ToC generálása előtt megoldja.
- 💬 NOTE: A `§3.3` NLM mindmap-alapú lekérdezési stratégia a 04_nlm_query_runner skillbe lett áthelyezve.
- ❔ QUESTION: A pedagógiai output kötelező elemei: tanulási célok, főszöveg, kulcsfogalmak, összefoglaló, kérdések -- mennyi és milyen formátumban? (Összefoglaló blokk: `> [!NOTE]` GFM callout megoldás?)

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-30 | 2.1 | K0 cleanup: 5 ✅ → §9 (ToC idempotencia, encoding fix, unnumbered, dupla sorszámozás, archivált scriptek) |
| 2026-05-26 | 2.0 | Overhaul: template-alapú átírás; NLM mindmap szekció áthelyezve 04-be; §8 Visszajelzések |
| 2026-05-24 | 1.1 | §3.4 NLM mindmap-alapú lekérdezési stratégia hozzáadva |
| 2026-05-21 | 1.0 | Létrehozva |
