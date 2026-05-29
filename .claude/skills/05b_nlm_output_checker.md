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

- ✅ **D2 (átszámozás, 2026-05-28):** Átnevezve `05_source_controller` → `05b_nlm_output_checker`. A `05` szám az `05_assemble.py` szkripthez tartozik; ez a checkpoint skill a `05b` szufixet kapja.
- ✅ **D5 (leíróbb név, 2026-05-28):** `source_controller` → `nlm_output_checker`. Az eredeti név nem jelezte egyértelműen, hogy ez az NLM DFS outputok checkpoint-ja (és nem forráskezelés).
- ✅ **Hibás HTML kommentformátum javítva (2026-05-28):** Az `05_assemble.py` `<!, Q:1, >` helyett már `<!-- Q:N -->` formátumot generált (korábbi fix). Ellenőrizve.
- ✅ **Szekciónevekben tartalom (2026-05-28):** Az `05_assemble.py` átírva -- `## N. szekció (QN)` helyett az NLM válasz első `##` fejlécét használja szekcióként (D6: csak a heading_numberer számoz).
- ✅ **YAML cím fallback (2026-05-28):** Az `05_assemble.py` `--title` hiányában a `nlm_mindmap_export.md` H1 fejlécét olvassa be automatikusan.
- ✅ **`05_assemble.py` hiányzó `main()` hívás javítva (mini teszt, 2026-05-28).** A script csendesen futott (exit 0, no file) mert `if __name__ == "__main__": main()` hiányzott a fájl végéről. Hozzáadva + `print("Írva: ...", file=sys.stderr)` visszajelzéssel.
- ✅ **`extract_section_title()` `###` heading kezelés javítva (mini teszt, 2026-05-28).** Az NLM CLI válaszok **minden esetben `###` szintű headinggel** kezdenek (37/37 query), nem `##`-vel. Az eredeti `r'^##\s+(.+)$'` regex sosem illeszkedett. Fix: `r'^#{2,3}\s+(.+)$'` -- mind `##`, mind `###` elfogadott szekciófeliratként, `##` szintre emelve.
- ✅ **J1 Prompt B + assembler `##` duplikáció javítva (2026-05-29, iteráció 2).** Miután a Prompt B `## kötelező első sor` szabályt kapott, az NLM minden válasz elejére `##` headinget ír. Az assembler viszont L1/L2 node-oknál saját `## {node_name}` fejlécet is beilleszt → kettős fejléc. Fix: `extract_section_title()` most L1/L2-nél is eltávolítja a vezető `##`-t a szövegből, mielőtt a node_name-et fejlécként beilleszti. Tanulság: ha a Prompt B formátumot változtat, mindig ellenőrizni kell az assembler fejléc-logikájával való interakciót.
- ✅ **NLM válaszok prózával kezdtek (2026-05-28 TODO) — J1 Prompt B-vel megoldva (2026-05-29).** A `## kötelező első sor` szabály garantálja, hogy az NLM soha nem kezd prose-zal. Lezárt TODO. Q17, Q24, Q32 esetén az NLM rövid bevezető mondattal kezd, és csak utána jön a `###` heading. Ezek nem kapnak `##` wrappert (az assembler csak az 1. nem-üres sort vizsgálja). Eredmény: a dokumentumban 37 queryből csak 6 kap `##` szekciót; a többi tartalom az előző szekció alá esik. Megoldás: Prompt B frissítése (explicit instrukció: `###` heading legyen az ELSŐ sor, prose bevezető TILOS) -- vagy az assembler lookahead kibővítése (első 3 sor vizsgálata).
- 🔲 TODO: **`citations_seed.json` hiányzó `_meta` szekció (tesztelve 2026-05-27).** Az `05_assemble.py` fallback logikát kapott (`nlm_mindmap_export.md` H1 + `_notebook` mezők), de a `_meta` szekció explicit kitöltése az `01_references_collector` lépésben még nem megoldott. Következő lépés: `01_references_collector` generálja a `_meta` szekciót automatikusan.
- 💬 NOTE: **Üres `citations` mező L3-L4 nodeknél (tesztelve 2026-05-27, 1_het, 40 query).** Q14, Q20, Q25, Q31, Q32-nél `citations: {}`, de `references` UUID-eket tartalmaz -- forráslefedetség teljes. Elfogadott viselkedés mély nodeknél.
- ✅ **Extrém tartalmi ismétlődés részben megoldva (2026-05-29, iteráció 2).** Gyökérok: minden DFS csomópont teljes kontextuális választ kap → szülő+gyerek azonos tartalmat hoz. Megoldás: (1) `--max-level 2` (37→23 query, L3+ kihagyva); (2) J3 Q1 bevezető-prompt (5269→1213 kar, -77%); (3) Prompt B `ismétlés tilalma` szabály. Eredmény iteráció 2-ben: bullet 85%→40%, prose 15%→59%. Részben nyitott: szomszéd L2-csomópontok közt még van átfedés.
- ✅ **Robotikus bevezető mondatok megoldva (2026-05-29).** Prompt B `## kötelező első sor` + prose szabály megszüntette a "Az infravörös termográfia egy olyan módszer, amely..." sablon-nyitányokat. Lezárt.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-28 | 3.0 | D2+D5: átnevezés `05b_nlm_output_checker`-re; §8 frissítve (✅ + nyitott); tartalmi pontosítások |
| 2026-05-26 | 2.0 | Overhaul: template-alapú átírás; státusz `review`; elavult tartalom eltávolítva |
| 2026-05-26 | 1.1 | Státusz `active`; pipeline sorrend javítva |
| 2026-05-22 | 1.0 | Létrehozva (`05_source_controller`) |
