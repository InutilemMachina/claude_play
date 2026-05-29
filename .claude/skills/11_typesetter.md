---
name: 11_typesetter
title: 11_TYPESETTER -- Typesetter
type: skill
tags: [meta, skill]
status: active
version: 4.0
updated: 2026-05-26
description: Markdown linter NLM pipeline outputhoz. Fázis 1 (bullet-to-prose, Claude API). Fázis 2: whitespace/tipográfiai linting (A-H szabályok). Pipeline 11. lépése.
---

# 11_TYPESETTER

## 1. Cél

A `4_wip_outputs/N_Jegyzet.md` in-place lint-elése: whitespace, sortörés, tipográfia, fejléc-hierarchia normalizálása.

## 2. Bemenetek

- `4_wip_outputs/N_Jegyzet.md` -- 06-10 kimenet

## 3. Eljárás

### 3.1. Kétfázisú működés

| Fázis | Mit csinál | Eszköz | Státusz |
|:------|:-----------|:-------|:--------|
| **1. Próza konverzió** | Bullet-point blokkok → összefüggő folyamatos próza | Claude API | ❌ eltávolítva -- NLM `--response-length longer` már prózát ad |
| **2. Linting** | Whitespace, bekezdéstörés, LaTeX, kép/blockquote spacing | Regex szabályok (A-H) | ✅ aktív |

**Megőrzött elemek (mindkét fázisban érintetlenek):**
- Markdown fejlécek, képhivatkozások, HTML kommentek (`<!-- Q:N -->`), blockquote-ok, YAML, `<sup>` citációk, LaTeX

### 3.2. Futtatás

```powershell
# ANTHROPIC_API_KEY legyen beállítva
python scripts\11_typesetter.py test_outputs\<Tantargy>\N_het\4_wip_outputs\N_Jegyzet.md

# Fejléc-számozás külön:
python scripts\11_util_heading_numberer.py test_outputs\<Tantargy>\N_het\4_wip_outputs\N_Jegyzet.md
```

### 3.3. Szabálykészlet

| Szabály | Mit javít |
|:--------|:----------|
| **A** | `</sup>.` utáni nagybetű → üres sor szúrás (bekezdéstörés) |
| **B** | Soron belüli `N. Cím` → saját bekezdés félkövér címmel |
| **C** | `![` előtt/után üres sor |
| **D** | `>` blockquote előtt üres sor |
| **E** | Dupla `---` deduplikáció és spacing |
| **F** | LaTeX `$`/`$$` delimiter párosítás (csak figyelmeztet) |
| **G** | Fejléc-hierarchia számozás (`scripts/11_util_heading_numberer.py`) |
| **H** | Dash kiirtás: `--`, `–`, `—` → eltávolítás (NLM mellékhatás) |
| **I** | GFM tábla-szeparátor javítás: `\| :, - \|` → `\| :--- \|` (NLM formázási hiba) |
| **J** | Terminológia normalizálás: ingadozó magyar szakkifejezések → kanonikus forma |

**Rule H részletek:** Minden `4_wip_outputs/` és `5_clean_outputs/` fájlban tilos `--`, `–`, `—`. Magyarban ezek szinte mindig hibák.

**Rule I részletek:** Az NLM olykor `| :, - |` elválasztó sort generál GFM tábla-szeparátorként. Ez érvénytelen szintaxis — a renderelők nem ismerik fel táblázatként. Fix: `:---` formátumra normalizálás.

**Rule J részletek (IR termográfia + általános):** Per-query NLM válaszok különböző terminológiát használnak ugyanarra a fogalomra. Kanonikus párok:
- `emissziós tényező`, `emittancia`, `sugárzási tényező` → `emisszivitás`
- `légköri ablak(ok)` → `atmoszferikus ablak(ok)`
- `szürke test` → `szürketest`
- `hőkamera(ák)` → `IR kamera(ák)`

**Bővítés:** A TERM_MAP dict `11_typesetter.py`-ban könnyen bővíthető tantárgy-specifikus párral.

**Idempotens:** Többszöri futtatás nem szúr be felesleges üres sorokat.
**UTF-8 BOM nélkül** írja vissza a fájlt.

## 4. Kimenetek

- `4_wip_outputs/N_Jegyzet.md` -- in-place felülírva (lint + próza)

## 5. Ellenőrzés

- [ ] `</sup>.\s*[A-Z]` minta eltűnt (Szabály A)
- [ ] Soron belüli `N. Cím` eltűnt (Szabály B)
- [ ] Minden `![` előtt üres sor (Szabály C)
- [ ] Minden `>` előtt üres sor (Szabály D)
- [ ] Nincs dupla `---` (Szabály E)
- [ ] LaTeX delimiterek párosak (Szabály F -- csak figyelmeztetés)
- [ ] Minden `##`+ fejléc számozott (Szabály G)
- [ ] Nincs `--`, `–`, `—` (Szabály H)
- [ ] Tábla-szeparátor `| :--- |` formátumú (Szabály I)
- [ ] Terminológia normalizált (Szabály J -- Rule J log mutatja a javítások számát)
- [ ] Hivatkozás-szám változatlan (`<sup>` darabszám)
- [ ] Képek száma változatlan (`![` darabszám)

## 6. Hibakezelés

- Tünet: `ANTHROPIC_API_KEY` hiánya → Fázis 1 leáll
- Megoldás: `$env:ANTHROPIC_API_KEY = "..."` beállítása
- Tünet: idempotencia-hiba (dupla üres sorok)
- Megoldás: `--dry-run` flag (ha implementálva)

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [scripts/11_typesetter.py](../../scripts/)
- [scripts/11_util_heading_numberer.py](../../scripts/)

## 8. Visszajelzések

- 💬 NOTE: A Fázis 1 (bullet→próza, Claude API) újra aktív -- az NLM `--response-length longer` (helyes flag) beállítás nem mindig ad folyó prózát. Ha a Prompt B-vel kapott válaszok már prózában vannak, a Fázis 1 idempotens (nem küld API-hívást).
- ✅ Rule B lista whitespace (`*   **...**` → `* **...**`): megvalósítva, `rule_b_bullet_whitespace()` regex `^(\s*[*-])\s{2,}` az összes bullet típusra. Tesztelve.
- ✅ **Skill §3.1 Fázis 1 inkonzisztencia javítva (2026-05-28).** A §3.1 táblázat most helyesen mutatja: Fázis 1 eltávolítva.
- 🔲 TODO: **Hibás Markdown táblázat-szeparátor az NLM kimenetben (külső szemlélő, 2026-05-28).** Több táblázatban `| :, - | :, - | :, - |` szeparátorsor jelenik meg, ami nem érvényes GFM szintaxis (helyes: `|:---|:---|:---|`). Következmény: a táblázatok Markdown-renderelőkben nem táblázatként, hanem szövegként jelennek meg. Az NLM Prompt B-t módosítani kell (explicit utasítás a helyes szeparátor-formátumra), vagy a `11_typesetter.py`-ba Rule I-ként bevezetni: `| :, - |` → `|:---|`.
- 🔲 TODO: **Automatikus táblafeliratok placeholderként láthatók (külső szemlélő, 2026-05-28).** `*1. táblázat: (automatikus felirat)*` sorok megmaradtak a kész dokumentumban. Az "(automatikus felirat)" szöveg egy pipeline-placeholder, amelyet a `06_table_caption_injector.py` szúrt be, de a VLM/NLM nem töltötte ki valódi felirattal. Következmény: minden táblázat előtt egy értelmetlen sor áll. Megoldás: ha VLM nem fut, a placeholder távolítandó el, vagy valódi tartalommal kell kitölteni (pl. NLM query per-tábla).
- 💬 NOTE: **Futtatás eredménye 1_het teszten (2026-05-28).** Rule B: 366 fix (nagy szám -- az NLM sok `*   **...**` formátumot generál). Rule H: 218 fix (sok dash az NLM kimenetben). Rule G: 233 fejléc-számozás változás. Ez az eredmény normálisnak tekinthető 40 DFS query esetén (~190KB fájl).

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-26 | 4.0 | Overhaul: template-alapú átírás; duplikált checklist eltávolítva; §8 Visszajelzések |
| 2026-05-26 | 3.1 | Rule B hozzáadva (bullet whitespace); Rule H aktiválva |
| 2026-05-25 | 3.0 | Fázis 1 (bullet→próza) eltávolítva (NOTE G); Rule H (dash cleanup) hozzáadva |
| 2026-05-25 | 2.0 | Fázis 1 hozzáadva; `11_typesetter.py` elkészült |
| 2026-05-22 | 1.0 | Létrehozva; Rule G (fejléc-hierarchia számozás) |
