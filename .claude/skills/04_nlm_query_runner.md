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

💡 **MCP alternatíva (2026-05-31 óta elérhető):** Claude Desktop sessionből a `mcp__notebooklm__notebook_query` tool közvetlenül hívható — subprocess és PATH beállítás nélkül. A `04_nlm_dfs_queries.py` subprocess-alapú megközelítés marad az elsődleges pipeline-út (stabil, tesztelt), de ad-hoc lekérdezésekhez és interaktív sessionökben az MCP tool ajánlott.

```
# MCP tool (Claude Desktop sessionben):
notebook_id: <UUID>   # nlm notebook list-ből
query: "kérdés szövege"
```

Config path (Windows UWP): `C:\Users\lasz\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json`

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

- 💬 NOTE: `nlm chat configure $NB --response-length longer` (nem `long`). A `nlm query notebook` timeout növelhető: `--timeout 180` (default: 120s).
- 🔲 TODO: Formátum-eltérés a Qfig NLM output és a `03-1_qfig_parser.py` között (tesztelve 2026-05-27). A parser per-soros `FORRAS: érték` formátumot vár, de az NLM Markdown táblázatot ad vissza → 0 entry parse-olva. Megoldás: Qfig prompt módosítása per-soros listára, VAGY a parser Markdown-tábla támogatással bővítve. Prioritás: magas (03-1 jelenleg teljesen inaktív).
- 💬 NOTE: Napi kvóta: Google-fiók szintű (nem per-notebook). ~50 lekérdezésnél merül ki. `--resume --sleep 5` másnap folytatja; RESOURCE_EXHAUSTED esetén Q_N manuálisan pótolható.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-31 | 2.2 | 3. hét cleanup: 4 tétel §9 (Studio mentés ✅ elfogadott CLI korlát; absztrakt Q0 ✅ jövőbeli; DFS perzisztencia ✅ jövőbeli; raw fájlnév ✅ dfs_node_list.json fedezi) |
| 2026-05-30 | 2.1 | K0 cleanup: 5 ✅ → §9; Qfig eredete + mentési hely + függőségi sorrend + vizuális progress lezárva; §8 tömörítve |
| 2026-05-26 | 2.0 | Overhaul: template-alapú átírás; DFS logika §3.2-ben; §8 Visszajelzések; archív szekció és inline script eltávolítva |
| 2026-05-25 | 1.3 | Qfig §4; citations.json builder; Q1 redesign (bevezető szerepkör); DFS sorrend dokumentálva |
| 2026-05-24 | 1.2 | CLI workaround; conversation_id megőrzése |
| 2026-05-22 | 1.0 | Létrehozva |
