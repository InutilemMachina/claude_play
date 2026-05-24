---
title: PITFALLS.MD -- Ismert problémák és gyökéroka-megoldások
type: meta
tags: [meta, debug]
updated: 2026-05-23
description: Pipeline futás közben felfedezett hibák, gyökérokaik és bevált megoldásaik. Session elején opcionálisan beolvasható.
---
QUESTION: Az egyes hibák miért nincsenek szétdobva a saját folyamatukat érintő fájlokba?

# Pitfalls -- Ismert Problémák és Megoldások

# 1. Fájlírási problémák

## 1.1. Write tool JSON csonkítás

**Tünet:** `citations_seed.json` vagy más JSON fájl az utolsó néhány sorban csonkul
(pl. `"note": "Interaktiv Python tutorial -- dida` -- mondat közepén vágódik el).
JSON parsing `JSONDecodeError: Unterminated string` hibával jelzi.

**Gyökérok:** A Write/Edit tool belső puffermérete nem kezeli megbízhatóan a ~3-4 KB
feletti, ékezetes karaktereket tartalmazó JSON fájlokat.

**Megoldás:** JSON fájlokat **bash `cat > fájl << 'HEREDOC'`** mintával kell írni,
nem Write tool-lal. A heredoc single-quote (`'HEREDOC'`) megakadályozza a változó-expanziót.

```bash
cat > /path/to/file.json << 'JSONEOF'
{
  "kulcs": "érték"
}
JSONEOF
```

**Érintett fájlok:** `citations_seed.json`, `citations.json` (minden JSON output).

## 1.2. PowerShell Out-File UTF-8-sig + CRLF

**Tünet:** `nlm query notebook ... | Out-File fajl.txt -Encoding utf8` kimenetét
Python `json.loads()` `JSONDecodeError`-rel dobja vissza, bár a fájl látszólag helyes.

**Gyökérok:** A PowerShell `-Encoding utf8` BOM-os UTF-8-et (`utf-8-sig`) és Windows
CRLF sortörést (`\r\n`) ír. A standard Python `json.loads()` a BOM-ot érvénytelen
karakterként értelmezi.

**Megoldás:** Python-ban kötelező olvasási minta:

```python
raw = Path("fajl.txt").read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
obj = json.loads(raw)
```

# 2. NLM CLI problémák

## 2.1. Üres citations/references mezők rövid query-nél

**Tünet:** `nlm query notebook` JSON kimenetében `"citations": {}` és `"references": []`,
bár az `answer` szöveg tartalmaz `[fajlnev.pdf: 43]` inline hivatkozásokat.

**Gyökérok:** Az NLM csak hosszabb, több szekciót érintő query esetén tölti fel a
strukturált `citations` mezőt. Rövid (~50-80 kar) kérdésnél ez elmarad.

**Megoldás:**
1. Q1 legyen a leghosszabb, legátfogóbb query -- ebből épül a `citations.json`.
2. Q2/Q3 inline citációiból (`[fajlnev.pdf: oldal]` regex) kinyert fájlneveket
   mappeld vissza a `citations_seed.json` UUID-jeivel.

Részletes implementáció: `skills/01_nlm_query_runner.md` §5.4.

## 2.2. references mezo struktúrája (nem {id: ...})

**Tünet:** `r["id"]` KeyError a references iterációjánál.

**Gyökérok:** A `references` lista elemei `{source_id, citation_number, cited_text}`
struktúrájúak -- **nem** `{id, ...}`.

**Megoldás:** `{r["source_id"]: r for r in val["references"]}` lookup dict.


## 2.3. PowerShell tobbsoros --prompt argument tores

**Tunet:** `nlm chat configure <ID> --goal custom --prompt $variable` hibaval dob:
`Got unexpected extra arguments (...)` -- a prompt szovege szokoznél szetdarabolodik.

**Gyokérok:** PowerShell here-string (`@'...'@`) valtozot native command-nak atadva
a CLI a szokozokat es sortoreseket argumentum-határkent ertelmezi.

**Megolddas:** Python subprocess-en keresztul hivni a CLI-t:

```python
subprocess.run(
    [r'path\to\nlm.exe', 'chat', 'configure', notebook_id,
     '--goal', 'custom', '--prompt', prompt_text],
    capture_output=True, text=True
)
```
## 2.3. PowerShell query timeout

**Tünet:** `MCP error -32001: Request timed out` hosszú query szövegnél.

**Gyökérok:** Az MCP PowerShell híd alapértelmezés szerint 30 másodperces timeout-ot
alkalmaz. Hosszú NLM lekérdezések (részletes, több alfejezetes kérdések) ezt túllépik.

**Megoldás:**
- A query szöveget tartsd 100 karakternél rövidebbre.
- Ha hosszabb kell: `mcp__Windows-MCP__PowerShell` `timeout` paramétert növeld (`45`+).
- Vagy bontsd szét több rövidebb query-re.

## 2.4. PowerShell multiline prompt: @'...'@ kötelező

**Tünet:** `nlm chat configure ... --prompt $szoveg` -- `Got unexpected extra arguments` hiba.

**Gyökérok:** A `@"..."@` (double-quote) heredoc változót expandál és sortöréseket
argumentum-határokként értelmez. A `$promptB` tartalma több argumentumként kerül a CLI-hez.

**Megoldás:** Kizárólag `@'...'@` (single-quote) heredoc a multiline prompt átadásához:

```powershell
$prompt = @'
# FEJLEC
Szoveg itt...
'@
& nlm chat configure $NB --goal custom --prompt $prompt
```

# 3. Python script problémák

## 3.1. heading_numberer.py: startswith vs == az unnumbered szekciókhoz

**Tünet:** `## 3.3. Forrásjegyzék regenerálása` -- a `3.3.` prefix eltűnik, mert
a skill `_is_unnumbered("Forrásjegyzék regenerálása")` `startswith("forrasjegyzek")`-kel
igaz értéket ad vissza.

**Gyökérok:** `startswith` prefix-illesztés a teljes fejléc-szövegen -- ha a fejléc
az unnumbered szóval *kezdődik* (pl. "Forrásjegyzék XYZ fejezet"), is unnumbered-nek
minősül.

**Megoldás:** Pontos egyezés: `normalized == pat` -- csak a tisztán az unnumbered
szóból álló fejlécek lesznek számozatlanok.

## 3.2. 03_excerpt_block_maker: `<!-- Q:N -->` marker belekerül a body_lines-ba

**Tünet:** Az utolsó `###` szekció `💡 Lényeg` blockquote-ja a `<!-- Q:N -->` marker
UTÁN jelenik meg (helyes: előtte kellene).

**Gyökérok:** A body-gyűjtő while loop csak `##` és `###` kezdetű soroknál áll meg.
A `<!-- Q:N -->` HTML komment áttételesen body-ba kerül, és `continue` után a főciklus
a következő `##`-t kapja meg. Az ott lévő 🗺️-ellenőrző ág sosem fut le (a `##` handler
`continue`-val ugrik ki előbb).

**Megoldás:** Javító script: (1) a Q:N marker körüli sorrendcsere, (2) 🗺️ blokkok
utólagos befűzése. Lásd `fix_blocks.py` minta a `03_excerpt_block_maker` dokumentációjában.

**Megelőzés:** A body-gyűjtő loop feltételét ki kell terjeszteni:
`if peek.startswith("## ") or peek.startswith("### ") or re.match(r'^<!-- Q:\d+ -->', peek): break`

## 3.3. 04_citations_maker: az assembly lépés nem konvertál minden hivatkozástípust

**Tünet:** `1_Jegyzet.md` assembly után maradnak nyers citációk:
- Multi-file: `[yeh2016_paper.pdf: 43, zhu2016_paper.pdf: 605]`
- Q1 tartomány: `[3-5]`, `[11-14]`, `[22, 24, 27-29]`

**Gyökérok:** A `01_nlm_query_runner` assembly script csak a következőket kezeli:
- Q1 JSON citations (`[N]`, `[N, M]` egészek) → global sup
- Q2/Q3 egyszerű `[fajlnev.pdf: oldal]` egyfájlos pattern

Nem kezeli: (a) multi-file vesszős listákat Q2/Q3-ban, (b) Q1 tartomány-hivatkozásokat.

**Megoldás:** A `04_citations_maker` lépésben utólagos pótlás:
1. `MULTI_RE` regex: `\[(?:[A-Za-z0-9_]+\.(?:pdf|html):[^\]]+)\]` -- fájlneveket extraktál,
   globálisra cseréli a `file_to_global` map alapján.
2. Q1 LOCAL: teljes `q1_local_to_global` map a `nlm_q1_raw.txt` `citations` dict-jéből,
   tartomány-expandálással (`3-5` → `[3, 4, 5]` → globális sup-ok).
3. Csak a `<!-- Q:1 -->` és `<!-- Q:2 -->` közötti szövegre alkalmazza a LOCAL cserét.

# 4. Figure pipeline problémák

## 4.1. MinerU extra `auto/` könyvtárszint

**Tünet:** A `build_figure_catalog.py` `source_stem = cl_file.parent.name` hívása
`"auto"` névvel tér vissza, nem a forrás nevével (pl. `"yeh2016_paper"`).

**Gyökérok:** MinerU nem `kepek/yeh2016_paper/` alá írja az outputot, hanem
`kepek/yeh2016_paper/auto/` alá. Ez egy extra könyvtárszint.

**Megoldás:** `source_stem = cl_file.parent.parent.name` (két szinttel felfelé).
A `rel_path`-ben is `auto/images/` szerepel: `forrasok/kepek/{source_stem}/auto/images/{new_name}`.

## 4.2. MinerU HTML forrást nem tud feldolgozni

**Tünet:** `stumpy2024_webpage.html` kimarad a MinerU feldolgozásból.

**Gyökérok:** MinerU dokumentum-konverterként (PDF, DOCX stb.) működik, nem
weboldal-rendererekként. HTML esetén nincs elérhető PDF-minőségű ábrakivonás.

**Megoldás:** Weboldalt PDF-ként kell menteni (Edge: nyomtatás → Save as PDF,
vagy SingleHTML bővítmény), majd a PDF kerül a `forrasok/` mappába.

## 4.3. `conda run` + PowerShell Start-Job: visszatér, mielőtt MinerU befejezne

**Tünet:** `Start-Job` befejezettnek jelöli a conda run hívást (pl. 15 sec alatt),
de a MinerU Python processz még fut a háttérben.

**Gyökérok:** `conda run` bizonyos konfigurációban nem vár a gyermekprocessz
befejezésére -- visszatér, amint a subprocess elindult.

**Megoldás:** MinerU futtatása manuálisan Git Bash-ből szinkron módon -- ez az
egyszerűbb és megbízhatóbb megközelítés. Kávészünet-lépés: 1-5 perc/PDF.

## 4.4. Hosszú PDF-ek: MinerU futási idő

**Tünet:** `yeh2018_paper.pdf` (170 oldal) esetén MinerU 10-30+ percig fut;
felhasználó kénytelen manuálisan leállítani.

**Gyökérok:** MinerU oldalanként dolgoz, lineárisan.

**Megoldás:** `mineru_pdf.py` automatikus figyelmeztetés 50 oldal felett
(pypdf page count check). Interaktív megerősítés kérése; `--yes` flag
az automatizált futtatáshoz.

```bash
python scripts/mineru_pdf.py 1_het/forrasok/ --output 1_het/forrasok/kepek/
# 50+ oldalas PDF-nél rákérdez; --yes flaggel kihagyható
```

# Változásjegyzék

- 2026-05-22 -- Létrehozva (matrixprofil_teszt_2 PoC futás tapasztalatai alapján)
- 2026-05-22 -- 3.2-3.3 hozzáadva: excerpt_block_maker marker-sorrend bug; citations assembly hiányos konverzió
- 2026-05-23 -- 4. fejezet: figure pipeline pitfalls hozzáadva (4.1-4.4)

## §5. NLM Studio UI funkciók vs. pipeline

### §5.1. NLM ábragaléria nem érhető el CLI-n

**Tünet:** Az NLM Studio "Notebook guide" ábragalériája vizuálisan látható, de `nlm query notebook` nem adja vissza.
**Gyökérok:** Az ábragaléria a webUI-ban renderelt funkció, nem CLI végpont.
**Megoldás:** Pipeline ábraforrása kizárólag MinerU (`figure_catalog.json`). NLM ábragaléria nem szükséges.

### §5.2. NLM mindmap CLI-n ELÉRHETŐ -- integrálni kell

**Tünet:** Korábban UI-only-nak hittük, de `nlm mindmap create <notebook_id> --confirm` CLI-n is fut.
**Kimenet:** Studio artifaktot generál (nem JSON/Mermaid -- formátum tesztelendő).
**Teendő:** Tesztelni, hogy az output alkalmas-e Mermaid-konverzióra, és ha igen, `05_mindmap_manager`-be integrálni `nlm_query.py mindmap` parancson keresztül.

### §5.3. HTML forrás képei elvesznek --text feltöltésnél



**Tünet:** `nlm source add --text <html_szöveg>` csak a szöveget adja át, az <img> tagek által hivatkozott képek nem kerülnek be.
**Gyökérok:** A `--text` opció plain text / stripped HTML, nem renderelt DOM.
**Megoldás:** Ha a HTML nyilvánosan elérhető: `--url` opció. Ha lokális: PDF-konverzió (wkhtmltopdf). Ha csak szöveg kell: elfogadható veszteség.

## §6. Karakterkódolás

### §6.1. CP1250-mojibake PowerShell fájlszerkesztésnél

**Tünet:** A PowerShell `[System.IO.File]::ReadAllText` + string replacement + `WriteAllText` utáni `.md` fájlokban a magyar karakterek (`á`, `é`, `ő` stb.) CP1250-mojibake formában jelennek meg (pl. `á`, `é`, `Ĺ'`).
**Gyökérok:** A PowerShell MCP híd a stdout-ot CP1250-ként adja vissza; a string-cserék az eredeti UTF-8 byte-okat CP1250-ként értelmezik, majd UTF-8-ba visszakódolva dupla kódolás keletkezik.
**Megoldás:**
1. Fájl-szerkesztésre az Edit tool használata (nem PowerShell WriteAllText).
2. NLM lekérdezések mentéséhez: `scripts/nlm_query.py` Python subprocess-en keresztül (`encoding='utf-8'`).
3. Utólagos javítás: `utf8_bytes.decode('cp1250')` táblával csere -- de kerülendő.
**Érintett fájlok (javítva 2026-05-23):** `.claude/pipeline.md`, `.claude/pitfalls.md`, `.claude/skills/00c_mineru_extractor.md`.

## 06_notes_collector -- TOC insert silent fail (2026-05-24)

**Tünet:** Tárgymutató nem jelenik meg a Jegyzetben, de a script hibát nem dob.
**Gyökérok:**  nem talált egyezést, mert a frontmatter után csak 1 sortörés volt ().
**Megoldás:**  rugalmas mintával -- 1 vagy több sortörés elfogadása.
**Státusz:** ✅ Javítva 2026-05-24.

## 06_notes_collector -- TOC insert silent fail (2026-05-24)

**Tünet:** Tárgymutató nem jelenik meg a Jegyzetben, de a script hibát nem dob.

**Gyökérok:** str.replace pontos string-egyezést keres. A frontmatter után 1 sortörés volt, nem 2.

**Megoldás:** re.sub rugalmas mintával -- (---\n+)(# 1_Jegyzet) -- 1 vagy több sortörés elfogadása.

**Státusz:** Javítva 2026-05-24.

## SingleFile CLI -- Windows-MCP-ből nem futtatható (2026-05-24)

**Tünet:** `single-file <url> out.html` futtatás Windows-MCP PowerShell-hídon keresztül: `Process exited with code 2147483651` (0x80000003 STATUS_BREAKPOINT).

**Gyökérok:** A Windows-MCP sandboxolt folyamatkörnyezetben a headless Chromium (CDP) indítása blokkolva van. Nem Edge-konfiguráció, hanem process isolation probléma.

**Mi NEM működik Claude-ból:**
- `single-file <url>` bármilyen `--browser-args` kombinációval
- `--browser-headless=false` sem segít
- Docker alternatíva: nem telepített
- `--browser-args` JSON-parse bug: `--no-sandbox` dashes = "negative number" hiba

**Helyes workflow:**
- SingleFile mentés: 👤 manuális lépés (felhasználó Edge-bővítménnyel ment)
- NLM-be kerülő forrás: mindig URL (`nlm source add --url`) -- nem lokális HTML
- Lokális HTML célja: archiválás + képkinyerés (MinerU, 05b pipeline)

**Státusz:** Elfogadott korlát. 00_references_collector skill-ben jelölendő (👤).
