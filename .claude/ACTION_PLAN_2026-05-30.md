---
title: Cselekvési terv — mini2 teszt utáni szintézis
type: log
tags: [meta]
status: active
generated: 2026-05-30
description: 61+ nyitott pont csoportosítva, prioritizálva. Forrás: 15_backlog_index + Instructions §13 + project_status §1 + saját session-tapasztalat.
---

# Cselekvési terv — 2026-05-30

61 nyitott pont a backlogban + 10 mini2 audit-találat + saját session-tapasztalatok. **Nem mindet kell javítani**: vannak elavult bejegyzések és vannak architektúrális kérdések, amelyek várhatnak. A javítások 5 témaklaszterre csoportosíthatók.

## Diagnózis: 3 mintázat a hibák mögött

A 61 TODO/hiba **nagy része 3 visszatérő gyökérokra vezethető vissza**, nem 61 különálló bugra:

1. **CLI ↔ UI hibrid félállapot**: A pipeline részben CLI-automatizált, részben NLM Studio UI-ra támaszkodik (mindmap export, C-promptok, Studio mentés). Minden ehhez kapcsolódó TODO (~15 db) tulajdonképpen **egyetlen kérdés**: Chrome MCP-vel automatizáljuk vagy fogadjuk el a manuális lépéseket?

2. **Citáció-pipeline széttöredezettsége**: 5 különálló komponens (`citations_seed.json`, `citations.json`, inline `<sup>[N]</sup>`, hivatkozásjegyzék, IEEE-formátum) — egyiket sem építi végig egy script, mind részfeladat. A `07 §8`-ban 8 TODO van ehhez kapcsolódóan, és a `04 §8`-ban további 2.

3. **Skript-API inkonzisztencia**: `--week-dir` vs. direkt argumentum váltogatva (06, 11, 14 másképp működik). Két helyen ez konkrétan blokkoló volt a mini2 tesztben.

---

## Klaszter 1: 🔴 KRITIKUS pipeline-blokkolók (most javítandó)

A mini2 tesztben **tényleges hibát okoztak**, vagy a következő futtatást is rontják.

| # | Hiba | Hol | Becsült munka |
|---|------|-----|---------------|
| K1 | `citations.json` nem generálódik 04-ben → 07 üres inputot kap | `04_nlm_dfs_queries.py` | 1-2 óra |
| K2 | `due_fill.py --week-dir` hardcoded Biofizika demo-t ad (NEM a Jegyzetet) | `due_fill.py` vagy a 12 skill flow átírása | 30 perc dokumentáció / 4 óra valódi auto |
| K3 | `[MSc]` markerek az `nlm_mindmap_export.md`-ben nem propagálódnak a Jegyzetbe | `05_assemble.py` | 2 óra |
| K4 | "Bevezetes" üres fejléc minden Jegyzetben | `05_assemble.py` (root-query fejléc logika) | 30 perc |
| K5 | Képsorszámozás visszalépett (5→1) | `10_notes_collector.py` (globális sorszám) | 1 óra |
| K6 | Qfig parser CAPTION/KEYWORDS mezők nem futnak (✅ már javítva mini2-ben) | — | ✅ KÉSZ |
| K7 | 04 DFS TimeoutExpired kezeletlen (✅ már javítva) | — | ✅ KÉSZ |
| K8 | DOCX export `cwd` hiány (✅ már javítva) | — | ✅ KÉSZ |
| K9 | Pandoc emoji-regex görög betűket törölt (✅ már javítva) | — | ✅ KÉSZ |

**Akció: K1-K5 következő session prioritása. Becsült összidő: 5-7 óra.**

---

## Klaszter 2: 🟡 Citáció/hivatkozás pipeline egységesítés

Egyetlen koherens architekturális kérdés, 8+ TODO mögötte. **Egy döntés sok TODO-t lezár.**

**Központi kérdés:** IEEE-stílusú számozott hivatkozás vagy NLM-féle `(fájlnév.pdf)` natív hivatkozás legyen-e a végső formátum?

| # | TODO összevont | Forrás |
|---|----------------|--------|
| C1 | `citations_seed.json` ↔ `citations.json` szerep duplikáció | 07 §8 |
| C2 | 5 különböző hivatkozás-stílus egyszerre | 07 §8 |
| C3 | Inline `(fájlnév.pdf)` zaj a prózában (NLM Prompt B-ből) | 07 §8 |
| C4 | Duplikált `[N],[N]` citációk | 07 §8 (78 előfordulás) |
| C5 | IEEE-stílus nem implementált | 07 §8 |
| C6 | Hivatkozásjegyzék tördelése (✅ már javítva mini2-ben) | — |

**Akció:** Egy 1-2 órás architektúrális döntés (😎) után 1 napos refaktor (🤖).

---

## Klaszter 3: 🟡 CLI ↔ UI automatizálás (Chrome MCP)

15+ TODO ugyanarról: lehet-e Claude in Chrome MCP-vel automatizálni az NLM Studio UI-t?

| Művelet | Jelenlegi | Cél |
|---------|-----------|-----|
| Mindmap export (08) | 😎 Ultra Explorer | 🤖 Chrome MCP |
| Studio mentés (04) | 😎 manuális | 🤖 Chrome MCP |
| Prompt C.1/C.2/C.3/C.4 | 😎 Studio Data Tables | 🤖 Chrome MCP |
| Vision bypass | hallucináció-gyanús | Chrome MCP-vel SVG-letöltés? |

**Akció:** Egyszeri proof-of-concept (4 óra) Chrome MCP-vel az NLM Studio-n; ha működik, ~15 TODO bezárható.

---

## Klaszter 4: 🟢 Script API inkonzisztencia és UX

| # | TODO | Becsült munka |
|---|------|---------------|
| U1 | `06_table_caption_injector` direkt arg vs. `--week-dir` | 15 perc |
| U2 | `11_typesetter` direkt arg vs. `--week-dir` | 15 perc |
| U3 | `03` kettős script UX (PDF vs nem-PDF külön parancs) | 1 óra wrapper |
| U4 | `03_util_figure_catalog` halmozási bug (catalog létezik → nem bővül) | 30 perc |
| U5 | Numerikus intervallum hibák (`1, 5 µm`) → Typesetter Rule K | 30 perc |
| U6 | Üres "Bevezetes" eltüntetése | (=K4) |

**Akció:** 1 session konzisztencia-sprint. Becsült összidő: 3-4 óra.

---

## Klaszter 5: 🟢 Dokumentáció és audit-hátralék

| # | Téma | Súlyosság |
|---|------|-----------|
| D1 | YAML `tags` séma átállítása minden `.md`-ben (B-08) | 🟢 |
| D2 | Skillek közti relatív linkek auditja (B-07) | 🟢 |
| D3 | CLAUDE.md + Instructions.md YAML `tags` hozzáadása | 🟢 |
| D4 | Prompt-szerep szétosztás explicit jelölés minden skill §3-ban | 🟡 |
| D5 | `__pycache__` és egyéb generált fájlok `.gitignore`-ba | 🟢 |
| D6 | Elavult ✅ tételek kitörlése a backlog-ból (cleanup) | 🟢 |

**Akció:** Heti karbantartási feladat, nem prioritás.

---

## Saját session-tapasztalat — implicit tanulságok

Amik NEM jelennek meg a TODO-listákban, de mini2-ben felmerültek:

1. **`cd` a Bash toolban tartós állapot** — több hiba forrása, hogy nem reseteltem vissza. Javaslat: minden Bash-hívás abszolút útvonalat használjon, vagy `Bash` tool elején `cd <project_root>` kötelező.

2. **PowerShell 5.1 newline-bug visszatér** — Prompt B esetén, de bármilyen multi-line string CLI-argumentumnál ugyanez. Érdemes egy `_ps_safe_string()` helper-t írni, ami egysoros-konvertál.

3. **NLM kvótakimerülés ~50 query/nap** — 19 query + 1 Qfig + 1 szószedet = 21 query mini2-höz. Egy 5 hetes éles tantárgy = ~105 query → 2-3 napos NLM "futtatási idő". Ezt a pipeline kapacitásszámításnál figyelembe kell venni.

4. **Vision bypass = hallucináció** — saját megfigyelésem szerint a PNG-rekonstrukció ~30%-ban kitalált node-okat tartalmazott. Ez nem a TODO-listában van mint warning, hanem mint korlát — érdemes lenne **kötelezővé tenni**, hogy ha Vision bypass volt, a user kötelezően ellenőrizze csomópontonként, és a tényt YAML frontmatter-ben jelölje (`mindmap_source: vision_bypass`).

5. **A Studio mindmap nem mindig magyarul generálódik** — magyar forrásokkal is angolul jött ki ("The Radiant Blueprint..."). Az NLM nyelvi viselkedés nehezen jósolható; a `VALASZOLJ MAGYARUL` mostantól kötelező első sor a Prompt B-ben.

---

## Cselekvési terv: 3 hetes ütemezés

### 1. hét — 🔴 Kritikus bugfix sprint (1-2 nap aktív munka)

**Cél:** A `meta_file_updates` branch mehessen `main`-be.

- [ ] K1: `citations.json` builder a 04-ben (1-2 óra)
- [ ] K3: `[MSc]` propagálás az assembler-ben (2 óra)
- [ ] K4: Üres "Bevezetes" fejléc fix (30 perc)
- [ ] K5: Globális képsorszámozás (1 óra)
- [ ] K2: `due_fill.py` CLI-mód deprecation warning + 12 skill flow doku (30 perc)
- [ ] U1+U2: Script API uniformizálás (30 perc) — `06b` és `11` `--week-dir` flag

**Ellenőrzés:** mini2 újrafuttatása, K1-K5 mindegyike validálható.

### 2. hét — 🟡 Architektúrális döntések (😎 user feladat)

**Cél:** Az architekturális dilemmák lezárása, hogy a refaktor egyértelmű legyen.

- [ ] **A1 döntés:** IEEE vagy NLM-natív hivatkozási stílus? (klaszter 2)
- [ ] **A2 döntés:** Chrome MCP automatizálási kísérlet az NLM Studio-n (klaszter 3) — egyetlen prompt erejéig, és ha működik, valódi automatizálás később
- [ ] **A3 döntés:** Vision bypass kötelező-szabályok rögzítése (frontmatter, ellenőrzési lista)
- [ ] **A4 döntés:** `main` merge mikor? (B-14)

### 3. hét — 🟢 Karbantartási sprint

**Cél:** Tartalmilag és vizuálisan letisztult repo.

- [ ] Klaszter 4: U3-U6 javítások (3-4 óra)
- [ ] Klaszter 5: D1-D6 dokumentációs hátralék (1 nap)
- [ ] Elavult ✅ TODO-k törlése
- [ ] `15_backlog_index.py` újrafuttatás → 61 → cél 20 alatt

---

## Mit NEM csinálok

- **Nem javítok meg mind a 61 pontot.** Sok már elavult (különböző teszt-futtatásokból maradtak).
- **Nem írom át a teljes pipeline-t.** A `main`-be mehet a jelenlegi állapot — a K1-K5 javítása után a pipeline éles tantárgyon futtatható.
- **Nem implementálok Chrome MCP-t magamtól.** Az architektúrális kérdés; user-döntés szükséges.
- **Nem írom át a `due_fill.py`-t.** A `12_pptx_gyarto.py` flow tisztább és működik; a `due_fill.py` API-marad library-ként.

---

## Hivatkozások

- Backlog forrás: `python scripts/15_backlog_index.py`
- mini2 audit eredmény: ezen session 2026-05-30
- Operatív backlog: [.claude/project_status.md §1](.claude/project_status.md)
