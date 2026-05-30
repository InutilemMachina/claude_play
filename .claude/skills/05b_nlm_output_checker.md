---
name: 05b_nlm_output_checker
title: 05B_NLM_OUTPUT_CHECKER -- NLM Output Quality Check
type: skill
tags: [meta, skill]
status: active
version: 3.0
updated: 2026-05-28
description: Az NLM DFS query outputok (nlm_q*.txt) minőségi ellenőrzése és 😎 jóváhagyás. Checkpoint az assembler (05_assemble.py) futtatása ELŐTT. Elkülönül az 05_assemble.py szkripttől.
---

# 05B_NLM_OUTPUT_CHECKER

## 1. Cél

Az NLM DFS query outputok (`3_raw_outputs/nlm_q*.txt`) minőségének ellenőrzése és 😎 jóváhagyása, **mielőtt `05_assemble.py` összefűzi** a draft Jegyzetet.

**Miért önálló skill?** Az `05_assemble.py` szkript végrehajtja az összefűzést -- ez a skill a megelőző minőségi checkpoint. Ha az NLM outputok hibásak (üres válaszok, hiányzó UUID-ek), az assembler futtatása előtt kell beavatkozni.

## 2. Bemenetek

- `3_raw_outputs/nlm_q*.txt` -- NLM DFS query nyers outputok (04_nlm_query_runner)
- `1_raw_inputs/citations_seed.json` -- elvárt forrás-UUID-ek referenciája

## 3. Eljárás

1. Minden `nlm_q*.txt` fájl `answer` mezőjének átnézése (nem üres, nem `null`, nem túl rövid < 200 char)
2. `sources_used` lista ellenőrzése (minden elvárt UUID megjelent-e legalább egy query-ben)
3. `citations` mező ellenőrzése (nem üres, ha Prompt B aktív)
4. Összefoglaló megjelenítése:

```
NLM Output Check összefoglaló:
- Q1: 1240 char, 3 forrás, 4 citáció
- Q2: 980 char, 2 forrás, 7 citáció
- Hiányzó UUID-ek: [ha van]
- Üres citations: [lista ha van]

😎 Ellenőrizd a minőséget. Folytassuk? "ok" / "újrafuttatás"
```

5. ⚠️ **🛑 nélküle nem folytatja** -- 😎 jóváhagyás kötelező

## 4. Kimenetek

- Belső ellenőrzés (nem hoz létre fájlt)
- 😎 jóváhagyás után: `05_assemble.py` futtatása (Bevezetés + tartalmi szekciók)

## 5. Ellenőrzés

- [ ] Minden `nlm_q*.txt` nem üres (>200 char)
- [ ] `sources_used` tartalmaz UUID-eket (minden forrás legalább egyszer hivatkozott)
- [ ] `citations` mező nem üres (ha Prompt B aktív) -- ⚠️ mély L3-L4 nodeknél ritkán üres, ez elfogadott
- [ ] 😎 jóváhagyás megérkezett

## 6. Hibakezelés

- Tünet: `answer` üres vagy nagyon rövid (<200 char)
- Gyökérok: Prompt B nem aktív, vagy a query rossz node-ra mutat, vagy kvóta-kimerülés
- Megoldás: `02_nlm_notebook_setup` újrafuttatás Prompt B-vel; `04_nlm_query_runner` query javítása; vagy másnap újra (kvóta reset éjfélkor PT szerint)

- Tünet: UUID hiányzik `sources_used`-ból
- Gyökérok: PPTX/nem-PDF forrás nem töltődött fel NLM-be (`nlm_uuid: None`)
- Megoldás: Forrás konvertálása PDF-re és újrafeltöltés; vagy a Bevezetés szekcióban megjegyezni, hogy a forrás kihagyásra került

## 7. Hivatkozások

- [pipeline.md](../pipeline.md) §4 (checkpointok)
- [04_nlm_query_runner.md](04_nlm_query_runner.md)
- [scripts/05_assemble.py](../../scripts/05_assemble.py)

## 8. Visszajelzések

- 🔲 TODO: **`citations_seed.json` hiányzó `_meta` szekció.** Az `05_assemble.py` fallback logikát kapott (`nlm_mindmap_export.md` H1 + `_notebook` mezők), de a `_meta` szekció explicit kitöltése az `01_references_collector` lépésben még nem megoldott.
- 💬 NOTE: **Üres `citations` mező L3-L4 nodeknél (tesztelve 2026-05-27, 1_het, 40 query).** `citations: {}`, de `references` UUID-eket tartalmaz -- forráslefedetség teljes. Elfogadott viselkedés mély nodeknél.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-30 | 3.1 | K0 cleanup: 10 ✅ → §9 (D2/D5 rename, HTML komment, szekciónevekl, YAML fallback, main(), ###, duplikáció, ismétlés, robotikus mondatok) |
| 2026-05-28 | 3.0 | D2+D5: átnevezés `05b_nlm_output_checker`-re; §8 frissítve (✅ + nyitott); tartalmi pontosítások |
| 2026-05-26 | 2.0 | Overhaul: template-alapú átírás; státusz `review`; elavult tartalom eltávolítva |
| 2026-05-26 | 1.1 | Státusz `active`; pipeline sorrend javítva |
| 2026-05-22 | 1.0 | Létrehozva (`05_source_controller`) |
