---
name: 04_nlm_query_runner
title: 04_NLM_QUERY_RUNNER — NLM Query Runner
type: skill
tags: [meta, skill]
status: active
version: 1.3
updated: 2026-05-25
description: NLM notebook lekérdezése CLI-n keresztül. Mindmap szintek alapján tematikus queryek (Q1-Q4) + Qfig (figura/táblázat katalógus), raw JSON mentés, citations.json alapozása.
---

# 04_NLM_QUERY_RUNNER.MD — NLM Query Runner
_04. lépés_

> **Megjegyzés:** A régi `01_html_to_md` lépés NLM Studio HTML-export importálásra épült.
> Az NLM CLI (Prompt B) direkten lekérdezi a notebookot -- HTML export felesleges.
> Ez a skill a CLI-alapú workflow-t dokumentálja.

# 1. Mit csinál pontosan

1. A mindmap `## 2. szint` témáit lekérdezi az NLM notebooktól.
2. Minden queryt `forrasok/nlm_qN_raw.txt`-be ment (JSON, Prompt B kimenet).
3. A `citations` mezőkből inicializálja a `forrasok/citations.json`-t (UUID-dedup).
4. **Szekció-markereket** (`<!-- Q:N -->`) szúr a Jegyzet-vázlatba, hogy a
   `04_citations_maker` per-szekció renumberinget tudjon végezni.

# 2. NLM CLI parancsok

```powershell
# PATH beállítás (minden sessionben egyszer)
$env:PATH = $env:PATH + ";C:\Users\lasz\AppData\Roaming\uv\tools\notebooklm-mcp-cli\Scripts"

# Alap query (level-2 mindmap tematika szerint)
nlm query notebook "<NOTEBOOK_ID>" "<kerdes>" --json | Out-File forrasok/nlm_q2_raw.txt -Encoding utf8

# Folytatás ugyanabban a konverzációban
nlm query notebook "<ID>" "<kerdes>" --conversation-id <conv_id> --json | Out-File forrasok/nlm_q3_raw.txt -Encoding utf8
```

**Ékezetes query workaround:** Ha a CLI csonkítja az outputot ékezetes kérdésnél,
az ASCII változatot küldd (pl. "Idosor" helyett "Idősor"). Stabil megoldásig
idézőjelbe is tehető: `"\"Idősor alapfogalmak\""`.

# 3. Query-tematika (level-2 mindmap alapján)

Minden héthez a mindmap 2. szintű csomópontjai adják a query témákat:

| Query | Szerepkör | Minta kérdés |
|:------|:----------|:-------------|
| Q1 | **Bevezető + összefoglaló** -- mi a témakör, miért fontos, mit fog tartalmazni az anyag; NEM részletes tárgyalás | Mi az [téma], miért releváns, és milyen főbb területeket érint a tantárgy? Rövid bevezető szükséges, nem részletes kifejtés. |
| Q2 | 1. szekció -- kizárólag saját mindmap-csomópontja | Ismertesd az alapvető fogalmakat és matematikai definíciókat! |
| Q3 | 2. szekció -- kizárólag saját mindmap-csomópontja | Ismertesd a főbb módszereket/algoritmusokat és azok összefüggéseit! |
| Q4 | 3. szekció -- kizárólag saját mindmap-csomópontja | Milyen alkalmazási területek léteznek, milyen példákkal? |
| Q5 | Kérdések (13 lépéshez) | [13_question_bank_collector promptja] |

⚠️ **Redundancia-szabály:** Q1 és Q2-Q4 NEM fedhetik át egymást. Q1 bevezeti a tágabb kontextust; Q2-Q4 kizárólag a saját mindmap-szekciójukat tárgyalják részletesen. Az assembler (lépés 05) ellenőrzi az átfedést.

A sorrend nem kötött; a mindmap struktúrája határozza meg.

## 3.1. Mindmap-vezérelt query sablonok (NLM belső logika)

Az NLM mindmap-nézetben a csomópontokra kattintva a következő belső queryt küldi a RAG-nak:

**Gyökér csomópont:**
```
Beszélgessen az ezekben a forrásokban tárgyalt <fő node> témakörről.
```

**2. szint (gyerek node):**
```
Beszélgessen az ezekben a forrásokban tárgyalt,
a(z) <szülő node> tágabb kontextusába tartozó <gyerek node> témakörről.
```

**3. szint (unoka node):**
```
Beszélgessen az ezekben a forrásokban tárgyalt,
a(z) <szülő node> tágabb kontextusába tartozó <unoka node> témakörről.
```

A szülő mindig az **egy szinttel feljebb lévő csomópont** neve -- nem a gyökér.

### Implikáció a Q1-Q4 queryekre

A helyes pipeline-sorrend: **00b (mindmap) → 01 (queryek mindmap alapján)**.

| Query | Sablon szint | Szerepkör | Minta |
|:------|:-------------|:----------|:------|
| Q1 | Gyökér -- bevezető | Kontextus, motiváció, terjedelem; **nem részletes tárgyalás** | `"Mi az <tantárgy>, miért fontos mérnöki/tudományos szempontból, és milyen főbb területeket érint? Rövid bevezetőt kérünk."` |
| Q2-Q4 | 2. szint | Kizárólag saját szekció részletesen | `"... a(z) <tantárgy> ... <főcsomópont> témakörről -- részletesen."` |
| Q5 (opció) | 3. szint | Részszekció mélyítés | `"... a(z) <főcsomópont> ... <részcsomópont> témakörről."` |

**Konkrét minta (Termografia, 1. hét):**
```powershell
# Q1 -- bevezeto (rovid, NEM atfogo)
$q1 = "Mi az infravoros termografia, miert fontos mernoki es diagnosztikai szempontbol, es milyen fo teruletek tartoznak a tantargyhoz? Rovid bevezetot kerunk, nem reszletes targyalast."
# Q2 -- level-2: Sugarzasfizika (kizarolag)
$q2 = "Beszelgessen az ezekben a forrasokban targyalt, a(z) Infravoros termografia tagabb kontextusaba tartozo Sugarzasfizikai alaptorvenyek temakorrol -- reszletesen, definiciokkal es egyenletekkel."
# Q3 -- level-2: Hokamerak (kizarolag)
$q3 = "Beszelgessen az ezekben a forrasokban targyalt, a(z) Infravoros termografia tagabb kontextusaba tartozo Hokamerak es merestechnika temakorrol -- reszletesen, muszaki parametereivel."
# Q4 -- level-2: Alkalmazasok (kizarolag)
$q4 = "Beszelgessen az ezekben a forrasokban targyalt, a(z) Infravoros termografia tagabb kontextusaba tartozo Alkalmazasi teruletek temakorrol -- konkret peldakkal es esetulmanyokkal."
```

⚠️ **ASCII-korlát:** A CLI-n küldött kérdésben ékezetek elfogadottak, de
ha az output csonka, ASCII fallback-et alkalmazz (l. §2 workaround).

# 4. Qfig -- figura és táblázat lekérdezés

A Qfig egy **egyszer futtatott** speciális query, amely az NLM saját Vision API-ját
használja a feltöltött PDF-ek ábráinak és táblázatainak katalogizálására.
Futtatandó: **Q1-Q4 előtt, egyszer per notebook**.

Output: `raw_outputs/nlm_qfig_raw.txt` → feldolgozza: `scripts/03b_qfig_parser.py`
→ feltölti a `figure_catalog.json` `caption` + `keywords` mezőit.

## 4.1. Qfig query sablon

```
Sorold fel az összes ábrát, diagramot és táblázatot a feltöltött forrásokból.
Minden elemhez add meg pontosan:
- FORRÁS: fájlnév kiterjesztéssel (pontosan ahogy a Sources panelen látható)
- SZÁM: az ábra/táblázat sorszáma a forrásban (pl. "Figure 3", "3. ábra", "Table 1")
- ALÁÍRÁS: az eredeti caption szó szerint (ha van a forrásban)
- LEÍRÁS: 1-2 mondatos saját leírás arról, mit ábrázol és mihez kapcsolódik
- TÉMAKÖR: 2-3 kulcsszó (angolul), amelyek a tartalmat jellemzik
```

## 4.2. CLI parancs

```powershell
$qfig = "Sorold fel az osszes abrat, diagramot es tablazatot a feltoltott forrasokbol. Minden elemhez add meg pontosan: FORRAS: fajlnev kiterjesztessel. SZAM: az abra/tablazat sorszama a forrasban. ALAIRAS: az eredeti caption szo szerint (ha van). LEIRAS: 1-2 mondatos sajat leiras. TEMAKÖR: 2-3 kulcsszo angolul."
nlm query notebook "<NOTEBOOK_ID>" $qfig --json | Out-File raw_outputs/nlm_qfig_raw.txt -Encoding utf8
```

⚠️ **Ékezetes parancs:** ASCII fallback kötelező a CLI-n (l. §2 workaround). A query szövege
hosszabb, mint Q1-Q4 -- ha timeout-ol, bontsd két részre (ábrák / táblázatok).

## 4.3. Kapcsolat a figure_catalog.json-hoz

A `03b_qfig_parser.py` a Qfig outputból tölti fel:
- `entry["caption"]` -- eredeti forrás-caption (ALÁÍRÁS mező)
- `entry["keywords"]` -- kulcsszavak listája (TÉMAKÖR mező, vesszőre bontva)
- `entry["vlm_done"]` -- `true` (jelzi: caption már kitöltve, nem kell `--vlm` flag)

Ha a `figure_catalog.json`-ban egy entry `vlm_done: true`, a `03_build_figure_catalog.py
--vlm` flag kihagyja (nem futtat Claude Vision API-t rá -- takarékos).

# 5. Szekció-markerek injektálása

A Jegyzet-összeállítás során minden query-forrású blokk elé `<!-- Q:N -->` kerül:

```markdown
<!-- Q:2 -->
## 2. Alapfogalmak és definíciók

Az idősor $T = t_1, ..., t_n$ ... <sup>[1]</sup>

<!-- Q:3 -->
## 3. Algoritmusok

A STAMP algoritmus ... <sup>[1]</sup>
```

Ez teszi lehetővé, hogy a `citations_renumber.py` per-szekció végezzen pontos
local→global cserét (nem kell fallback).

# 6. citations.json inicializálása

## 6.1. references mezo szerkezete (tesztelve 2026-05-22)

A `references` mezo elemei **nem** `{id, ...}` formájúak, hanem:

```json
{
  "source_id": "8bc56719-029d-4033-821b-607a96b6864a",
  "citation_number": 1,
  "cited_text": "..."
}
```

Python olvasáshoz: `{r["source_id"]: r for r in val["references"]}`.

## 6.2. citations mezo hiánya (rövid query esetén)

Tapasztalat: ha a query szövege rövid (~50-80 kar) vagy kevés szekciót fed,
az NLM a `citations` és `references` JSON mezőket üresen adja vissza (`{}`, `[]`),
bár az `answer` szöveg inline citációkat tartalmaz (`[fajlnev.pdf: 43]` formában).

⚠️ **Q1 redesign (2026-05-25) hatása:** Q1 mostantól bevezető/összefoglaló szerepkörű -- rövidebb, kevesebb JSON citations-t ad vissza. A citations-inicializálás stratégiája ennek megfelelően frissítve:

**Megoldás:**
1. **Q1 alapján inicializáld** a `citations.json`-t (UUID dedup) -- kevesebb entry várható, mint korábban.
2. **Q2-Q4 JSON citations** (ha van) szintén adjuk hozzá a dedup logikával.
3. **Inline fallback (kötelező):** Q1-Q4 `answer` mezőiből (regex: `\[([^:]+\.(?:pdf|html))[:\d\s,–-]*\]`)
   kinyert fájlneveket mappeld vissza a `citations_seed.json` `nlm_uuid` mezőivel.
   Minden még nem szereplő UUID-ot add hozzá a citations.json-hoz.
4. **Elvárt végeredmény:** minden notebookba töltött forrás szerepeljen a citations.json-ban
   (ellenőrzés: `set(citations_seed uuid-k) == set(citations.json nlm_uuid-k)`).

## 6.3. Python olvasási minta (UTF-8-sig + CRLF)

A PowerShell `Out-File -Encoding utf8` BOM-os UTF-8-et és CRLF sortörést ír.
Python-ban kötelező:

```python
raw = Path("nlm_q1_raw.txt").read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
obj = json.loads(raw)
val = obj.get("value", obj)
```

`encoding="utf-8"` önmagában JSONDecodeError-t okozhat a BOM miatt.

## 6.4. citations.json builder (helyes implementáció)

```python
import json, re
from pathlib import Path

DIR = Path("N_het/forrasok")

def load_nlm(fname):
    raw = (DIR / fname).read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return json.loads(raw).get("value", {})

seed = json.loads((DIR / "citations_seed.json").read_text(encoding="utf-8"))
uuid_to_entry = {v["nlm_uuid"]: v for k, v in seed.items()
                 if not k.startswith("_") and v.get("nlm_uuid")}
file_to_uuid  = {v["file"]: v["nlm_uuid"] for v in uuid_to_entry.values()}

# 1. Q1 alapján: JSON citations (teljes)
q1 = load_nlm("nlm_q1_raw.txt")
q1_cits = q1.get("citations", {})

uuid_to_global = {}
citations = {}
n = 1

for local_k in sorted(q1_cits.keys(), key=lambda x: int(x)):
    uuid = q1_cits[local_k]
    if uuid not in uuid_to_global:
        entry = uuid_to_entry.get(uuid, {})
        citations[str(n)] = {
            "title": entry.get("title", ""), "authors": entry.get("authors", ""),
            "year":  entry.get("year",  ""), "venue":   entry.get("venue",   ""),
            "doi":   entry.get("doi"),       "file":    entry.get("file",    ""),
            "url":   entry.get("url_download", ""),
            "nlm_uuid": uuid, "type": entry.get("type", "paper"),
            "note":  entry.get("note", ""),
        }
        uuid_to_global[uuid] = n
        n += 1

# 2. Q2/Q3: inline fajlnev-hivatkozasok (fallback)
for qf in ["nlm_q2_raw.txt", "nlm_q3_raw.txt"]:
    ans = load_nlm(qf).get("answer", "")
    for fname in re.findall(r'\[([^:\]]+\.(?:pdf|html))', ans):
        uuid = file_to_uuid.get(fname.strip())
        if uuid and uuid not in uuid_to_global:
            entry = uuid_to_entry[uuid]
            citations[str(n)] = {
                "title": entry.get("title", ""), "authors": entry.get("authors", ""),
                "year":  entry.get("year",  ""), "venue":   entry.get("venue",   ""),
                "doi":   entry.get("doi"),       "file":    entry.get("file",    ""),
                "url":   entry.get("url_download", ""),
                "nlm_uuid": uuid, "type": entry.get("type", "paper"),
                "note":  entry.get("note", ""),
            }
            uuid_to_global[uuid] = n
            n += 1

(DIR / "citations.json").write_text(
    json.dumps(citations, ensure_ascii=False, indent=2), encoding="utf-8"
)
```

Claude végzi az első alkalommal; a `04_citations_maker` karbantartja
(szám nem változhat, csak bővülhet).

# 7. Output fájlok

| Fájl | Tartalom |
|:-----|:---------|
| `raw_outputs/nlm_qfig_raw.txt` | Qfig: ábra/táblázat katalógus (NLM Vision kimenet) |
| `raw_outputs/nlm_qN_raw.txt` | Q1-Q4: tematikus NLM CLI JSON kimenet (Prompt B) |
| `raw_outputs/citations.json` | UUID-alapú forrásregiszter (04 inicializálja, 07 karbantartja) |
| `wip_outputs/N_Jegyzet.md` (váz) | Összeállított szekciók `<!-- Q:N -->` markerekkel |

# 8. Régi 01_html_to_md (archív)

Az eredeti lépés NLM Studio HTML-exportot dolgozott fel Markdown-ná.
Ha valaki Studio HTML-exportot tölt fel (Export-Tool nélkül), a régi workflow:
1. HTML → Pandoc vagy BeautifulSoup → `.md` konverzió
2. Citáció-mezők hiányoznak → `citations.json` kézi kitöltés szükséges

Ez az út **nem ajánlott** -- Prompt B és CLI nélkül UUID-ek nem állnak rendelkezésre.


# Ismert hibák

→ [pitfalls.md §2.1](../pitfalls.md) -- Üres citations/references rövid query-nél
→ [pitfalls.md §2.2](../pitfalls.md) -- references mező struktúrája (nem {id: ...})
→ [pitfalls.md §2.3](../pitfalls.md) -- PowerShell query timeout
→ [pitfalls.md §2.4](../pitfalls.md) -- Multiline prompt: @'...'@ kötelező

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-25 | 1.3 | §4 Qfig szekció (figura/táblázat lekérdezés); szekcióátszámozás (§4→§5...§7→§8); YAML name/title 01→04 javítva; output fájlok path-ok frissítve (raw_outputs/, wip_outputs/) |
| 2026-05-25 | 1.2 | Q1 redesign: bevezető/összefoglaló szerepkör (nem átfogó lefedés); redundancia-szabály hozzáadva; §5.2 citations fallback stratégia frissítve; Q4 minta hozzáadva |
| 2026-05-24 | 1.1 | §3.1 Mindmap query sablonok hozzáadva (NLM belső logika, szülő-gyerek template) |
| 2026-05-22 | 1.0 | Fájl létrehozva; 01_html_to_md felváltja; CLI workflow, Q:N markerek, citations init dokumentálva |
