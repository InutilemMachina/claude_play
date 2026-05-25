---
name: 03_excerpt_block_maker
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

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-22 — Whitespace szabály pontosítva | 1.0 | \n\n kötelező blockquote előtt/után (07 Rule D = 0) |
