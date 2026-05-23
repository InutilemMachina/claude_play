---
name: 01_html_to_md
title: 01_HTML_TO_MD — HTML to Markdown conversion
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-05-21
description: NotebookLM SingleFile HTML export Markdown-ra konvertálása. Input: tema_nev.html; output: tema_nev.md a forrasok/ mappában.
---
# 01_HTML_TO_MD.MD — HTML TO MARKDOWN CONVERSION
_01. lépés_

# 1. Cél
NotebookLM SingleFile HTML export → `N_het/forrasok/tema_nev.md`

# 2. Input
`N_het/forrasok/*.html` — NotebookLM SingleFile export (1 HTML per hét)
**🛑 Ha hiányzik: Claude leáll és kéri a feltöltést.**

# 3. Feldolgozási lépések
1. `message-content` class blokkok kinyerése
2. Hivatkozás gombok → `<sup>[N]</sup>` formátum
3. KaTeX math → `$...$` és `$$...$$`
4. Globális citáció deduplikáció
5. `## Forrásjegyzék` szekció generálása a fájl végén

# 4. Citáció formátum
- Hivatkozás: `<sup>[N]</sup>`
- Forrásjegyzék: `**[N]** Cím` + `> ↖ *Szekció neve*` backlink

# 5. Kimenet
`N_het/forrasok/tema_nev.md`
- Fájlnév: a NLM projekt témájából, CamelCase, pl. `KompresszorInstabilitas.md`
- 1 HTML → 1 MD (egy hetet fed le)

# Megjegyzés
NLM képek nem kerülnek át — megoldás: manuális képernyőkép vagy NLM PDF export.


# Ismert hibák

Nincs ismert, skill-specifikus pitfall. Általános: [pitfalls.md](../pitfalls.md)

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
