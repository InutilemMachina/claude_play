---
name: 07_citations_maker
title: 07_CITATIONS_MAKER -- Citations Maker
type: skill
tags: [meta, skill]
status: active
version: 2.0
updated: 2026-05-26
description: UUID-alapú citáció-kezelés. citations.json karbantartása, globális atsorszámozás (citations_renumber.py), szószedet generálás. 🛑 Checkpoint: 😎 jóváhagyás szükséges.
---

# 07_CITATIONS_MAKER

## 1. Cél

A Jegyzetben szereplő per-query lokális citáció-számokat globálisan atsorszámozza, és karbantartja a `citations.json` forrásregisztert.

**Miért kell?** Az NLM CLI minden querynél helyi [1..n] számokat generál. Ha több query anyaga kerül egy Jegyzetbe, az inline `<sup>[2]</sup>` más forrást jelent Q2-ben mint Q4-ben.

## 2. Bemenetek

- `3_raw_outputs/citations.json` -- UUID-alapú forrásregiszter (04 inicializálta)
- `3_raw_outputs/nlm_q*.txt` -- NLM query JSON kimenet (Prompt B)
- `4_wip_outputs/N_Jegyzet.md` -- `<!-- Q:N -->` markerekkel

## 3. Eljárás

### 3.0. Szószedet generálása (Claude feladata)

A Prompt D futtatása NLM CLI-n keresztül **Claude feladata**, nem a useré. Claude futtatja a `nlm query notebook` parancsot, menti a raw outputot, majd buildeli a `N_Szozedet.md`-t.

### 3.1. citations.json karbantartása

**Ha nem létezik:** 04_nlm_query_runner inicializálja (lásd ott).

**Ha létezik:** Csak új UUID-eket egészítünk ki; meglévők száma nem változhat.

Szabályok:
- Kulcs: sorrendi int-string (`"1"`, `"2"`, ...), szabad slot nincs
- `nlm_uuid` kötelező (Prompt B adja)
- Ismeretlen UUID esetén `"???"` kerül a `note` mezőbe; 😎 feladata pótolni

### 3.2. Citáció-számok atsorszámozása

```bash
python scripts/07_citations_renumber.py --het N --tantargy <mappa>
```

A script:
1. `citations.json` → UUID → global_N map
2. Minden `nlm_q*_raw.txt` `citations` dict → local_N → UUID → global_N
3. Ha van `<!-- Q:N -->` marker: per-szekció csere (pontos)
4. Ha nincs: csak egyértelmű (unanimus) mappingek cseréje (biztonságos fallback)
5. Backup: `N_Jegyzet.md.bak` -- in-place felülírás

**Speciális hivatkozástípusok kezelése:**

| Típus | Példa | Kezelés |
|:------|:------|:--------|
| Multi-file inline | `[yeh2016.pdf: 43, zhu2016.pdf: 605]` | file_to_global map |
| Q1 tartomány | `[3-5]`, `[22, 24, 27-29]` | parse_local_nums regex |

### 3.3. Forrásjegyzék regenerálása

A Jegyzet `## Forrásjegyzék` szakasza `citations.json` alapján regenerálódik (IEEE formátum):

```markdown
## Forrásjegyzék

**[1]** Yeh, C-C. M. et al., "Matrix Profile I...," *IEEE ICDM*, 2016.
```

Ha `file` létezik: link `1_raw_inputs/fajlnev.pdf`-re. Ha `url`: külső link.

### 3.4. Checkpoint -- 😎 jóváhagyás

```
🛑 07_citations_maker CHECKPOINT

citations.json: N forrás, M new UUID
Citáció-cserék: K db (X pontosan, Y fallback)
Ismeretlen UUID-ek: [lista ha van]

Forrásjegyzék:
[1] ...

😎 Ellenőrizd a forráslistát. "ok" / "folytasd"
```

## 4. Kimenetek

- `3_raw_outputs/citations.json` -- frissített forrásregiszter
- `4_wip_outputs/N_Szozedet.md` -- szószedet (NLM Prompt D via `nlm_szozedet_raw.txt`)
- `4_wip_outputs/N_Jegyzet.md` -- atsorszámozott citációk + Forrásjegyzék

## 5. Ellenőrzés

- [ ] Nincs duplikált UUID `citations.json`-ban
- [ ] Globális számok nem módosultak visszafelé (csak bővítés)
- [ ] `<sup>[N]</sup>` számok a Forrásjegyzékkel konzisztensek
- [ ] Backup (`N_Jegyzet.md.bak`) létezik
- [ ] 😎 jóváhagyás megérkezett

## 6. Hibakezelés

- Tünet: `citations: {}` üres a JSON-ban
- Gyökérok: Prompt B nem aktív, vagy a query rövid → inline fallback szükséges
- Megoldás: regex fallback `\[([^:]+\.pdf)\]` az `answer` mezőkből

- Tünet: `citations.json` utolsó sorban csonkul, `JSONDecodeError: Unterminated string`
- Gyökérok: Write tool puffer nem kezeli megbízhatóan a >3 KB ékezetes JSON-t
- Megoldás: JSON íráshoz `bash cat > fájl << 'HEREDOC'` minta (single-quote heredoc)
- Tünet: `nlm_q*_raw.txt` beolvasása `JSONDecodeError`-t dob, fájl látszólag helyes
- Gyökérok: PowerShell `Out-File -Encoding utf8` BOM-os UTF-8 + CRLF-t ír
- Megoldás: `raw = Path(f).read_bytes().decode("utf-8-sig").replace("\r\n", "\n"); json.loads(raw)`

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [scripts/07_citations_renumber.py](../../scripts/)
- [04_nlm_query_runner.md](04_nlm_query_runner.md) -- citations.json inicializálás

## 8. Visszajelzések

- 🔲 TODO: **Öt különböző hivatkozás-stílus egyszerre egy dokumentumban (külső szemlélő, 2026-05-28).** Az NLM per-szekciónként más formátumban adja vissza a citációkat, és az assembler mindet változtatás nélkül illeszti be: (1) `[1-3]` szám-only; (2) `[5] **Wikipedia**` inline vastag szöveg; (3) `**FORRÁS: Wikipedia, MIT...**` záróblokk-formátum; (4) `Forrás: \`fajlnev.pdf\`` backtick-es sor; (5) `[84, \`Discrete Fourier transform - Wikipedia\`]` szám+backtick+fájlnév. Következmény: az összefűzött dokumentum hivatkozásai kaotikusak. Megoldás: Prompt B egységesítése (`[N]` szám-only inline, külön FORRÁSJEGYZÉK-szekció per-query), vagy post-process normalizálás a 07_citations_renumber.py-ban.
- 🔲 TODO: **Forrás megjelenítési neve eltér a fájlnévtől (tesztelve 2026-05-28, 2_het).** A `citations_seed.json`-ban: `nagyi_NA_slides.pdf`, de az NLM válaszokban `Aramlasi rendellenessegek (Nagy).pdf` (ékezet nélkül, NLM-belső megjelenítési névként). Ugyanerre a forrásra 3 névvariáns jelenik meg a Jegyzetben: `Aramlasi rendellenessegek (Nagy).pdf`, `Aramlasi rendellenessegek (Nagy)` (.pdf nélkül), `nagyi_NA_slides.pdf`. Megoldás: `citations_seed.json`-ban egy `display_name` mező bevezetése, amely az NLM-beli megjelenítési nevet tárolja; a `07_citations_renumber.py` ezt használja egységesítésre.
- 🔲 TODO: **Per-szekciós forrásblokkok elnevezése inkonzisztens (tesztelve 2026-05-28, 2_het).** Különböző szekciókban: `**Hivatkozott források:**`, `**Felhasznált források:**`, `**Hivatkozott/Felhasznált források:**`, vagy semmi. Az NLM Prompt B nem írja elő, milyen névvel zárja a szekciót. Egységesítendő: Prompt B-be beépíteni az elvárt szöveget, pl. "A válasz végén mindig `**Felhasznált források:**` blokkot írj."
- 🔲 TODO: **Inline FORRÁSJEGYZÉK blokkban -- nem összesített, nem IEEE (külső szemlélő, 2026-05-28).** Q1 és Q35 végén bullet lista: `* \`Discrete Fourier transform - Wikipedia\`` formátumban -- ez az NLM per-query forrásmegjelölése, nem egy szabványos forrásjegyzék. Az összefűzött Jegyzetben ezek a blokkok "beleszúrtan" maradnak a szöveg közepén. Az `05_assemble.py` ezeket nem szűri ki. Megoldás: per-query FORRÁSJEGYZÉK blokkokat eltávolítani az összefűzésnél, az összesített IEEE-stílusú Forrásjegyzéket a `07_citations_maker` generálja a dokumentum végén.
- 🔲 TODO: **A szövegközi hivatkozások nem IEEE formátumban jelennek meg a wip Jegyzetben (user feedback, 2026-05-28).** Például: `[27, 'Discrete Fourier transform - Wikipedi']` -- ez az NLM nyers JSON `citations` mezőjének változtatás nélküli beragasztása. Az elvárt formátum: `<sup>[27]</sup>` (szám-only inline), a Forrásjegyzékben `[27] Szerző, "Cím," ...` (IEEE). Gyökérok: (1) `07_citations_renumber.py` nem futott (elavult útvonalak); (2) `05_assemble.py` a nyers `citations` dict-et inline szúrja be, nem formázott `<sup>` tagként. Megoldás: az assembler formázza a citations dict-et `<sup>[N]</sup>` alakra az összefűzés során, ne a nyers szöveget illessze be.
- 💬 NOTE: A `nlm_szozedet_raw.txt` feldolgozásához szükséges lehet egy `07_szozedet_parser.py` script (hasonlóan 03-1_qfig_parser-hez); egyelőre manuális feldolgozás vagy Claude-feladatként.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-30 | 2.2 | K1: 07_citations_renumber.py + citations.json auto-gen lezárva (_citations_util.py + 04 integráció) |
| 2026-05-30 | 2.1 | K0 cleanup: Prompt D ✅ → §9; Duplikált citációk lezárva (05_assemble.py sorted(set(...)) igazolja) |
| 2026-05-26 | 2.0 | Overhaul: template-alapú átírás; §8 Visszajelzések; csonkított NOTE-ok pótolva |
| 2026-05-25 | 1.1 | NOTE: szószedet NLM-alapra teendő |
| 2026-05-24 | 1.0 | Létrehozva |
