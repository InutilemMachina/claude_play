---
name: 04_nlm_query_runner
title: 04_NLM_QUERY_RUNNER -- NLM Query Runner
type: skill
tags: [meta, skill]
status: active
version: 2.0
updated: 2026-05-26
description: NLM notebook lekérdezése CLI-n keresztül. Mindmap DFS alapján tematikus queryek + Qfig (figura/táblázat katalógus), raw JSON mentés, citations.json inicializálása.
---

# 04_NLM_QUERY_RUNNER

## 1. Cél

Az NLM notebook mindmap-jét Depth-First-Search sorrendben bejárva tematikus lekérdezéseket futtat, a nyers válaszokat elmenti, és inicializálja a `citations.json`-t.

## 2. Bemenetek

- NLM notebook ID (02_nlm_notebook_setup kimenet)
- `4_wip_outputs/N_Mindmap.md` (08_mindmap_manager kimenet) -- a query-témák forrása
- `1_raw_inputs/citations_seed.json` -- UUID-mapping referencia

**Előfeltétel:** 02 (notebook + Prompt B aktív) és 08 (mindmap export) lefutott.

## 3. Eljárás

### 3.1. PATH beállítása

```powershell
$env:PATH = $env:PATH + ";C:\Users\lasz\AppData\Roaming\uv\tools\notebooklm-mcp-cli\Scripts"
```

### 3.2. Mindmap-vezérelt DFS lekérdezések

Az NLM belső query-sablonja szint szerint:

```
Gyökér (1. szint):
"Beszélgessen az ezekben a forrásokban tárgyalt <fő node> témakörről."

2. szint (gyerek):
"Beszélgessen az ezekben a forrásokban tárgyalt,
 a(z) <szülő node> tágabb kontextusába tartozó <gyerek node> témakörről."

3. szint (unoka):
"Beszélgessen az ezekben a forrásokban tárgyalt,
 a(z) <szülő node> tágabb kontextusába tartozó <unoka node> témakörről."
```

**Fontos:** A `<szülő node>` mindig az egy szinttel feljebb lévő csomópont -- nem a gyökér.

**ASCII-korlát:** Ha a CLI csonkítja az outputot ékezetes kérdésnél, ASCII fallbacket küldj.

**Példa (Termográfia, 1. hét):**
```powershell
$NB = "<notebook_id>"

# Gyökér query
$q1 = "Mi az infravoros termografia, miert fontos mernoki es diagnosztikai szempontbol?"
nlm query notebook $NB $q1 --json | Out-File 3_raw_outputs/nlm_q1_raw.txt -Encoding utf8

# 2. szint: Sugárzásfizika
$q2 = "Beszelgessen az ezekben a forrasokban targyalt, a(z) Infravoros termografia tagabb kontextusaba tartozo Sugarzasfizikai alaptorvenyek temakorrol -- reszletesen."
nlm query notebook $NB $q2 --json | Out-File 3_raw_outputs/nlm_q2_raw.txt -Encoding utf8

# Folytatás ugyanabban a konverzációban
nlm query notebook $NB $q3 --conversation-id <conv_id> --json | Out-File 3_raw_outputs/nlm_q3_raw.txt -Encoding utf8
```

A `conversation_id`-t az első lekérdezés visszaadja -- meg kell tartani a követő kérdésekhez.

⚠️ **Napi kvóta:** Az NLM-nek napi kérdéslimit-je van. `RESOURCE_EXHAUSTED` hiba esetén várj, és használd a `--resume --sleep 5` flageket (lásd §6).

### 3.3. Qfig -- figura és táblázat lekérdezés

A Qfig egy **egyszer futtatott** speciális query, amelyet **Q1 előtt** kell futtatni:

```powershell
$qfig = "Sorold fel az osszes abrat, diagramot es tablazatot a feltoltott forrasokbol. Minden elemhez add meg pontosan: FORRAS: fajlnev kiterjesztessel. SZAM: az abra/tablazat sorszama. ALAIRAS: az eredeti caption szo szerint. LEIRAS: 1-2 mondatos sajat leiras. TEMAKÖR: 2-3 kulcsszo angolul."
nlm query notebook $NB $qfig --json | Out-File 3_raw_outputs/nlm_qfig_raw.txt -Encoding utf8
```

A `03-1_qfig_parser.py` a Qfig outputból tölti fel a `figure_catalog.json` `caption` + `keywords` mezőit.

### 3.4. citations.json inicializálása

Python olvasáshoz (kötelező UTF-8-sig + CRLF kezelés):
```python
raw = Path("nlm_q1_raw.txt").read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
obj = json.loads(raw)
val = obj.get("value", obj)
```

**Stratégia:**
1. Q1 JSON `citations` mező → UUID dedup → `citations.json` inicializálás
2. Q2-Q4 JSON citations → hozzáadás dedup logikával
3. Inline fallback: `answer` mezőkből `\[([^:]+\.pdf)\]` regex → `citations_seed.json` UUID-mapping

**Elvárt végeredmény:** `set(citations_seed uuid-k) == set(citations.json nlm_uuid-k)`

### 3.5. Szekció-markerek injektálása

Minden query-forrású blokk elé `<!-- Q:N -->` kerül a Jegyzet-összeállítás során -- a `07_citations_renumber.py` per-szekció renumberinghez.

```markdown
<!-- Q:2 -->
## 2. Alapfogalmak
...
<!-- Q:3 -->
## 3. Algoritmusok
```

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `3_raw_outputs/nlm_qfig_raw.txt` | Qfig: ábra/táblázat katalógus (NLM Vision kimenet) |
| `3_raw_outputs/nlm_q1_raw.txt` ... `nlm_qN_raw.txt` | Tematikus NLM CLI JSON kimenet (Prompt B) |
| `3_raw_outputs/citations.json` | UUID-alapú forrásregiszter (04 inicializálja, 07 karbantartja) |

## 5. Ellenőrzés

- [ ] Minden tervezett query (Qfig + Q1..QN) lefutott
- [ ] `nlm_q*_raw.txt` fájlok nem üresek, `answer` mező nem null
- [ ] `citations.json` létezik, bejegyzések száma >= notebookba töltött forrásszám
- [ ] `<!-- Q:N -->` markerek injektálva a Jegyzet-vázlatba

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `citations: {}` üres a JSON-ban | Prompt B nem aktív, vagy query túl rövid | `nlm chat configure <id>` ellenőrzés; ha aktív → inline regex fallback (§3.4) |
| `r["id"]` KeyError references iterációnál | `references` elemei `{source_id, citation_number, cited_text}`, nem `{id, ...}` | `{r["source_id"]: r for r in val["references"]}` lookup dict |
| `MCP error -32001: Request timed out` | MCP alapértelmezett 30 s timeout | Query szöveget tartsd <100 kar; vagy `--timeout 180` flag |
| `Got unexpected extra arguments` multiline promptnál | `@"..."@` double-quote heredoc expandál | Kizárólag `@'...'@` single-quote heredoc: `$prompt = @'...'@; & nlm ... --prompt $prompt` |
| `RESOURCE_EXHAUSTED` JSON hiba minden query-n | Napi NLM kvóta kimerítve | Várj kvóta-reset-ig (éjfél PT); `--resume --sleep 5` flagekkel folytasd: `python 04_nlm_dfs_queries.py --resume --sleep 5 --week-dir ...` |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [08_mindmap_manager.md](08_mindmap_manager.md) -- a query-témák forrása
- [07_citations_maker.md](07_citations_maker.md) -- citations.json karbantartás

## 8. Visszajelzések

- 🔲 TODO: Minden NLM lekérdezés válaszát a Studio panelbe is menteni kell (auditálhatóság, reprodukálhatóság). Jelenlegi állapot: csak `3_raw_outputs/nlm_q*.txt`-be kerül, Studio-ba nem. Megvizsgálandó: `nlm studio artifact save` parancs elérhető-e CLI-n; ha nem, 😎 manuális lépés (Studio jobboldali panel → Mentés). Prioritás: a Studio-ba mentett tartalmak újra felhasználhatók és kereshetők NLM-en belül.
- ✅ `nlm chat configure $NB --response-length longer` (nem `long`). A `nlm query notebook` timeout növelhető: `--timeout 180` flag (default: 120s).
- 🔲 TODO: A Qfig query eredete nem egyértelmű a user számára (tesztelve 2026-05-27). A prompt (`Sorold fel az osszes abrat...`) a §3.3-ban van definiálva, de a pipeline.md IO táblázata csak `scripts/03-1_qfig_parser.py -- Qfig query` szövegre hivatkozik -- nem derül ki, hogy ez egy NLM CLI lekérdezés, amelyet Claude futtat le. A 03-1 sor inputjaként `NLM notebook (🔌)` szerepel, de ez nem magyarázza, hogy milyen kérdést tesz fel Claude. Javítandó: a pipeline.md IO táblában a Qfig sort bővíteni: `scripts/03-1_qfig_parser.py -- Qfig query (04 §3.3 prompt)`.
- 🔲 TODO: A Qfig lekérdezés eredménye (`nlm_qfig_raw.txt`) mentési helye és státusza nem konzisztensen nyomon követett -- a §3.3 rögzíti az elvárt helyet, de a korábbi teszten ez nem volt lementve. A checklist ezt tartalmazza.
- 🔲 TODO: Formátum-eltérés a Qfig NLM output és a `03-1_qfig_parser.py` között (tesztelve 2026-05-27). A parser per-soros `FORRAS: érték` formátumot vár (FIELD_RE regex), de az NLM Markdown táblázatot ad vissza (`| FORRAS | SZAM | ALAIRAS | ... |`). Eredmény: 0 entry parse-olva mindkét hétre (1_het: 9 katalógusbejegyzés, 2_het: 34 — mind 0 match). Megoldás: vagy a Qfig prompt módosítandó ("adj per-soros listát"), vagy a parser bővítendő Markdown-tábla támogatással. Prioritás: magas (03-1 jelenleg teljesen inaktív).
- 🔲 TODO: Függőségi ellentmondás (tesztelve 2026-05-27): `scripts/04_nlm_dfs_queries.py` sor 171 megköveteli `3_raw_outputs/nlm_mindmap_export.md` fájlt, amely a **08_mindmap_manager** kimenete (Ultra Explorer bővítmény, manuális export). A pipeline.md IO táblázata szerint a sorrend `02→03→04→...→08`, vagyis 04 fut 08 előtt -- de a DFS script nem fut 08 nélkül. Következmény: 04 nem hajtható végre, amíg a mindmap exportot a user manuálisan el nem végzi (NLM Studio → Ultra Explorer → `nlm_mindmap_export.md`). A pipeline.md §3-ban rögzített "helyes sorrend" módosítandó: `02 (mindmap generálás) → 03 (MinerU) → 08 (mindmap export) → 04 (DFS lekérdezések)`.
- 🔲 TODO: Az NLM absztrakt szövegét (középső panel) Q1 helyett vagy Q1 előtt kellene lekérdezni: `nlm query <id> "Adj egy absztraktot a témakörben."`. Ez reprodukálhatóbb bevezető, mint a generált Q1.
- 🔲 TODO: **Vizuális progress megjelenítés hiányzik (tesztelve 2026-05-27).** A user nem látja a DFS futását. Elvárt: egy terminálablak (pl. `Start-Process` Windows Terminal), amely valós időben mutatja: `[1/2 hét] [5/41 kérdés] Q05 -- Cooley-Tukey FFT`. Jelenlegi állapot: a stdout csak logfájlba megy, nem látható. Megoldás: `04_nlm_dfs_queries.py`-ban `rich.progress` vagy egyszerű `tqdm` progress bar, és a script Windows Terminalból legyen indítva (nem MCP-ből).
- 💬 NOTE: Napi kvóta kimerülés tapasztalva (2026-05-27): a kvóta notebook-független -- a 2_het notebook is RESOURCE_EXHAUSTED hibát ad, holott azon még egyetlen DFS query sem futott. A limit tehát Google-fiók szintű (nem per-notebook). Tesztnap összesített lekérdezések: 1_het Qfig(1) + DFS próba(2, leállítva) + DFS újra(40) + 2_het Qfig(1) + tesztlekérdezések ≈ 50 körül merül ki. Következő futtatás: másnap (kvóta éjfélkor PT szerint reset).
- 💬 NOTE: Napi kvóta kimerülés tapasztalva (2026-05-27): 1_het 41 queryből 40 sikerült, Q41 (Parciális differenciálegyenletek) RESOURCE_EXHAUSTED hibával leállt. A 2_het DFS ugyanazon a napon nem futtatható. A `--resume` flag másnap kihagyja a kész fájlokat, de Q41 nem mentődött -- `--resume` nélküli újrafuttatás felülírja az összeset. Javasolt eljárás: Q41-et manuálisan pótolni (`nlm query notebook ... --json > nlm_q41_raw.txt`), majd a 2_het DFS-t másnap `--sleep 5`-tel indítani.
- 🔲 TODO: **DFS állapot-perzisztencia hiányzik (tesztelve 2026-05-27).** Ha az NLM napi kvóta lejár, a következő session-ben a skill/agent nem tudja, hol tartott a feldolgozás. Szükséges: `3_raw_outputs/dfs_state.json` fájl, amely tárolja: `{"total_weeks": 2, "current_week": 1, "total_queries": 41, "completed": 7, "last_query": "Q07", "quota_exhausted": false}`. A `--resume` flag a meglévő `nlm_q*_raw.txt` fájlok alapján ugrik, de ez nem tantárgy-szintű állapot -- ha a script újraindul egy új session-ben, nem tudja hány hét van hátra. Perzisztens állapotfájl a tantárgy gyökerében (`<tantargy>/dfs_state.json`) kezelné ezt.
- ✅ **Névkonvenció eltérés javítva (2026-05-28).** `04_nlm_dfs_queries.py` zero-padding eltávolítva: `nlm_q{i}_raw.txt` (padding nélkül). `05_assemble.py` ugyanezt a sémát használja. Kanonikus konvenció a `pipeline.md §2`-ben rögzítve.
- 🔲 TODO: A `04_nlm_dfs_queries.py` --dry-run kimenete L0-L4 mélységig generál queryket (1_het: 41, 2_het: 43). A pipeline.md §3 csak 3 szintet (Gyökér / 2. szint / 3. szint) dokumentál, de a script default `--max-level 99` → az egész mindmap-et lekérdezi. Nem egyértelmű, hogy a mélységi korlát szándékos-e. Mérlegelendő: `--max-level 2` alapértelmezés (pontosan 3 szint), vagy explicit dokumentálás, hogy az összes szint lekérdezése a cél.
- ✅ DFS implementálandó → **KÉSZ**: `scripts/04_nlm_dfs_queries.py` teljes DFS traversal (--resume, --sleep, --max-level, RESOURCE_EXHAUSTED detekció). A Q1-Q4 fix struktúra elavult -- a DFS script az NLM notebook ID-jét a `citations_seed.json _notebook.id` mezőből olvassa.
- 🔲 TODO: **Raw fájlnév-konvenció nem hordoz mindmap-pozíció-információt (user feedback, 2026-05-28).** Jelenlegi névséma: `nlm_q1_raw.txt`, `nlm_q01_raw.txt` -- a sorszám csak a DFS traversal sorrendjét jelöli, nem a mindmap fában elfoglalt helyet. Például nem derül ki, hogy a fájl melyik ág, melyik szint, melyik node-jához tartozik. Javasolt névséma: `nlm_q_<L0>-<L1>-<L2>_raw.txt`, ahol a szintindex a DFT traversal ágát jelöli (pl. `nlm_q_1-2-3_raw.txt` = 1. főág, 2. alág, 3. levél). Alternatíva: metadata-fájl (`dfs_state.json`) amely a sorszám↔node-path leképezést tárolja. Mérlegelendő: visszafelé kompatibilitás az assemblerrel (05_assemble.py egyszerű sorszámra vár); átállás esetén assembler-módosítás is szükséges.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-26 | 2.0 | Overhaul: template-alapú átírás; DFS logika §3.2-ben; §8 Visszajelzések; archív szekció és inline script eltávolítva |
| 2026-05-25 | 1.3 | Qfig §4; citations.json builder; Q1 redesign (bevezető szerepkör); DFS sorrend dokumentálva |
| 2026-05-24 | 1.2 | CLI workaround; conversation_id megőrzése |
| 2026-05-22 | 1.0 | Létrehozva |
