---
title: Prompt C -- NLM Data Tables Studio (index)
type: prompt-index
pipeline_step: 01 / 07 / 09 / 13
updated: 2026-05-29
---

# Prompt C — NLM Data Tables Studio (index)

**Hova:** NotebookLM → Studio panel → Data Tables → **ceruza ikon** → "Customize Data Table"  
**Elérhetőség:** ✅ minden felhasználónak (2026 elejétől minden tier-re)

| Al-prompt | Fájl | Pipeline lépés |
|:----------|:-----|:---------------|
| C.1 Forrásáttekintő | [prompt_c1_forrasattekinto.md](prompt_c1_forrasattekinto.md) | 01_references_collector |
| C.2 Fogalomtérkép | [prompt_c2_fogalomterkep.md](prompt_c2_fogalomterkep.md) | 07_citations_maker |
| C.3 Ábrajegyzék (képpipeline fallback) | [prompt_c3_abrajegyzek.md](prompt_c3_abrajegyzek.md) | 09_figure_mapper |
| C.4 Kérdésbank-alap | [prompt_c4_kerdesbank_alap.md](prompt_c4_kerdesbank_alap.md) | 13_question_bank_collector |

---

## Közös workflow (minden C.x prompthoz)

**Generálás:**
1. Studio tab → Data Tables kártya
2. Kattints a **ceruza ikonra** (ne a sima "Generate"-re!)
3. Másold be a megfelelő C.x prompt szövegét
4. Generate

**Mentés:**
1. **Export-Tool** — https://github.com/cced3000/NotebookLM-Export-Tool (automatikus letöltés)
2. **Kézi másolás** — a chat-ablakban megjelenő táblázatot közvetlenül be lehet másolni a `3_raw_outputs/` mappába

**Megjegyzés:** Az MCP automatizálás angol kimenetet ad — a generálás tehát emberi lépés. A mentés viszont mindig elvégezhető manuálisan is.

## Változásjegyzék

| Dátum | Leírás |
|-------|--------|
| 2026-05-29 | C.1–C.4 → önálló fájlok; ez az index a megosztott workflow-val |
| 2026-05-29 | C.3 ábrajegyzék fallback hozzáadva; kézi mentés dokumentálva |
| 2026-05-21 | Létrehozva (C §3.1–3.3) |
