---
name: 06_excerpt_block_maker
title: 03_EXCERPT_BLOCK_MAKER — Excerpt block maker
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-05-21
description: Strukturált összefoglaló blockquote-ok (💡 Lényeg, 🗺️ Fejezet összegzés) Markdown fájlba szúrása.
---

# 03_EXCERPT_BLOCK_MAKER.MD — EXCERPT BLOCK MAKER
_03. lépés_

Beolvas egy strukturált Markdown fájlt, és **két típusú összefoglaló blockquote-ot** szúr be a megfelelő helyekre, majd visszaírja a módosított tartalmat ugyanabba a fájlba.

# 1. Mit csinál pontosan

## 1.1. Alfejezet-összefoglaló (`###` szint után)

Minden `###` szintű alfejezet tartalma után — közvetlenül a következő fejléc vagy fájlvég előtt — egy tömör, 2–4 mondatos lényegi összefoglalót szúr be:

```markdown
> **💡 Lényeg:** [2–4 összefoglaló mondat folyó szövegben.]
```

## 1.2. Fejezet-összegzés (`##` szint után)

Minden `##` szintű fejezet összes alfejezetének lezárása után — egy hierarchikus összegző blokkot szúr be:

```markdown
> **🗺️ Fejezet összegzés — [fejezet neve]**
>
> [1 bevezető mondat.]
> **[alfejezet neve]** — [egy mondatos lényeg].
> Összességében: [1 záró mondat.]
```

# 2. Workflow
1. Beolvasás: `.md` fájl teljes tartalma.
2. Szerkezet elemzése: `#` = főcím, `##` = fejezet, `###` = alfejezet.
3. Összefoglalók generálása.
4. In-place visszaírás.

# 3. Fontos szabályok
- **Ne duplikálj:** Meglévő blockquote-ot frissítsd, ne szúrj be újat.
- Összefoglalók **folyó mondatokban**, nem bullet pontokban.
- Beillesztett blokkok előtt és után **kötelező kettős üres sor** (`\n\n`):
  ```
  [előző bekezdés szövege]

  > **💡 Lényeg:** ...

  [következő fejléc vagy bekezdés]
  ```
  Ez biztosítja, hogy a 07_typesetter Rule D ne jelezzen hibát (0 javítás).
- Meglévő szöveget **ne módosítsd**.
- Nyelv: magyar. Angol szakkifejezések megtarthatók.


# Ismert hibák

→ [pitfalls.md §3.2](../pitfalls.md) -- Q:N marker belekerül a body_lines-ba

# NOTE-ok (tesztelés visszajelzések)

- NOTE 💬 **Lista whitespace:** A generált szövegben a felsorolásjel után (`*`) felesleges szóközök kerülnek (pl. `*   **Kompakt jelölés:**`). Elég egyetlen szóköz (`* **...**`). Megoldandó: a 11_typesetter.py lint-szabályai közé felvenni (`*{3,}` → `* `).
- NOTE 💬 **Heading hierarchia:** A Q1 kimenetben a `###` fejlécek közvetlenül a `#` főcím alá kerülnek (`##` szint kihagyásával). A többi szekció (Q2+) `##` + `###` struktúrát kap, de a Q1 bevezető rész nem. Következmény: VSCode vázlatban (és ToC-ban) a szintek nem konzisztensek. Megoldandó: 05_assemble.py Q1 kezelése: vagy `## Bevezetés` szülő szekciót kell köré generálni, vagy az NLM Prompt B-t kell módosítani, hogy a Q1 is `##` szintű fejezeteket tartalmazzon.
- NOTE 💬 **Formázás alternatíva:** A `> **💡 Lényeg:**` és `> **🗺️ Fejezet összegzés**` blockquote-ok helyett a `markdown_textboxes.md` **3. megoldása** javasolt (`<div style="background-color: rgba(120, 120, 120, 0.08); border-radius: 6px; padding: 15px; margin: 15px 0;">`). Ez Obsidian/VSCode preview-ban lekerekített, szürke hátteres dobozként jelenik meg. A fájl archiválva: `.claude/archive/markdown_textboxes.md`. Implementáció: skill következő verziójában.
- NOTE 💬 **Ingyenes alternatívák:** A 06. lépés Claude-feladat (nem script). Ingyenes alternatívák a blockquote generáláshoz: (1) Ollama helyi LLM (pl. llama3, mistral) -- azonos prompt-logika, de lassabb, hardver-függő; (2) szabály-alapú kivonat (első/utolsó mondat per szekció) -- deterministikus, de minőség korlátozott; (3) NLM maga query-n át -- de ez extra NLM hívás, token-ár nélkül, de lassabb. Ajánlott: helyi Ollama a reprodukálhatóság és offline futás miatt.
- NOTE 💬 **Pipeline-szintű megfigyelés (saját):** A 06. lépés az egyetlen hely, ahol a pedagógiai minőség számottevően javul -- a `💡 Lényeg` és `🗺️ Fejezet összegzés` blokkok valóban hozzáadnak értéket. A többi lépés inkább strukturális/technikai. Ha a pipeline-t le kell csökkenteni, ez az egyik lépés, amelyet mindenképpen meg kell tartani.

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-22 | 1.0 | Létrehozva; \n\n kötelező blockquote előtt/után (07 Rule D = 0) |
| 2026-05-25 | 1.1 | NOTE-ok: lista whitespace, heading hierarchia, formázási alternatíva, ingyenes alternatívák |
