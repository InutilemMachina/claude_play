---
title: NLM_PROMPTS.MD — Prompt index
type: meta
tags: [meta, reference]
updated: 2026-05-29
description: Index. Minden prompt kanonikus helye .claude/prompts/. Ne szerkeszd itt a tartalmat.
---

# NLM Prompts — Index

> **Szerkesztés mindig a `.claude/prompts/` mappában.** Ez a fájl csak index.

| Prompt | Fájl | Pipeline lépés | Megjegyzés |
|:-------|:-----|:---------------|:-----------|
| A — Claude Project Instructions | `.claude/archive/prompt_a.md` | -- | Elavult -- aktualitása kérdéses |
| B — NLM Custom Instructions | [prompt_b_nlm_custom_instructions.md](prompts/prompt_b_nlm_custom_instructions.md) | 02 | Legfontosabb; minden notebookon beállítandó |
| C — Data Tables Studio | [prompt_c_datatables.md](prompts/prompt_c_datatables.md) | 01 / 09 / 13 | C.3 = képpipeline fallback |
| D — Szószedet CLI query | [prompt_d_szozedet.md](prompts/prompt_d_szozedet.md) | 07 | `nlm query ... --json` |
| E — Kérdésbank CLI query | [prompt_e_kerdesbank.md](prompts/prompt_e_kerdesbank.md) | 13 | `nlm query ... --json` |

# Változásjegyzék

| Dátum | Leírás |
|-------|--------|
| 2026-05-29 | Teljes lecsupaszítás indexre; B/C/D/E → `.claude/prompts/`; A → archive |
| 2026-05-29 | Prompt C kiemelve (`prompt_c_datatables.md`); C.3 ábrajegyzék fallback hozzáadva |
| 2026-05-29 | Prompt B frissítve: `##` kötelező első sor + prose szabály (J1) |
| 2026-05-26 | Prompt D hozzáadva |
| 2026-05-21 | Létrehozva (A+B+C) |
