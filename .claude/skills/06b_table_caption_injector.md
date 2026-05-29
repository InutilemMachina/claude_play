---
name: 06b_table_caption_injector
title: 06B_TABLE_CAPTION_INJECTOR -- Táblázatfelirat injektálás
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-05-29
description: GFM táblázatok fölé automatikus számozott felirat (*N. táblázat: ...*) szúrása. Script: 06_table_caption_injector.py. Pipeline 06b. lépése (06_excerpt_block_maker UTÁN).
---

# 06B_TABLE_CAPTION_INJECTOR

## 1. Cél

A `4_wip_outputs/N_Jegyzet.md`-ben lévő GFM táblázatok fölé akadémiai konvenció szerint számozott feliratot szúr be: `*N. táblázat: (automatikus felirat)*`.

**Akademikus konvenció:** a táblázatfelirat a táblázat FELETT áll (ellentétben az ábracímmel, amely alatta).

## 2. Bemenetek

- `4_wip_outputs/N_Jegyzet.md` -- 06_excerpt_block_maker kimenet

## 3. Eljárás

```powershell
python scripts/06_table_caption_injector.py 4_wip_outputs/N_Jegyzet.md

# Opciók:
--prefix "táblázat"   # Felirat előtag (alap: "táblázat")
--dry-run             # Csak megjeleníti, nem ment
--no-backup           # .bak fájl kihagyása
```

**Működés:**
1. GFM táblázat-blokkok keresése (`|` kezdetű sorok)
2. Ha a táblázat felett nincs már felirat (`*N. táblázat*` minta) → sorszámozott felirat szúrása
3. Meglévő feliratok érintetlenül maradnak
4. In-place felülírás, `.bak` backup

**Generált felirat formátuma:**
```markdown
*1. táblázat: (automatikus felirat)*
| Fejléc | ... |
| :--- | ... |
```

## 4. Kimenetek

- `4_wip_outputs/N_Jegyzet.md` -- in-place felülírva (feliratok hozzáadva)

## 5. Ellenőrzés

- [ ] Minden GFM táblázat felett `*N. táblázat:` sor látható
- [ ] Dupla felirat nincs (meglévők megmaradtak)
- [ ] Sorszámozás folyamatos (1, 2, 3, ...)

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `(automatikus felirat)` megmarad a végtermékben | A script placeholder szöveget szúr, nem valódi tartalmat | Opció: NLM Qfig Studio query táblázatcímekhez, vagy manuális szerkesztés |
| Dupla felirat | Script kétszer futott | Idempotens -- meglévő feliratot kihagyja; dupla sor nem keletkezhet |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [06_excerpt_block_maker.md](06_excerpt_block_maker.md) -- előfeltétel
- [11_typesetter.md](11_typesetter.md) -- Rule I: tábla-szeparátor javítás

## 8. Visszajelzések

- 💬 NOTE: **`(automatikus felirat)` placeholder** -- a script nem ismeri a táblázat tartalmát, ezért generikus szöveget szúr. BSc-szintű kiadványban manuális szerkesztés vagy NLM-alapú cím-generálás szükséges.
- 💬 NOTE: **Skill létrehozva (2026-05-29, bottom-up audit).** A script a pipeline 06b. lépéseként szerepel (`pipeline.md §1`), de korábban nem volt önálló skill-dokumentációja.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-29 | 1.0 | Létrehozva (bottom-up audit hiányosság pótlása) |
