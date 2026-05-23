---
name: 01_nlm_query_runner
title: 01_NLM_QUERY_RUNNER — NLM Query Runner
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-05-22
description: NLM notebook lekérdezése CLI-n keresztül. Mindmap szintek alapján tematikus queryek, raw JSON mentés, citations.json alapozása. Felváltja a 01_html_to_md lépést.
---

# 01_NLM_QUERY_RUNNER.MD — NLM Query Runner
_01. lépés (korábban: 01_html_to_md)_

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

| Query | Téma | Minta kérdés |
|:------|:-----|:-------------|
| Q1 | Áttekintés | Mi a [téma] és mire való? |
| Q2 | Alapfogalmak | Ismertesd az alapvető fogalmakat és matematikai definíciókat! |
| Q3 | Algoritmusok / Módszerek | Ismertesd a főbb algoritmusokat és azok összefüggéseit! |
| Q4 | Alkalmazások | Milyen alkalmazási területek léteznek, milyen példákkal? |
| Q5 | Kérdések (09 lépéshez) | [09_question_bank_collector promptja] |

A sorrend nem kötött; a mindmap struktúrája határozza meg.

# 4. Szekció-markerek injektálása

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

# 5. citations.json inicializálása

## 5.1. references mezo szerkezete (tesztelve 2026-05-22)

A `references` mezo elemei **nem** `{id, ...}` formájúak, hanem:

```json
{
  "source_id": "8bc56719-029d-4033-821b-607a96b6864a",
  "citation_number": 1,
  "cited_text": "..."
}
```

Python olvasáshoz: `{r["source_id"]: r for r in val["references"]}`.

## 5.2. citations mezo hiánya (rövid query esetén)

Tapasztalat: ha a query szövege rövid (~50-80 kar) vagy kevés szekciót fed,
az NLM a `citations` és `references` JSON mezőket üresen adja vissza (`{}`, `[]`),
bár az `answer` szöveg inline citációkat tartalmaz (`[fajlnev.pdf: 43]` formában).

**Megoldás:**
1. **Q1 legyen a leghosszabb, legátfogóbb query** -- ez adja a legtöbb JSON citations-t.
2. A `citations.json`-t **Q1 alapján** inicializáld (UUID dedup).
3. Q2/Q3 inline citációiból (regex: `\[([^:]+\.(?:pdf|html))[:\d\s,–-]*\]`) kinyert
   fájlneveket mappeld vissza a `citations_seed.json` `nlm_uuid` mezőivel, és add
   hozzá a citations.json-hoz, ha még nem szerepel.

## 5.3. Python olvasási minta (UTF-8-sig + CRLF)

A PowerShell `Out-File -Encoding utf8` BOM-os UTF-8-et és CRLF sortörést ír.
Python-ban kötelező:

```python
raw = Path("nlm_q1_raw.txt").read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
obj = json.loads(raw)
val = obj.get("value", obj)
```

`encoding="utf-8"` önmagában JSONDecodeError-t okozhat a BOM miatt.

## 5.4. citations.json builder (helyes implementáció)

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

# 6. Output fájlok

| Fájl | Tartalom |
|:-----|:---------|
| `forrasok/nlm_qN_raw.txt` | NLM CLI JSON kimenet (Prompt B) |
| `forrasok/citations.json` | UUID-alapú forrásregiszter (01 inicializálja, 04 karbantartja) |
| `N_Jegyzet.md` (váz) | Összeállított szekciók `<!-- Q:N -->` markerekkel |

# 7. Régi 01_html_to_md (archív)

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
| 2026-05-22 | 1.0 | 5.1-5.4 hozzáadva: references mezo szerkezet (source_id), citations hiány Q2/Q3-ban, UTF-8-sig CRLF minta, helyes builder kód |
| 2026-05-22 | 1.0 | Fájl létrehozva; 01_html_to_md felváltja; CLI workflow, Q:N markerek, citations init dokumentálva |
