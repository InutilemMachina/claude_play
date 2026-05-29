---
name: 02_nlm_notebook_setup
title: 02_NLM_NOTEBOOK_SETUP -- NLM Notebook Setup
type: skill
tags: [meta, skill]
status: active
version: 3.0
updated: 2026-05-26
description: NLM notebook létrehozása CLI-vel. Notebook create + source add (PDF/URL) + Prompt B (chat configure) + mindmap create + citations_seed.json UUID-frissítés. Pipeline 02. lépése.
---

# 02_NLM_NOTEBOOK_SETUP

## 1. Cél

Új NLM notebook létrehozása, források feltöltése, Prompt B beállítása, mindmap generálása, és a `citations_seed.json` UUID-mezőinek kitöltése -- teljesen CLI-ből.

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `1_raw_inputs/*.pdf` | 01_references_collector | Letöltött PDF-ek |
| `1_raw_inputs/*.html` | 01_references_collector | Weboldalak |
| `1_raw_inputs/citations_seed.json` | 01_references_collector | Metaadatok, `nlm_uuid: null` |
| `.claude/nlm_prompts.md` | Meta mappa | Prompt B szövege (ASCII változat) |

**Előfeltétel:** `nlm` CLI elérhető és bejelentkezve.

```powershell
$env:PATH = $env:PATH + ";C:\Users\lasz\AppData\Roaming\uv\tools\notebooklm-mcp-cli\Scripts"
nlm --version
```

Ha `Authentication Error`: `nlm login` (Edge megnyílik → Google bejelentkezés; 2-4 hetente szükséges).

## 3. Eljárás

### 3.1. PATH beállítása (minden PowerShell hívásban kötelező)

```powershell
$env:PATH = $env:PATH + ";C:\Users\lasz\AppData\Roaming\uv\tools\notebooklm-mcp-cli\Scripts"
```

### 3.2. Notebook létrehozása

```powershell
nlm notebook create "<tantargy> - <N>. het"
# Kimenet: ID: ff49ac69-0750-4773-bd4d-42536e96be3f
```

Az ID-t jegyezd fel -- minden következő parancshoz kell. Mentsd a `citations_seed.json` `_notebook.id` mezőjébe.

### 3.3. Források feltöltése

**PDF fájlok:**
```powershell
$NB = "<notebook_id>"
$DIR = "C:\Users\lasz\claude_play\test_outputs\<tantargy>\N_het\1_raw_inputs"

nlm source add $NB --file "$DIR\yeh2016_paper.pdf" --title "Matrix Profile I (Yeh 2016)" --wait
# Kimenet: Source ID: 56662e98-04ce-4ba6-9f44-d2c97599eb50
```

**URL forrás:**
```powershell
nlm source add $NB --url "https://stumpy.readthedocs.io/..." --title "STUMPY Tutorial" --wait
```

Minden `source add` kimenetéből jegyezd fel a Source ID-t → `citations_seed.json` `nlm_uuid` mezői.

Minden forrást egymás után kell feltölteni (`--wait` kötelező). A `--wait` legfeljebb 600s-t vár.

### 3.4. Prompt B beállítása

**Kötelező:** `@'...'@` (single-quote heredoc) -- a `@"..."@` szintaxishibát okoz.

```powershell
$promptB = @'
[Prompt B szövege -- lásd nlm_prompts.md §2]
'@

& nlm chat configure $NB --goal custom --prompt $promptB
# Kimenet: ✓ Chat configuration updated
```

A Prompt B ASCII változatát használd (PowerShell encoding-probléma miatt). Az ékezetes változat az NLM webes UI-ban illeszthető be (lásd `nlm_prompts.md` §2).

### 3.5. Mindmap generálása

```powershell
nlm mindmap create $NB --title "<tantargy> <N>. het" --confirm
# Kimenet: Mindmap ID: d74b759b-...
```

A Mindmap ID-t mentsd a `citations_seed.json` `_notebook.mindmap_id` mezőjébe.

⚠️ **Mindmap export (elsődleges módszer):** A Studio Gondolattérkép exportja az egész pipeline sarokköve. A CLI csak szöveges rekonstrukciót ad vissza -- ez nem megbízható. Az export a 08_mindmap_manager feladata (Ultra Explorer bővítmény).

### 3.6. citations_seed.json frissítése UUID-ekkel

```json
{
  "1": {
    "file": "yeh2016_paper.pdf",
    "nlm_uuid": "56662e98-04ce-4ba6-9f44-d2c97599eb50"
  },
  "_notebook": {
    "id": "ff49ac69-0750-4773-bd4d-42536e96be3f",
    "title": "Matrixprofil Teszt - 1. het",
    "url": "https://notebooklm.google.com/notebook/<id>",
    "mindmap_id": "d74b759b-81dc-432d-9229-ccc13331ff89",
    "created": "2026-05-22"
  }
}
```

### 3.7. NLM CLI pipeline parancsok (referencia)

| Lépés | Parancs |
|---|---|
| Notebook lista | `nlm notebook list` |
| Notebook ellenőrzés | `nlm notebook get <id>` |
| Forrás lista | `nlm source list <id>` |
| Studio státusz | `nlm studio status <id>` |
| Prompt B ellenőrzés | `nlm chat configure <id>` |
| Lekérdezés | `nlm query notebook <id> "<kérdés>" --json` |

## 4. Kimenetek

- NLM notebook (online): létrehozva, források indexelve, Prompt B aktív, mindmap kész
- `1_raw_inputs/citations_seed.json`: `nlm_uuid` mezők kitöltve
- `3_raw_outputs/nlm_mindmap_raw.txt`: mindmap szöveges rekonstrukciója (workaround)

## 5. Ellenőrzés

- [ ] `nlm notebook create` sikerült, ID rögzítve
- [ ] Minden forrás feltöltve, Source ID-k rögzítve
- [ ] `nlm chat configure` sikeres (`✓ Chat configuration updated`)
- [ ] `nlm mindmap create` sikeres, Mindmap ID rögzítve
- [ ] `citations_seed.json` `nlm_uuid` mezői kitöltve
- [ ] `nlm notebook get <id>` `source_count` == várt szám

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `Got unexpected extra arguments` | `@"..."@` használva | Csereld `@'...'@`-ra |
| `citations: {}` a query válaszban | Prompt B nem aktív | `nlm chat configure <id>` ellenőrzés |
| Forrás `processing` állapon ragad | NLM szerver lassú | `--wait-timeout` növelése (alap: 600s) |
| `nlm login` szükséges | Cookie lejárt (2-4 hét) | `nlm login` → böngésző megnyílik |
| PPTX feltöltés sikertelen | NLM CLI csak PDF + URL | PPTX → PDF konverzió (Office mentés), majd `--file` |
| HTML feltöltés sikertelen | `--file` csak PDF-et fogad | Nyilvánosan elérhető oldalhoz: `--url "<url>"` |
| Forrásneveket NLM átírja | UI auto-generál nevet | `nlm source list <id>` → Source ID + cím loggolás → `citations_seed.json` |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [nlm_prompts.md](../nlm_prompts.md) -- Prompt B szövege
- [08_mindmap_manager.md](08_mindmap_manager.md) -- mindmap export
### Notebook-lista (ismert notebookok)

| ID | Cím | Prompt B |
|---|---|---|
| c894e121-3c39-4da0-af74-b1f2c82ffa69 | DFT | ❔ |
| b26582da-9051-4a26-954b-4075013981e4 | Matrix Profile | ✅ aktív |
| fb2b02e6-7735-41f7-81db-73314a164255 | Termográfia a műszaki diagnosztikában | ❔ |
| 8732cec4-a875-4afa-b0e1-27743febae1d | Introduction to Wavelets | ❔ |
| 73a46dcf-c4ed-4148-8143-3b05c2dccbf5 | Áramlási rendellenességek | ❔ |
| 5efb3ad6-4858-4c52-b95e-79d6102726ab | meta_file_updates_test - 1. het | ✅ aktív |
| 060c9cfb-4404-4bff-a57b-ec26b4433773 | meta_file_updates_test - 2. het | ✅ aktív |

Alias beállítása: `nlm alias set <rövidnév> <ID>`

## 8. Visszajelzések

- ❔ QUESTION: A user nem érti, miért van 🛑 checkpoint a 02. lépés után. Magyarázat: a checkpoint azért van, mert (1) az NLM notebook + Prompt B + mindmap manuális/CLI lépések, amelyek sikerét ellenőrizni kell, mielőtt a downstream lépések (03 MinerU, 04 DFS query) elindulnak -- ezek a mindmap struktúrájára épülnek; (2) ha a mindmap rosszul generálódik, az egész downstream pipeline csonka. A checkpoint tehát minőségbiztosítási pont, nem forrás-ellenőrzés. Megfontolás: a checkpoint leírása a pipeline.md §4-ben nem egyértelmű -- pontosítás indokolt.

- ✅ `nlm chat configure $NB --response-length longer` (nem `long` -- tesztelve 2026-05-26). Opciók: `default` / `longer` / `shorter`.
- ⚠️ WARNING: `--goal custom --prompt` és `--response-length` NEM adható meg külön parancsokban -- a második hívás visszaállítja a goal-t `default`-ra. Mindig egy parancsban: `nlm chat configure $NB --goal custom --prompt $p --response-length longer`.
- ⚠️ WARNING: Prompt B `@'...'@` heredoc-ban `[tema]` vagy más szögletes zárójeleket tartalmazó szöveg `Got unexpected extra arguments` hibát okoz. Megoldás: a promptot temp fájlba kell írni (`Out-File`), majd `Get-Content -Raw`-val beolvasni stringként.
- 🔲 TODO: **PPTX forrás `nlm_uuid: None` marad -- teljesen hiányzik a tartalomból, figyelmeztetés nélkül (tesztelve 2026-05-28, 2_het).** A `hari2024_slides.pptx` és `hari2024b_slides.pptx` fájlok `nlm_uuid: None` értékkel szerepelnek a `citations_seed.json`-ban -- NLM-be nem tölthetők fel PPTX formátumban. Következmény: az összes NLM lekérdezés (43 db) ezekre egyetlen hivatkozást sem tartalmaz. Az olvasó számára ezek a forrásanyagok láthatatlanok, és a pipeline sehol nem jelzi, hogy 2 forrás kimaradt. Megoldás: (1) `01_references_collector` vagy `02_nlm_notebook_setup` checkpoint figyelmeztetést adjon `nlm_uuid: None` esetén; (2) a Bevezetés szekció megjegyezze, hogy mely források maradtak ki.
- 💬 NOTE: DOC és PPTX fájlok feltöltése `--file`-lal sikertelen (tesztelve 2026-05-27). HTML fájlok lokálisan mentve szintén nem tölthetők fel -- csak `--url`-ként, nyilvánosan elérhető oldalhoz.
- 🔲 TODO: Az NLM UI szerint számos formátum támogatott: pdf, txt, md, docx, csv, pptx, epub, hang- és videóformátumok, képek (png, jpg, stb.). Megvizsgálandó: a CLI `--file` flag mely formátumokat fogadja el ténylegesen, és hogyan illeszkedik ez a pipeline §6 forrástípus-táblázatába. Ha PPTX és DOCX CLI-n is feltölthető, a pipeline §6 ❔ státuszok felülvizsgálandók.
- 💬 NOTE: Notebook-lista frissítendő -- meta_file_updates_test notebookok hozzáadva (§7).
- 🔲 TODO: **NLM Mindmap title angolul generálódott, miközben a tartalom és a DFS queries magyarul futottak (tesztelve 2026-05-28, 2_het).** A `citations_seed.json._notebook.mindmap_title` = `"Dynamics and Diagnostics of Fluid Flow Anomalies"` (angol), de az NLM válaszok és a mindmap export teljes egészében magyarul van (`Áramlástechnikai Gépek Rezgésdiagnosztikája és Üzemzavarai`). A 02. lépés checkpoint-jánál ellenőrizendő, hogy a mindmap generálás során milyen nyelven készül el, és hogy a `mindmap_title` a `citations_seed.json`-ban mindig az export tényleges nevét tükrözi-e.
- 🔲 TODO: A mindmap CLI workaround (`nlm query notebook` → `nlm_mindmap_raw.txt`) nem a Studio vizuális gráfját adja vissza, csak szöveges rekonstrukciót. Megvizsgálandó: van-e natív mindmap-read parancs, vagy automatizálható-e a Studio export (Claude in Chrome MCP).
- 💬 NOTE: A Prompt B ASCII változatot használ a PowerShell encoding-probléma miatt. Az ékezetes változat NLM UI-ban illeszthető be (nlm_prompts.md §2).
- 💬 NOTE: Studio panel mentés (auditálhatóság): `nlm studio` CLI csak `status`, `delete`, `rename` parancsot ismer -- `save`/`export` **NEM érhető el CLI-n** (tesztelve 2026-05-26). A Studio export kizárólag Export-Tool böngészőbővítménnyel lehetséges. Az audit trail manuális lépés.
- ❔ QUESTION: Chrome Extension (Export-Tool / Ultra Explorer) automatizálható-e Claude in Chrome MCP-vel? (Studio Gondolattérkép + Data Tables export)

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-26 | 3.0 | Overhaul: template-alapú átírás; ékezetek visszaállítva; §8 Visszajelzések; pipeline diagram és felesleges szekciók eltávolítva; Auth/telepítés beolvasztva |
| 2026-05-24 | 2.0 | Auth és telepítés beolvasztva (nlm_integration.md); notebook-lista hozzáadva |
| 2026-05-22 | 1.0 | Létrehozva; teljes CLI workflow dokumentálva |
