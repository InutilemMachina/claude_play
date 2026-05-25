---
name: 04_citations_maker
title: 04_CITATIONS_MAKER — Citations Maker
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-05-22
description: UUID-alapú citáció-kezelés. citations.json építése NLM Prompt B kimenetéből + globális atsorszámozás (B opció). Checkpoint: 👤 jóváhagyás.
---

# 04_CITATIONS_MAKER.MD — Citations Maker
_04. lépés -- 🛑 Checkpoint: 👤 jóváhagyás szükséges_

# 1. Háttér -- Miért kell?

Az NLM CLI (Prompt B aktív) minden querynél **helyi** [1..n] citáció-számokat generál.
Ha több query anyaga kerül egy Jegyzetbe, az inline `<sup>[2]</sup>` hivatkozás más forrást
jelent a Q2-es szekciókban mint a Q4-esekben.

**B opció (UUID-alapú dedup + globális atsorszámozás):**
- `forrasok/citations.json` minden forrást **UUID alapján** tárol (NLM Prompt B adja).
- `scripts/citations_renumber.py` visszaalakítja a query-lokális számokat globálisakra.
- Szekció-markerek (`<!-- Q:N -->`) teszik pontossá a cserét; markerek nélkül csak
  egyértelmű (minden queryben azonos) mappingek kerülnek alkalmazásra.

# 2. citations.json séma

```json
{
  "1": {
    "title": "Matrix Profile I...",
    "authors": "Yeh, C-C. M. et al.",
    "year": "2016",
    "venue": "IEEE ICDM 2016",
    "file": "yeh2016_paper.pdf",
    "url": null,
    "nlm_uuid": "72d4e1ee-a813-4764-a33e-873a136e0c81",
    "note": "STAMP algoritmus, MASS szubrutin"
  },
  "_pipeline_note": "NLM UUID-k a Prompt B citations mezoibol. ..."
}
```

Kulcs: globális sorrend (`"1"`, `"2"`, ...) = a forrás elsőként felbukkant queryjében elfoglalt sorrend.

# 3. Workflow

## 3.0. Hiányos konverzió pótlása az assembly kimenetén

Az `01_nlm_query_runner` assembly lépés NEM kezeli az alábbi hivatkozástípusokat:

| Típus | Példa | Hol jelenik meg |
|:------|:------|:----------------|
| Multi-file inline | `[yeh2016.pdf: 43, zhu2016.pdf: 605]` | Q2, Q3 body |
| Q1 tartomány | `[3-5]`, `[22, 24, 27-29]` | Q1 body |

**Megoldás:** 04 futásakor Python scripttel pótolni (ld. §3.2 alatt).

```python
# Multi-file: regex + file_to_global map
MULTI_RE = re.compile(r'\[(?:[A-Za-z0-9_]+\.(?:pdf|html):[^\]]+)\]')
def replace_multi(m):
    files = re.findall(r'([A-Za-z0-9_]+\.(?:pdf|html))', m.group(0))
    return make_sup(sorted({file_to_global[f] for f in files if f in file_to_global}))
text = MULTI_RE.sub(replace_multi, text)

# Q1 tartomány: csak a <!-- Q:1 --> ... <!-- Q:2 --> szekción belül
def parse_local_nums(s):
    nums = []
    for p in re.split(r',\s*', s):
        rng = re.match(r'^(\d+)[–\-](\d+)$', p.strip())
        if rng: nums.extend(range(int(rng.group(1)), int(rng.group(2))+1))
        elif p.strip().isdigit(): nums.append(int(p.strip()))
    return nums
```

## 3.1. citations.json építése / frissítése

**Ha nem létezik:** Claude manuálisan építi az NLM query JSON `citations` és `references`
mezőiből. UUID-onként egyszer szerepelhet egy forrás.

**Ha létezik:** Csak új UUID-eket egészít ki; meglévők száma nem változhat.

Szabályok:
- Kulcs mindig sorrendi int-string (`"1"`, `"2"`, ...), szabad slot nincs.
- `nlm_uuid` kötelező (Prompt B adja).
- `file` mező a `forrasok/` relatív fájlnévre mutat (0_references_collector naming).
- Ismeretlen UUID esetén `"???"` kerül a `note` mezőbe; 👤 feladata pótolni.

## 3.2. Citáció-számok javítása (citations_renumber.py)

```bash
python scripts/citations_renumber.py --het N --tantargy <mappa>
```

A szkript:
1. `citations.json` → UUID → global_N map
2. Minden `nlm_q*_raw.txt` → `citations` dict → local_N → UUID → global_N
3. Ha van `<!-- Q:N -->` marker a Jegyzetben: per-szekció csere (pontos)
4. Ha nincs: csak egyértelmű (unanimus) mappingek cseréje (biztonságos fallback)
5. Backup: `N_Jegyzet.md.bak` -- in-place felülírás

## 3.3. Forrásjegyzék regenerálása

A Jegyzet `## Forrásjegyzék` szakasza a `citations.json` alapján regenerálódik:

```markdown
## Forrásjegyzék

**[1]** Yeh, C-C. M. et al., "Matrix Profile I...," *IEEE ICDM*, 2016.
**[2]** Zhu, Y. et al., "Matrix Profile II...," *IEEE ICDM*, 2016.
```

IEEE formátum. Ha `file` létezik: link `forrasok/fajlnev.pdf`-re. Ha `url`: külső link.

# 4. Checkpoint -- 👤 jóváhagyás

Claude leáll és a következőt jeleníti meg:

```
🛑 04_citations_maker CHECKPOINT

citations.json: N forrás, M new UUID
Citáció-cserék: K db (X pontosan, Y fallback)
Ismeretlen UUID-ek: [lista ha van]

Forrásjegyzék:
[1] ...
[2] ...

👤 Ellenőrizd a forráslistát. Jóváhagyás: "ok" / "folytasd"
```

# 5. Fontos szabályok

- **Ne duplikálj UUID-et** a citations.json-ban.
- **Ne módosítsd a globális számokat** visszafelé -- csak bővítés lehetséges.
- **In-place módosítás:** Csak `<sup>[N]</sup>` és Forrásjegyzék változik a Jegyzetben.
- **Relatív útvonalak:** Linkek a `.md` fájlhoz képest relatívak.

# 6. Kapcsolódó fájlok

| Fájl | Szerepe |
|:-----|:--------|
| `forrasok/citations.json` | Master forrásregiszter (UUID-alapú) |
| `scripts/citations_renumber.py` | Renumber script |
| `forrasok/nlm_q*_raw.txt` | NLM query JSON (Prompt B kimenet) |
| `N_Jegyzet.md` | In-place módosítás célpontja |


# Ismert hibák

→ [pitfalls.md §1.1](../pitfalls.md) -- Write tool JSON csonkítás
→ [pitfalls.md §1.2](../pitfalls.md) -- PowerShell Out-File UTF-8-sig + CRLF
→ [pitfalls.md §3.3](../pitfalls.md) -- Assembly lépés hiányos konverzió

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-22 | 1.0 | §3.0 hozzáadva: multi-file és Q1 tartomány-hivatkozások utólagos konverziója (tesztelve PoC futáson) |
| 2026-05-22 | 1.0 | B opció implementálva: UUID-dedup + citations_renumber.py; checkpoint formátum hozzáadva |
| 2026-05-21 | 1.0 | YAML header frissítve |
