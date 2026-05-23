---
name: 07_typesetter
title: 07_TYPESETTER — Typesetter
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-05-21
description: Markdown tördelő és tipográfiai linting. Bekezdéstörések, LaTeX delimiterek, kép/blockquote körüli üres sorok javítása.
---

# 07_typesetter_TYPESETTER.MD

Éberi szemmel (szedői perspektívából) olvassa át a Markdown fájlt, és javítja
azokat a whitespace- / sortörés-hibákat, amelyek a renderelt nézetben
összefolyó szöveget, hiányzó bekezdés-elválasztást vagy összenyomott blokkokat
okoznak.

> **Alapelv:** Kizárólag whitespace-t és sortöréseket módosítunk — a szöveges
> tartalom, fejléc-szövegek, hivatkozások, képútvonalak és LaTeX-formulák
> érintetlenül maradnak.

# 1. Szabálykészlet

## 1.1. Szabály A — Bekezdés-törés hivatkozás után

**Minta:** `</sup>.` (vagy `</sup>,`) közvetlenül nagybetűvel folytatódik
ugyanazon a soron belül, üres sor nélkül.

**Javítás:** A hivatkozás záró pontja (`</sup>.`) után üres sort szúrunk be,
ha utána új mondat/bekezdés indul (nagybetű, nem kötőszó).

**Regex:**
```
(?<=</sup>\.\s*)(?=[A-ZÁÉÍÓÖŐÚÜŰ])
```
→ beszúrjuk: `\n\n`

**Példa (előtte):**
```markdown
…alapul<sup>[[1]](#ref-1)</sup>.A feketetest egy ideális…
```
**Példa (utána):**
```markdown
…alapul<sup>[[1]](#ref-1)</sup>.

A feketetest egy ideális…
```

## 1.2. Szabály B — Számozott alpont-cím kiemelése futó szövegből

**Minta:** Egy sor belsejében `N. Címszöveg` alakú alpont jelenik meg
(ahol N = 1–9), az előző bekezdéshez/mondathoz tapadva, üres sor nélkül.

**Javítás:** A számozott cím elé üres sort szúrunk, a számozott címet **félkövérré** tesszük: `**N. Címszöveg**`, majd a cím után üres sort szúrunk, mielőtt a törzs-szöveg folytatódik.

**Regex (felismerés):**
```
([.!?:;)\]])\s*(\d+\.\s+[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]+(?:\s+\S+)*?)([A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű])
```

**Példa (előtte):**
```markdown
…szükséges elméleti alapok a következők:1. Termodinamikai alapfogalmakA források…
```
**Példa (utána):**
```markdown
…szükséges elméleti alapok a következők:

**1. Termodinamikai alapfogalmak**

A források…
```

> ⚠️ **Figyelem:** Csak soron belüli, bekezdésbe ágyazott számozott címekre
> vonatkozik. Ha a szám már önálló sor elején áll (pl. markdown felsorolás),
> ne módosítsuk.

## 1.3. Szabály C — Kép-blokk körüli üres sorok

`![` előtt **üres sor** kell (kivéve, ha a fájl eleje vagy másik üres sor előzi meg). `![…]` sor után, ha italic caption következik (`*…*`), a caption után **üres sor** kell. Ha nincs caption, a `![…]` sor után közvetlenül **üres sor** kell.

**Regex (hiányzó üres sor `![` előtt):**
```
([^\n])\n(!\[)
```
→ `\1\n\n\2`

## 1.4. Szabály D — Blockquote előtti üres sor

Minden `>` blokk előtt üres sor szükséges (kivéve, ha az előző sor is `>` vagy üres).

**Regex:**
```
([^\n>])\n(> )
```
→ `\1\n\n\2`

## 1.5. Szabály E — Horizontális vonal (`---`) deduplikáció és spacing

Egymást követő `---` sorok (akár üres sorral elválasztva) → egyetlen `---`. `---` előtt és után pontosan **egy üres sor** legyen.

**Regex (dupla `---`):**
```
---\n+---
```
→ `---`

## 1.6. Szabály F — LaTeX delimiter-ellenőrzés

Minden `$` nyitónak legyen záró `$` párja (inline math). Minden `$$` nyitónak legyen záró `$$` párja (display math). Display math (`$$…$$`) saját sorban legyen, üres sorokkal körülvéve. Nyitó zárójel utáni math: `($` → ellenőrizni, hogy `$…$)` formátumú-e.

> ⚠️ Csak figyelmeztet / jelöl — nem próbálja automatikusan kijavítani a
> képletet, mert a tartalom-értelmezés szükséges.

## 1.7. Szabály G -- Fejléc-hierarchia számozása

Minden `#`/`##`/`###` fejléc (kivéve: dokumentumcím és speciális szekciók)
pontozott számozást kap: `# 1.`, `## 1.1.`, `### 1.1.1.` stb.

**Végrehajtás:** `scripts/heading_numberer.py <fajl>` -- nem kézzel.

Speciális (számozatlan) szekciók: `Tárgymutató`, `Forrásjegyzék`,
`Változásjegyzék`, `Változásnapló`.

**Ellenőrzés:**
```
grep '^##' fajl.md | grep -v '## [0-9]'
```
→ Ha üres kimenet: Rule G teljesült.

# 2. Workflow

1. **Beolvasás:** Teljes `.md` fájl beolvasása.
2. **Szabály G alkalmazása:** `heading_numberer.py` futtatása (script).
3. **Szabály A alkalmazása:** Regex-szel megkeressük az összes `</sup>.` + nagybetű mintát, és üres sort szúrunk be.
4. **Szabály B alkalmazása:** Megkeressük a soron belüli számozott alpont-címeket (`N. Cím`), kiemeljük saját bekezdésbe félkövér címmel.
5. **Szabály C alkalmazása:** Ellenőrizzük a `![…]` sorok előtti/utáni üres sorokat, szükség esetén beszúrjuk.
6. **Szabály D alkalmazása:** Ellenőrizzük a `> ` sorok előtti üres sorokat; ha hiányzik, beszúrjuk.
7. **Szabály E alkalmazása:** Deduplikáljuk a `---` sorokat, és biztosítjuk az egy-egy üres sort körülöttük.
8. **Szabály F ellenőrzése:** LaTeX delimiterek párosítása -- figyelmeztetést listázunk a páratlan `$`/`$$` előfordulásokról.
9. **Visszaírás:** A javított tartalom in-place visszaírása a fájlba.
10. **Összegzés:** A felhasználónak visszajelzés a javítások számáról szabálykategóriánként (G: n, A: n, B: n, C: n, D: n, E: n, F: n figyelmeztetés).

# 3. Fontos szabályok

- **Ne módosítsd a tartalmat:** Fejléc-szövegek, hivatkozások (`<sup>…</sup>`), képútvonalak (`![…](…)`), LaTeX-formulák, blockquote-szövegek és tárgymutató/forrásjegyzék-blokkok érintetlenek maradnak.
- **Ne törölj meglévő üres sorokat:** Csak hiányzókat szúrj be — a meglévő szeparáció maradjon meg.
- **Heading-hierarchia érintetlen:** A `#`, `##`, `###` szintek és szövegeik nem változnak.
- **Anchor-linkek megőrzése:** Az `<a id="…">` horgonyok és a hozzájuk tartozó `[…](#…)` hivatkozások érintetlenek maradnak.
- **Idempotens működés:** A skill többszöri futtatása nem szúr be felesleges üres sorokat — ha egy elválasztás már megvan, ne duplikáld.
- **UTF-8 kódolás megőrzése:** A fájl UTF-8 kódolással írandó vissza (BOM nélkül).

# 4. Ellenőrző lista (linting után)

- [ ] `</sup>.\s*[A-Z]` minta eltűnt (Szabály A teljesült)
- [ ] Soron belüli `N. Címszöveg` eltűnt (Szabály B teljesült)
- [ ] Minden `![` előtt üres sor van (Szabály C)
- [ ] Minden `> ` előtt üres sor van (vagy előző `>` sor) (Szabály D)
- [ ] Nincs dupla `---` (Szabály E)
- [ ] LaTeX delimiterek párosak (Szabály F)
- [ ] `</sup>.\s*[A-Z]` minta eltűnt (Szabály A teljesült)
- [ ] Soron belüli `N. Címszöveg` eltűnt (Szabály B teljesült)
- [ ] Minden `![` előtt üres sor van (Szabály C)
- [ ] Minden `> ` előtt üres sor van (vagy előző `>` sor) (Szabály D)
- [ ] Nincs dupla `---` (Szabály E)
- [ ] LaTeX delimiterek párosak (Szabály F)
- [ ] Minden `##`+ fejléc számozott, speciálisak kivételével (Szabály G)
- [ ] Hivatkozás-szám változatlan (`<sup>` darabszám)
- [ ] Képek száma változatlan (`![` darabszám)


# Ismert hibák

Nincs ismert, skill-specifikus pitfall. Általános: [pitfalls.md](../pitfalls.md)

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-22 | 1.0 | Szabály G hozzáadva (fejléc-hierarchia számozás, heading_numberer.py) |
| 2026-05-21 | 1.0 | YAML header frissítve (name typo javítva: typesetterter → typesetter) |
