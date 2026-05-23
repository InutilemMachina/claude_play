---
title: NLM-Claude Integrációs Útmutató
type: meta
tags: [meta, reference, integration]
updated: 2026-05-21 (rev2)
description: Tesztelt, működő NLM-Claude architektúra. Alapja: notebooklm-mcp-cli Python CLI, híd a Windows-MCP PowerShell toolon keresztül. + Export-Tool Studio workflow.
---
NOTE ez nem egy aktívan használt fájl

# NLM-Claude Integrációs Útmutató

# 1. Összefoglalás

## 1.1. Ami működik

```
Claude (Cowork)
  → mcp__Windows-MCP__PowerShell
    → nlm query notebook <ID> "<kérdés>" --json
      → NLM RAG (Gemini) lekérdezés
        → JSON válasz hivatkozásokkal (citations + references töltve, ha Prompt B aktív)
```

Tesztelve: 2026-05-21. Státusz: ✅

**Kritikus lelet (MP teszt, 2026-05-21):** A Configure Chat Custom Instructions (Prompt B) a CLI-lekérdezésekre is hat. Prompt B aktív notebookban a JSON válasz `citations` és `references` mezői teljes forrásazonosítókkal és idézett szövegrészletekkel töltődnek fel. Prompt B nélkül ezek üresek.

| JSON mező | Prompt B nélkül | Prompt B aktív |
|---|---|---|
| `sources_used` | [] | UUID lista (4-28 db) |
| `citations` | {} | {citáció-szám: UUID} szótár |
| `references` | [] | [{source_id, citation_number, cited_text}] lista |

## 1.2. Ami nem működik

- `mcpServers` kulcs a `claude_desktop_config.json`-ban **Cowork-ben nem aktív** (csak Claude Code-ban olvasódik).
- A `notebooklm-mcp.exe` sztenderd MCP szerver indításként nem jelenik meg a Cowork session-ben.
- A `nlm query notebook` CLI-nek nincs `--system` vagy `--instructions` flagje; rendszerszintű prompt csak Configure Chat-en keresztül adható.

---

# 2. Telepített eszköz: `notebooklm-mcp-cli`

## 2.1. Csomag azonosítás

| Tulajdonság | Érték |
|---|---|
| Csomag neve | `notebooklm-mcp-cli` |
| Típus | Python (uv tool) |
| Verzió | 0.6.10 |
| Szerző | Jacob Ben-David |
| PyPI | https://pypi.org/project/notebooklm-mcp-cli/ |
| GitHub | https://github.com/jacob-bd/notebooklm-mcp-cli |
| Auth mechanizmus | Cookie kinyerés Edge-ből (`nlm login`) |
| Binárisok | `nlm.exe`, `notebooklm-mcp.exe` |
| Elérési út | `C:\Users\lasz\AppData\Roaming\uv\tools\notebooklm-mcp-cli\Scripts\` |
| Credentials | `C:\Users\lasz\.notebooklm-mcp-cli\profiles\default` |
| Cookie élettartam | 2-4 hét |

**Nem tévesztendő össze:** `PleasePrompto/notebooklm-mcp` (https://github.com/PleasePrompto/notebooklm-mcp) -- npm csomag, Chrome Patchright automatizáció, teljesen más eszköz.

## 2.2. Auth megújítás

Ha `Authentication Error` jön:

```bash
nlm login
# Edge megnyílik → Google bejelentkezés → OK után bezárja magát
nlm notebook list  # ellenőrzés
```

---

# 3. Claude-ból való használat (Cowork session)

## 3.1. Notebook lekérdezés

Claude az alábbi mintával hívja a Windows-MCP PowerShell toolt:

```powershell
$env:PATH = $env:PATH + ";C:\Users\lasz\AppData\Roaming\uv\tools\notebooklm-mcp-cli\Scripts"
nlm query notebook "<NOTEBOOK_ID_VAGY_ALIAS>" "<KÉRDÉS>" --json
```

Visszatérési struktúra (JSON) -- Prompt B aktív esetén:

```json
{
  "value": {
    "answer": "...",
    "conversation_id": "...",
    "sources_used": ["uuid1", "uuid2"],
    "citations": {"1": "uuid1", "2": "uuid2"},
    "references": [
      {"source_id": "uuid1", "citation_number": 1, "cited_text": "..."}
    ]
  }
}
```

Fontos: a `conversation_id`-t meg kell tartani a követő kérdésekhez (`--conversation-id <id>`).

## 3.2. Pipeline lépések CLI-ből

A `nlm` CLI a pipeline lépések nagy részét közvetlenül végrehajtja:

| Lépés | CLI parancs |
|---|---|
| Notebook lista | `nlm notebook list` |
| Lekérdezés | `nlm query notebook <ID> "<kérdés>" --json` |
| Gondolattérkép | `nlm mindmap ...` |
| Kvíz | `nlm quiz ...` |
| Flashcard | `nlm flashcards ...` |
| Dia | `nlm slides ...` |
| Jelentés | `nlm report ...` |
| Pipeline futtatás | `nlm pipeline ...` |
| Cross-notebook | `nlm cross ...` |

---

# 4. Studio outputok exportálása (Export-Tool)

## 4.1. Eszköz

**cced3000/NotebookLM-Export-Tool** -- Edge/Chrome bővítmény, 100% lokális feldolgozás.

| Tulajdonság | Érték |
|---|---|
| GitHub | https://github.com/cced3000/NotebookLM-Export-Tool |
| Típus | Böngészőbővítmény (HTML-alapú) |
| Adatkezelés | 100% lokális, nincs szerveroldali feldolgozás |

## 4.2. Exportálható tartalmak

| Studio output | Elérhető formátumok | Pipeline-relevancia |
|---|---|---|
| Adattáblázat (Data Tables) | CSV, Markdown, Word, PDF | 03, 04, 09 lépések bemenete |
| Gondolattérkép | PNG, SVG, **Markdown** | 05_mindmap_manager bemenete |
| Tanulókártyák | CSV, Markdown, Anki | kész tananyag-elem |
| Csevegési előzmény | Markdown, Word, PDF | 01_html_to_md alternatívája |
| Diasorozat | ZIP, hosszú kép | 08_presentation_maker kiegészítő |
| Kvíz | ❌ fejlesztés alatt | -- |

## 4.3. Mindmap export workflow (05_mindmap_manager)

Az NLM Gondolattérkép funkciója nem promptolható, de exportálható:

```
Studio → Gondolattérkép generálása → Export-Tool → Markdown letöltés
  → N_het/forrasok/mindmap_raw.md
    → 05_mindmap_manager (Claude átformázza Mermaid flowchart LR formátumba)
      → N_Mindmap.md
```

## 4.4. Adattáblázat workflow (Prompt C → projektmappa)

```
Studio → Data Tables → ceruza ikon → Prompt C sablon → Generate
  → Export-Tool → Markdown/CSV letöltés
    → N_het/forrasok/forrasattekinto.md (vagy .csv)
      → Claude pipeline (03, 04, 09 lépések)
```

**Névadás:** Az NLM heurisztikus nevet ad (pl. "Strukturált Forrásáttekintő Táblázat..."). Nem szükséges átnevezni -- Claude a tartalmat dolgozza fel.

---

# 5. Notebook-lista (2026-05-21)

| ID | Cím | Források | Prompt B |
|---|---|---|---|
| c894e121-3c39-4da0-af74-b1f2c82ffa69 | DFT | 9 | ❔ tesztelendő |
| b26582da-9051-4a26-954b-4075013981e4 | Matrix Profile | 7 | ✅ aktív |
| 9a4de53c-b8ea-4db9-8059-2add8a11700a | Dive into Time-Series Anomaly Detection | 1 | ❔ |
| 8732cec4-a875-4afa-b0e1-27743febae1d | Introduction to Wavelets | 16 | ❔ |
| 73a46dcf-c4ed-4148-8143-3b05c2dccbf5 | Áramlási rendellenességek | 41 | ❔ |
| a053ecbf-4e39-4e9d-98e4-ac0063b62262 | Compressor Instabilities | 7 | ❔ |
| 643cfc27-3cb1-4126-bd90-590b64a34402 | Tavakoli | 11 | ❔ |
| fb2b02e6-7735-41f7-81db-73314a164255 | Termográfia a műszaki diagnosztikában | 33 | ❔ |
| db5df32b-a4b2-41f0-b38a-38b3b30be8bc | synchrosqueezing and reassignment | 19 | ❔ |
| cf7bc34a-7d46-44a6-821f-af02260f04ad | Sémák | 3 | ❔ |

Alias beállítása: `nlm alias set <rövidnév> <ID>`

---

# 6. Nyitott kérdések

- `nlm setup add "Claude Code"` -- tesztelendő, ha Claude Code-ot is használunk
- `nlm skill install` -- milyen skill-ek érhetők el?
- Alias-ok beállítása a tantárgy notebookjaihoz
- Cookie megújítás automatizálása (2-4 hetente)
- `PleasePrompto/notebooklm-mcp` HTTP transport tesztelése (potenciálisan jobb toolset)
- Prompt B beállítása a többi notebookban (jelenleg csak Matrix Profile-ban aktív)
- Export-Tool Claude in Chrome-ból való vezérlése (automatizált Studio export)

# Változásjegyzék

- 2026-05-21 -- Fájl létrehozva, tesztelt architektúra dokumentálva; PyPI és GitHub hivatkozás hozzáadva
- 2026-05-21 (rev2) -- Kritikus lelet: Prompt B hat a CLI-re (MP teszt, 28 citation); 1.1 frissítve; 1.2 kiegészítve CLI flag-limitációval; 3.1 JSON struktúra frissítve Prompt B-s példával; 4. fejezet hozzáadva (Export-Tool, mindmap workflow, adattáblázat workflow); notebook-lista Prompt B státusszal bővítve