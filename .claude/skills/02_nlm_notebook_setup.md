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
| `Got unexpected extra arguments` | `@"..."@` vagy `[...]` szögletes zárójelek a heredocban | Csereld `@'...'@`-ra; a `[tema]` típusú placeholder szöveget távolítsd el |
| `citations: {}` a query válaszban | Prompt B nem aktív | `nlm chat configure <id>` ellenőrzés |
| Második `configure` parancs visszaállítja a goal-t | `--goal` és `--response-length` külön hívva | Mindig egy parancsban: `--goal custom --prompt $p --response-length longer` |
| Prompt B többsoros heredoc `Got unexpected extra arguments` | PS 5.1 a newline-t argumentumhatárként értelmezi | Bypass: egysorossá tömörített prompt; `VALASZOLJ KIZAROLAG MAGYARUL` az első sor legyen |
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

- 🔲 TODO: **PPTX forrás `nlm_uuid: None` marad -- teljesen hiányzik a tartalomból, figyelmeztetés nélkül (tesztelve 2026-05-28, 2_het).** A `hari2024_slides.pptx` és `hari2024b_slides.pptx` fájlok `nlm_uuid: None` értékkel szerepelnek a `citations_seed.json`-ban -- NLM-be nem tölthetők fel PPTX formátumban. Megoldás: (1) checkpoint figyelmeztetést adjon `nlm_uuid: None` esetén; (2) a Bevezetés szekció megjegyezze, hogy mely források maradtak ki.
- 💬 NOTE: DOC és PPTX fájlok feltöltése `--file`-lal sikertelen (tesztelve 2026-05-27). HTML fájlok lokálisan mentve szintén nem tölthetők fel -- csak `--url`-ként, nyilvánosan elérhető oldalhoz.
- 💬 NOTE: Notebook-lista frissítendő -- meta_file_updates_test notebookok hozzáadva (§7).
- 💬 NOTE: A mindmap `_notebook.mindmap_title` angolul generálódhat, miközben a tartalom magyarul van. A 02 checkpoint-nál ellenőrizd a mindmap nyelvét (tesztelve 2026-05-28, 2_het).
- 💬 NOTE: A Prompt B ASCII változatot használ a PowerShell encoding-probléma miatt. Az ékezetes változat NLM UI-ban illeszthető be (nlm_prompts.md §2).
- 💬 NOTE: Studio panel mentés (auditálhatóság): `nlm studio` CLI csak `status`, `delete`, `rename` parancsot ismer -- `save`/`export` **NEM érhető el CLI-n** (tesztelve 2026-05-26). Az audit trail manuális lépés.
- 🔲 TODO: **Forrásnyelv-ellenőrzés a 02 checkpoint-nál.** Ha a feltöltött források nem magyarok, az NLM válaszok valószínűleg angolul lesznek. Figyelmeztetés helye: pipeline.md §4 checkpoint szövege.
- 🔲 TODO: **Általános NLM UI copy-paste útmutató hiányzik.** Szükséges lista: Prompt B → Configure Chat; Prompt C → Studio Data Tables; mindmap → Ultra Explorer → `3_raw_outputs/nlm_mindmap_export.md`.
- 🔲 TODO: **NLM forráspanel parse-hiba nincs detektálva (tesztelve 2026-05-30, mini2).** `nlm source add` sikeres kóddal tér vissza, de a forrás az NLM-ben piros (tartalom nélküli). Megoldás: `nlm source list <NB_ID>` a checkpoint-nál, `status != ready` szűrés.
- 🔲 TODO: **Retroaktív forrás-hozzáadás protokollja hiányzik.** Ha a user 02 után helyez el új forrást: (1) átnevezés; (2) URL visszakeresés; (3) `nlm source add --url`; (4) `citations_seed.json` bővítése. (Tesztelve 2026-05-30, mini2.)

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-31 | 3.2 | 3. hét cleanup: 3 tétel §9 (mindmap CLI korlát ✅, Chrome Extension ❔ duplikáció ✅, CLI formátum kutatás ✅ → jövőbeli sprint) |
| 2026-05-30 | 3.1 | K0 cleanup: ❔ checkpoint-kérdés lezárva; 4 ⚠️ WARNING áthelyezve §6-ba; mindmap_title NOTE-ra konvertálva |
| 2026-05-26 | 3.0 | Overhaul: template-alapú átírás; ékezetek visszaállítva; §8 Visszajelzések; pipeline diagram és felesleges szekciók eltávolítva; Auth/telepítés beolvasztva |
| 2026-05-24 | 2.0 | Auth és telepítés beolvasztva (nlm_integration.md); notebook-lista hozzáadva |
| 2026-05-22 | 1.0 | Létrehozva; teljes CLI workflow dokumentálva |
