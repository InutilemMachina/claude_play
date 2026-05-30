---
name: 06_excerpt_block_maker
title: 06_EXCERPT_BLOCK_MAKER -- Excerpt Block Maker
type: skill
tags: [meta, skill]
status: active
version: 2.0
updated: 2026-05-26
description: Strukturált összefoglaló blockquote-ok (💡 Lényeg, 🗺️ Fejezet összegzés) in-place szúrása a Jegyzetbe. Pipeline 06. lépése.
---

# 06_EXCERPT_BLOCK_MAKER

## 1. Cél

A `4_wip_outputs/N_Jegyzet.md` minden `###` szintű alfejezete után `💡 Lényeg` blokkot, minden `##` fejezet zárásánál `🗺️ Fejezet összegzés` blokkot szúr be in-place.

## 2. Bemenetek

- `4_wip_outputs/N_Jegyzet.md` -- összeállított Jegyzet draft (05_assemble.py kimenet)

## 3. Eljárás

### 3.1. Alfejezet-összefoglaló (`###` szint után)

Minden `###` szintű alfejezet tartalma után, közvetlenül a következő fejléc vagy fájlvég előtt:

```markdown
> **💡 Lényeg:** [2–4 összefoglaló mondat folyó szövegben.]
```

### 3.2. Fejezet-összegzés (`##` szint zárásánál)

```markdown
> **🗺️ Fejezet összegzés -- [fejezet neve]**
>
> [1 bevezető mondat.]
> **[alfejezet neve]** -- [egy mondatos lényeg].
> Összességében: [1 záró mondat.]
```

### 3.3. Szabályok

- **Ne duplikálj:** Meglévő blockquote-ot frissítsd, ne szúrj be újat.
- Összefoglalók **folyó mondatokban** -- nem bullet pontokban.
- Blockquote előtt és után **kötelező kettős üres sor** (`\n\n`):
  ```
  [előző szöveg]

  > **💡 Lényeg:** ...

  [következő fejléc]
  ```
  Ez biztosítja, hogy a 11_typesetter Rule D ne jelezzen hibát.
- Meglévő szöveget **ne módosítsd**.
- Nyelv: **magyar**. Angol szakkifejezések megtarthatók.

## 4. Kimenetek

- `4_wip_outputs/N_Jegyzet.md` -- in-place frissítve (`💡` és `🗺️` blokkok beillesztve)

## 5. Ellenőrzés

- [ ] Minden `###` fejezet után megjelent `💡 Lényeg` blokk
- [ ] Minden `##` fejezet végén megjelent `🗺️ Fejezet összegzés`
- [ ] Meglévő blockquote-ok nem duplikálódtak
- [ ] Kettős üres sorok a blockquote-ok előtt/után (`\n\n`)
- [ ] 11_typesetter Rule D: 0 javítás a blockquote-ok körül

## 6. Hibakezelés

- Tünet: duplikált `💡 Lényeg` blokkok
- Gyökérok: a skill nem ellenőrizte a meglévő blockquote-okat
- Megoldás: keresd meg a duplikátumokat (`grep '💡 Lényeg' fajl.md`), töröld a duplikátumokat

- Tünet: `💡 Lényeg` blockquote a `<!-- Q:N -->` marker UTÁN jelenik meg (helyes: előtte)
- Gyökérok: body-gyűjtő loop csak `##`/`###`-nál áll meg; `<!-- Q:N -->` átcsúszik a body-ba
- Megoldás: loop feltétel kiterjesztése: `or re.match(r'^<!-- Q:\d+ -->', peek): break`

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [11_typesetter.md](11_typesetter.md) -- Rule D (blockquote spacing)

## 8. Visszajelzések

- 🔲 TODO: **`abstractive` mód implementálandó.** Az extractive script (06_excerpt_block_maker.py) megoldja a skálázást (227 blokk, gond nélkül), de a minőség alacsonyabb mint egy LLM-é. Ha API elérhető, `--mode abstractive` LLM-összefoglalóval.
- 💬 NOTE: Lista whitespace: a generált szövegben `*   **...**` forma (több szóköz) helyett `* **...**` legyen. Megoldandó: 11_typesetter.py lint-szabályba felvenni (`*{3,}` → `* `).
- 💬 NOTE: Heading hierarchia: Q1 kimenetben `###` közvetlenül `#` alatt (nincs `##`). Következmény: VSCode vázlatban és ToC-ban inkonzisztens szintek. Megoldandó: `05_assemble.py` Q1-hez `## Bevezetés` szülőt generáljon, vagy Prompt B módosítás.
- 💬 NOTE: Formázási alternatíva: a blockquote-ok helyett `<div style="background-color: rgba(120,120,120,0.08); border-radius: 6px; padding: 15px;">` alapú doboz (Obsidian/VSCode preview-ban lekerekített szürke háttér). Archiválva: `.claude/archive/markdown_textboxes.md`.
- 💬 NOTE: A `06. lépés az egyetlen hely, ahol a pedagógiai minőség számottevően javul -- a 💡 és 🗺️ blokkok valóban hozzáadnak értéket. Ha a pipeline-t le kell csökkenteni, ez az egyik lépés, amelyet mindenképpen meg kell tartani.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-31 | 2.2 | 3. hét cleanup: ingyenes alternatívák §9 (jövőbeli research, abstractive mód marad nyitott) |
| 2026-05-30 | 2.1 | K0 cleanup: ✅ → §9; skálázhatóság TODO tömörítve (abstractive mód marad nyitott) |
| 2026-05-26 | 2.0 | Overhaul: template-alapú átírás; cím 03→06 javítva; §8 Visszajelzések |
| 2026-05-25 | 1.1 | NOTE-ok: lista whitespace, heading hierarchia, formázási alternatíva |
| 2026-05-22 | 1.0 | Létrehozva; `\n\n` kötelező blockquote előtt/után |
