---
title: CLAUDE.md -- master index
type: meta
tag: [meta]
version: 1.0
updated: 2026-05-26
description: Belépési pont, olvasási sorrend és fájlindex.
---

# CLAUDE.md

## 1. Indulás

Minden session elején ezt a két fájlt olvasd be:

1. `Instructions.md`
2. `.claude/pipeline.md`

## 2. Olvasási szabály

Más fájlt csak akkor olvass be, ha a feladat ezt közvetlenül igényli.

- Skill fájl: ha az adott pipeline-lépést futtatod. **Hibakezelés a skill §6-jában van.**
- `project_status.md`: ha állapotot kell frissíteni.
- `scripts/*.py`: ha végrehajtó logikára van szükség.

## 3. Rövid elv

- Egy fájl = egy cél.
- Az `Instructions.md` tartalmazza a stabil szabályokat.
- A `pipeline.md` tartalmazza a végrehajtási gráfot.
- A skill-ek csak lokális működési protokollok.
- A script-ek a végrehajtást végzik.

## 4. Fájlkatalógus

- `.claude/pipeline.md` -- pipeline és függőségek
- `Instructions.md` -- projekt-alkotmány
- `.claude/project_status.md` -- futási állapot
- `.claude/skill_template.md` -- skill-sablon
- `.claude/skills/*.md` -- egyes pipeline-lépések
- `scripts/*.py` -- automatizmusok

## 5. Kommunikáció

- Tömör, egyértelmű, redundanciamentes.
- Ne ismételd meg a globális szabályokat.
- Ha valami nem egyértelmű, a megfelelő kanonikus fájlra hivatkozz.

TODO: itt is relatív linkek alkalmazása