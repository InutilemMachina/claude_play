---
name: 00b_nlm_notebook_setup
title: 00B_NLM_NOTEBOOK_SETUP -- NLM Notebook Setup
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-05-22
description: NLM notebook letrehozasa CLI-vel. Notebook create + source add (PDF/URL) + Prompt B (chat configure) + mindmap create + citations_seed.json UUID-frissites. Pipeline 00b. lepese -- 00 es 01 kozott.
---

# 00B_NLM_NOTEBOOK_SETUP.MD -- NLM Notebook Setup

_00b. lepes -- 00_references_collector utan, 01_nlm_query_runner elott_

# 1. Cel es helye a pipeline-ban

```
00_references_collector  →  00b_nlm_notebook_setup  →  01_nlm_query_runner  →  ...
```

Ez a lepes teljes egeszeben automatizalt -- nem igenyel manualis NLM UI-használatot.
A `notebooklm-mcp-cli` (`nlm`) CLI-n keresztul vegzi el:

1. Uj NLM notebook letrehozasa
2. Forrasok feltoltese (PDF fajlok + URL-ek)
3. Prompt B beallitasa (Configure Chat / Custom Instructions)
4. Mindmap generalasa
5. `citations_seed.json` UUID-mezok frissitese

**Elofeltetel:** `00_references_collector` lefutott -- `forrasok/` mappa feltoltve,
`citations_seed.json` letezik (`nlm_uuid: null` mezokkel).

**Output:**
- NLM notebook: eletben, forrasok indexelve, Prompt B aktiv, mindmap kesz
- `forrasok/citations_seed.json`: `nlm_uuid` mezok kitoltve
- `forrasok/nlm_mindmap_raw.txt`: mindmap strukturaja szovegkent
- `1_Mindmap.md`: Mermaid flowchart (05_mindmap_manager elvegzi)

# 2. Elofeltetelek

## 2.1. nlm CLI elerhetosege

```powershell
$env:PATH = $env:PATH + ";C:\Users\lasz\AppData\Roaming\uv\tools\notebooklm-mcp-cli\Scripts"
nlm --version
```

Ha nem talalhato: `nlm login` (cookie megujitas, 2-4 hetente szukseges).

## 2.2. Szukseges bemenetek

| Bemeneti fajl | Honnan | Tartalom |
|:--------------|:-------|:---------|
| `N_het/forrasok/*.pdf` | 00_references_collector | Letoltott PDF-ek |
| `N_het/forrasok/*.html` | 00_references_collector | Letoltott weboldalak |
| `N_het/forrasok/citations_seed.json` | 00_references_collector | Metaadatok, `nlm_uuid: null` |
| `.claude/nlm_prompts.md` | Meta mappa | Prompt B szovege (2. szekció, ASCII valtozat) |

# 3. Workflow

## 3.1. PATH beallitasa (minden PowerShell hivasnal kotelezo)

```powershell
$env:PATH = $env:PATH + ";C:\Users\lasz\AppData\Roaming\uv\tools\notebooklm-mcp-cli\Scripts"
```

## 3.2. Notebook letrehozasa

```powershell
nlm notebook create "<tantargy> - <N>. het"
```

**Pelda:**
```powershell
nlm notebook create "Matrixprofil Teszt 2 - 1. het"
# Kimenet: ✓ Created notebook: ...
#            ID: ff49ac69-0750-4773-bd4d-42536e96be3f
```

A visszaadott ID-t jegyezd fel -- minden kovetkezo parancshoz kell.
Ajanlott: mentsd el a `citations_seed.json` `_notebook.id` mezojebe.

## 3.3. Forrasok feltoltese

### 3.3.1. PDF fajlok

```powershell
$NB = "<notebook_id>"
$DIR = "C:\Users\lasz\claude_play\<tantargy>\<N>_het\forrasok"

nlm source add $NB --file "$DIR\yeh2016_paper.pdf" --title "Matrix Profile I (Yeh 2016)" --wait
# Kimenet: ✓ Added source: ...
#            Source ID: 56662e98-04ce-4ba6-9f44-d2c97599eb50
```

A `--wait` flag megvarja a feldolgozas befejezeset (ajanlott, max 600s).
Minden forrást egymás után kell feltolteni -- parhuzamos feltoltes nem tamogatott.

### 3.3.2. URL forrasok

```powershell
nlm source add $NB --url "https://stumpy.readthedocs.io/en/latest/Tutorial_The_Matrix_Profile.html" \
  --title "STUMPY Tutorial (2024)" --wait
```

### 3.3.3. Visszaadott Source ID-k rogzitese

Minden `source add` kimeneteben megjelenik a Source ID. Ezek a `citations_seed.json`
`nlm_uuid` mezoit toltik ki (lasd 3.5. szekció).

## 3.4. Prompt B beallitasa (Configure Chat)

**Fontos:** A Prompt B az NLM `Configure Chat > Custom Instructions` mezoje.
CLI-vel allithato be, es a `nlm query notebook` parancsra is hat -- a JSON kimenet
`citations` es `references` mezoi csak Prompt B mellett lesznek feltoltve.

### 3.4.1. PowerShell heredoc minta (kotelezo forma)

Multiline szoveg atadásához **kizarolag** a `@'...'@` (single-quote) heredoc hasznalhato.
A `@"..."@` (double-quote) valtozot explandal es szintaksis hibat okoz.

```powershell
$NB = "<notebook_id>"

$promptB = @'
# SZEREPKOR ES CEL

Te egy rendkivul preciz, akademiai szintu kutatasi es adatintegracios asszisztens vagy.
Kizarolag a feltoltott forrasokbol dolgozol. Ha egy informacio nem talalhato meg a
forrasokban, jelold meg: A forrasok nem tartalmaznak informaciot a kovetkezore: [tema].

# CITACIOS ES AUDITALASI SZABALYOK

1. KOTELEZO FORRASMEGJELOLES: Minden allitas, numerikus adat, kovetkeztetes vegen
   helyezz el szovegkozi hivatkozast. A generalt szovegbe ird bele a pontos forrasfajl
   nevet kiterjeszetevel (pl. tavak2004.pdf).
2. FORRASNEV-KONVENCION: A forrasokra kizarolag a Sources panelen lathato nevukkel es
   kiterjeszetukkel hivatkozz. Ne rovidits, ne valtoztass a neveken.

# ABRAK ES TABLAZATOK

1. Ha a forrasban abra vagy tablazat talalhato, de nincs sorszama, elemezd a 3 kornyezo
   bekezdesbol.
2. Ha nevtelen abrara hivatkozol, generalj kontextusbol levezetett horgonyt.
3. Ha a folyoszoveg nem hivatkozik az abrara, de az adatok egyeznek, kapcsold ossze.

# KIMENETI FORMATUM

* Valaszaidat strukturalt Markdown formatumban add meg.
* Tablazatokat GFM formatumban generald, minden cellaban forrasattribucioval.
'@

& nlm chat configure $NB --goal custom --prompt $promptB
# Kimenet: ✓ Chat configuration updated
```

**Megjegyzes az ekezetek hianyrool:** A Prompt B ASCII valtozatot hasznal a PowerShell
encoding-problema miatt. Az NLM webes UI-ban az ekezetes valtozat illesztheto be
(lasd `nlm_prompts.md` 2. szekció, kepernyo).

## 3.5. Mindmap generalasa

```powershell
nlm mindmap create $NB --title "<tantargy> <N>. het" --confirm
# Kimenet: ✓ Mind map created
#            ID: d74b759b-81dc-432d-9229-ccc13331ff89
#            Title: Matrix Profile: Foundations and Applications
```

A mindmap ID mentendo a `citations_seed.json` `_notebook.mindmap_id` mezojebe.

### 3.5.1. Mindmap tartalom lekerdezese (CLI workaround)

A CLI-nek nincs natív mindmap-read parancsa (`nlm studio status` csak ID-t ad,
`nlm export artifact` csak Google Docs/Sheets celudat tamogat).

Workaround: a mindmap strukturajat `nlm query notebook` paranccsal kerdezzuk le:

```powershell
nlm query notebook $NB "Listazd a gondolatterkep teljes strukturajat: fofogalmak es minden alhivatkozasuk, hierarchikusan, kotojeles listaval. Az osszes csomopont neve jelenjen meg." --json
```

A kimenet `answer` mezoje tartalmazza a hierarchikus listat --> mentsd el
`forrasok/nlm_mindmap_raw.txt`-be --> 05_mindmap_manager Mermaid-de alakitja.

## 3.6. citations_seed.json frissitese UUID-ekkel

A `source add` es `notebook create` kimenetebol szarmazo ID-kat irazd be a
`citations_seed.json`-be:

```json
{
  "1": {
    ...
    "nlm_uuid": "56662e98-04ce-4ba6-9f44-d2c97599eb50"
  },
  "_notebook": {
    "id": "ff49ac69-0750-4773-bd4d-42536e96be3f",
    "title": "Matrixprofil Teszt 2 - 1. het",
    "url": "https://notebooklm.google.com/notebook/<id>",
    "mindmap_id": "d74b759b-81dc-432d-9229-ccc13331ff89",
    "created": "2026-05-22"
  }
}
```

A `_notebook` kulcs egy informalis metadata blokk -- a `04_citations_maker` figyelmen
kivul hagyja (numerikus kulcsokat dolgoz fel).

# 4. Ellenorzo lista

- [ ] `nlm notebook create` sikerult, ID rogzitve
- [ ] Minden forrás (`*.pdf`, `*.html`) feltoltve, Source ID-k rogzitve
- [ ] `nlm chat configure` sikeres (`✓ Chat configuration updated`)
- [ ] `nlm mindmap create` sikeres, Mindmap ID rogzitve
- [ ] `citations_seed.json` `nlm_uuid` mezoi kitoltve
- [ ] `nlm_mindmap_raw.txt` elmentve
- [ ] `nlm notebook get <id>` visszaigazolja: `source_count` == vart szam

# 5. Hasznos diagnosztikai parancsok

```powershell
# Notebook ellenorzese
nlm notebook get <id>

# Forrasok listaja
nlm source list <id>

# Studio artifaktok (mindmap status)
nlm studio status <id>

# Prompt B ellenorzese
nlm chat configure <id>  # aktualis beallitas megjelenitese
```

# 6. Ismert korlatok

| Problema | Ok | Megoldas |
|:---------|:---|:---------|
| `Got unexpected extra arguments` | `@"..."@` helyett `@'...'@` kell | Csereld le a heredoc tipusat |
| `citations: {}` a query valaszban | Prompt B nincs aktivan | Ellenorizd: `nlm chat configure <id>` |
| Forras `processing` allapoton ragad | NLM szerver lassu | Noveld a `--wait-timeout` erteket (alapert. 600s) |
| `nlm login` szukseges | Cookie lejart (2-4 het) | `nlm login` -> bongeszo megnyilik |

# 7. Kapcsolodo fajlok

| Fajl | Keletkezik | Felhasznalo |
|:-----|:-----------|:------------|
| `forrasok/citations_seed.json` | 00, **00b** (UUID-kkel frissitve) | 04_citations_maker |
| `forrasok/nlm_mindmap_raw.txt` | **00b** | 05_mindmap_manager |
| NLM notebook (online) | **00b** | 01_nlm_query_runner |

# Valtozasnaplo

- 2026-05-22 -- Letrehozva; teljes CLI workflow dokumentalva (matrixprofil_teszt_2 PoC alapjan)

# Ismert hibák

→ [pitfalls.md §2.4](../pitfalls.md) -- Multiline prompt: @'...'@ kötelező
→ [pitfalls.md §2.3](../pitfalls.md) -- PowerShell query timeout

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
