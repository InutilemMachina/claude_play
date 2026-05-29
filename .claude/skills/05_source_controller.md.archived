---
name: 05_source_controller
title: 05_SOURCE_CONTROLLER -- Source Controller
type: skill
tags: [meta, skill]
status: review
version: 2.0
updated: 2026-05-26
description: Forrás-összefoglalás és checkpoint az NLM query outputok ellenőrzéséhez. 🛑 Checkpoint: 😎 jóváhagyás szükséges.
---

# 05_SOURCE_CONTROLLER

## 1. Cél

Az NLM query outputok (`3_raw_outputs/nlm_q*.txt`) minőségének ellenőrzése és 😎 jóváhagyása, mielőtt a downstream lépések (06+) futnak.

⚠️ **Státusz:** Ez a skill jelenleg átdolgozás alatt áll. Eredeti célja (forrásrészek azonosítása MinerU markdown-ból) elavult -- az NLM dolgozza fel a forrásokat. Jelenlegi szerepe: checkpoint + sanity check.

## 2. Bemenetek

- `3_raw_outputs/nlm_q*.txt` -- NLM query nyers outputok
- `1_raw_inputs/citations_seed.json` -- elvárt forrásszám referencia

## 3. Eljárás

1. Minden `nlm_q*.txt` fájl `answer` mezejének átnézése (nem üres, nem `null`)
2. `sources_used` lista ellenőrzése (minden elvárt UUID megjelent-e)
3. `citations` mező ellenőrzése (nem üres ha Prompt B aktív)
4. Összefoglaló megjelenítése:

```
Source check összefoglaló:
- Q1: 3 forrás, 4 citáció
- Q2: 2 forrás, 7 citáció
- Hiányzó UUID-ek: [ha van]

😎 Ellenőrizd a minőséget. Folytassuk? "ok" / "újrafuttatás"
```

5. ⚠️ **🛑 nélküle nem folytatja** -- 😎 jóváhagyás kötelező

## 4. Kimenetek

- Belső ellenőrzés (nem hoz létre fájlt)
- 😎 jóváhagyás után: 06 indul

## 5. Ellenőrzés

- [ ] Minden `nlm_q*.txt` nem üres
- [ ] `sources_used` tartalmaz UUID-eket
- [ ] `citations` mező nem üres (ha Prompt B aktív)
- [ ] 😎 jóváhagyás megérkezett

## 6. Hibakezelés

- Tünet: `answer` üres vagy nagyon rövid
- Gyökérok: Prompt B nem aktív, vagy a query rossz node-ra mutat
- Megoldás: 02_nlm_notebook_setup újrafuttatás Prompt B-vel; 04_nlm_query_runner query javítása

## 7. Hivatkozások

- [pipeline.md](../pipeline.md) §4 (checkpointok)
- [04_nlm_query_runner.md](04_nlm_query_runner.md)

## 8. Visszajelzések

- 🔲 TODO: **`05_assemble.py` futtatási anomália (tesztelve 2026-05-27).** A script PowerShell-ből és Bash-ből is csendesen futott (exit 0, semmi kimenet, semmi fájl), inline Python hívással viszont működött. Ok: ismeretlen stdout/stderr capture probléma a MCP Bash/PS környezetben. Workaround: `python -c "... mod.main()"` alakban hívandó. Következő tesztnél kivizsgálandó, hogy a közvetlen `python scripts/05_assemble.py` hívás miért néma.
- 🔲 TODO: **`05_assemble.py` heading-struktúra problémák (tesztelve 2026-05-27, csatolt kép alapján).** Három hiba: (1) dupla sorszám a `##` fejlécekben: `## 9. 9. szekció (Q10)` -- a szám kétszer szerepel; (2) `(Q10)` felesleges suffix a kész dokumentumban -- olvasó számára zavaró; (3) a `###` alszakaszok nem hierarchikusan számozottak: `### 1. A számítási igény...` helyett `### 9.1. A számítási igény...` lenne helyes. Megjegyzés: lehetséges, hogy a downstream `11_typesetter` vagy egy dedikált heading-renumberező script javítja -- eldöntendő, hogy melyik lépés felelőssége.
- 🔲 TODO: **Heading-struktúra elcsúszik a Tartalomjegyzék + `<!-- Q:N -->` marker kombinációja miatt (user feedback, 2026-05-28).** A wip Jegyzetben pl. `<!-- Q:4 -->` után `## 5. 3. szekció (Q4)` következik -- a szekcióban egyszerre van jelen a marker (HTML komment), a dupla sorszám, és a (QN) suffix. A `11_util_heading_numberer.py` futtatása után a `## 5.` prefix duplázódik a már az NLM által számozott `3. szekció` elé. Gyökérok: az assembler által generált fejlécek (`## N. szekció (QM)`) tartalmazzák a sorszámot, a heading numberer mégis hozzáad egy külső sorszámot. Megoldás: a numberer ne számozzon újra olyan fejléceket, amelyek már `## N.` mintával kezdődnek; vagy az assembler ne tegyen sorszámot a fejlécekbe.

- 🔲 TODO: **YAML főcím és H1 vegyes ékezetes/ékezet nélküli szöveg a 2_het Jegyzetben (tesztelve 2026-05-28).** Az assembler `--title` CLI-argumentumból kerül a YAML fejlécbe és a H1 főcímbe. Ha az argumentumban az ékezetek részben hiányoznak (pl. PowerShell encoding), a cím inkonzisztens lesz: `Aramlastechnikai Gepek Rezgésdiagnosztikaja` -- vegyes, nem olvasható. A helyes cím a `nlm_mindmap_export.md` első sorából deriválható. Megoldás: az assembler a `--title` hiányában a `3_raw_outputs/nlm_mindmap_export.md` H1 fejlécét olvassa be automatikusan.
- 🔲 TODO: **`citations_seed.json` hiányzó `_meta` szekció (tesztelve 2026-05-27).** Az `05_assemble.py` a `_meta.week`, `_meta.subject`, `_meta.title` mezőket olvassa -- ezek nem léteznek, csak `_notebook`. Következmény: a cím, tantárgy, hétszám CLI-argumentumként kell megadni minden futásnál. Az `01_references_collector` vagy `02_nlm_notebook_setup` lépésben fel kellene tölteni a `_meta` szekciót a `citations_seed.json`-ba.
- 💬 NOTE: **Üres `citations` mező 6 query-nél (tesztelve 2026-05-27, 1_het, 40 query).** Q14, Q20, Q25, Q31, Q32 és még egy query `citations: {}` mezőt ad vissza, holott Prompt B aktív volt. A `references` mező ezekben is tartalmaz UUID-eket -- a forráslefedetség teljes (6/6 UUID megjelent). Valószínű ok: mély szintű (L3-L4) mindmap csomópontokra a Prompt B citációs mechanizmusa nem mindig aktiválódik. Következmény: az `05_assemble.py` local→global citation mapping ezeknél üres, a szövegközi hivatkozások az eredeti `[1]`, `[2]` formában maradnak (nem globális ID-ra mappolva).
- 🔲 TODO: **Extrém tartalmi ismétlődés a DFS kimenetben (külső szemlélő, 2026-05-28).** A DFT alapdefiníció képlete és magyarázata szóról szóra megismétlődik Q2, Q3, Q4, Q5, Q6 szekcióban. 40 DFS query esetén a mindmap L2-L3 szintjeinek szülő-csomópont-kérdései átfedő válaszokat generálnak, mert az NLM a "DFT alapfogalmak" kérdésnél és az összes leszármazott kérdésnél is hasonló bevezető kontextust ad. Következmény: az összefűzött Jegyzet nem egy tankönyv, hanem 40 egymástól független, átfedő ismertetés sorozata. Megoldás: az assembler deduplikálási logikát kapjon (pl. hasonló paragrafusok kiszűrése), vagy a Prompt B-t módosítani kell, hogy az NLM jelezze: "ezt már tárgyaltuk".
- 🔲 TODO: **Szekciónevekben nincs tényleges téma (külső szemlélő, 2026-05-28).** A `##` szintű fejlécek (`## 3. 1. szekció (Q2)`) üresek -- az olvasó a Tartalomjegyzékből nem tudja, melyik fejezet miről szól. Csak az alszakasz-cím (`### 3.1. Matematikai definíció`) hordoz tartalmat. Megoldás: az assembler az NLM válasz első `##` fejlécét használja a szekció neveként, pl. `## 3. A DFT matematikai definíciója` -- a `szekció (QN)` sablon mellőzendő.
- 🔲 TODO: **Robotikus bevezető mondatok minden szekció elején (külső szemlélő, 2026-05-28).** Az NLM sablon-bevezető szinte szóról szóra ismétlődik: "A [téma] a modern digitális jelfeldolgozás [szuperlatívusz] eszköze, amely lehetővé teszi... A feltöltött források alapján az alábbiakban részletezem...". Megoldás: Prompt B módosítása -- az NLM ne kezdjen bevezető formulával, hanem közvetlenül a tartalommal.
- 🔲 TODO: **Hibás HTML kommentformátum (külső szemlélő, 2026-05-28).** Az assembler `<!, Q:1, >` alakú markereket szúr be, amelyek érvénytelen HTML szintaxissal rendelkeznek (helyes: `<!-- Q:1 -->`). Következmény: webes/Word-exportnál ezek látható szövegként jelenhetnek meg. Az `05_assemble.py`-ban a marker-generáló kód javítandó.
- ❔ QUESTION: Ez a skill a jelenlegi formájában átdolgozandó. Eredeti logikája (forrásrészek azonosítása MinerU markdown-ból, context.md tematikával összevetés) elavult -- az NLM dolgozza fel a forrásokat. Kell-e önálló skill, vagy a 04_nlm_query_runner checklistjébe kell integrálni?
- 💬 NOTE: A pipeline-ban az `05_assemble.py` script és az `05_source_controller` skill azonos sorszámot visel -- ez zavaró. Az `05_assemble.py` egy Python szkript (Q1-Q4 összefűzés), az `05_source_controller` egy Claude-feladat (ellenőrzés). A kettő sorrendje: `assemble.py` → `source_controller` (ellenőrzés az összeállított draft-on).
- ⚠️ EMLÉKEZTETŐ (következő teszt futásnál döntendő): skill-szám ↔ script-szám párhuzamosság rendezése -- az `05_assemble.py`-nak nincs saját skill-je; a `06_excerpt_block_maker` és `06_table_caption_injector.py` két különböző műveletet fed egy számon. D2-vel együtt átgondolandó (script-átnevezés pipeline-széles változás).
- ⚠️ EMLÉKEZTETŐ: `scripts/05_util_fix_structure.py` -- NEM ehhez a skill-hez tartozik (névbeli véletlen egybeesés). Ez egy hardcoded, egyszeri post-hoc heading/TOC javítóscript a `Termografia_teszt_v2`-höz (POSIX elérési út, specifikus fejléc-map). Ha az `05_assemble.py` + `11_util_heading_numberer.py` helyesen fut, ez a script felesleges. Következő teszt futásnál eldöntendő: archiválandó-e.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-26 | 2.0 | Overhaul: template-alapú átírás; státusz `review`; elavult tartalom eltávolítva; §8 Visszajelzések |
| 2026-05-26 | 1.1 | Státusz `active`; pipeline sorrend javítva |
| 2026-05-22 | 1.0 | Létrehozva |
