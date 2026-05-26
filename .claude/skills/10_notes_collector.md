---
name: 10_notes_collector
title: 10_NOTES_COLLECTOR — Notes collector
type: skill
tags: [meta, skill]
status: active
version: 1.0
updated: 2026-05-21
description: Strukturált Tárgymutató (index) és Notes szekció generálása Markdown fájlba. Fejléc-alapú anchor linkek, kulcsszó-keresés.
---

# 10_NOTES_COLLECTOR.MD — NOTES COLLECTOR

Beolvas egy Markdown fájlt, kiszámítja az összes fejléc anchor-linkjét, opcionálisan
kulcsszavas mélylinkeket is beinjektál, majd egy **`## Tárgymutató`** blokkot szúr be
közvetlenül a főcím (`#`) után — vagy frissíti a meglévőt.

# 1. Amit csinál pontosan

## 1.1. Fejléc-alapú tartalomjegyzék

Minden `##`, `###`, `####` szintű fejléc szerepel az indexben, behúzással jelölve a szintet:

```markdown
## Tárgymutató

- [Fejezet neve](#fejezet-neve)
  - [Alfejezet neve](#alfejezet-neve)
    - [Részfejezet neve](#reszfejezet-neve)
```

## 1.2. Kulcsszavas mélylink (opcionális)

Ha a felhasználó kulcsszó-listát ad meg, a skill megkeresi az első bekezdést, amely
tartalmazza a kulcsszót, és beilleszt egy `<a id="idx-kulcsszó"></a>` horgonyt a bekezdés elé,
majd hozzáad egy sort az indexhez: `  - [kulcsszó](#idx-kulcsszó)`

## 1.3. In-place visszaírás

A módosított fájlt ugyanabba a fájlba írja vissza. Nem hoz létre új fájlt.

# 2. Anchor-link generálás szabályai (GitHub Flavored Markdown)

A GitHub és a legtöbb Markdown renderelő ezeket a szabályokat alkalmazza: a fejléc szövegét kisbetűsítjük, eltávolítjuk a `#`-jeleket és a vezető/záró szóközöket, a `(`, `)`, `.`, `,`, `!`, `?`, `:`, `*`, `` ` `` karaktereket eltávolítjuk, a szóközöket `-`-re cseréljük, a magyar ékezetes betűk **megmaradnak** (`é`, `á`, `ő`, `ű` stb.), duplikált fejlécek esetén `-1`, `-2` stb. suffixet kapnak.

Példák:
- `## Elméleti alapok` → `#elméleti-alapok`
- `#### 1.2.3 Stefan-Boltzmann-törvény (összsugárzás)` → `#123-stefan-boltzmann-törvény-összsugárzás`
- `### 1.3 Anyagi kölcsönhatások` → `#13-anyagi-kölcsönhatások`

# 3. Kulcsszó-stratégia célközönség szerint

Mielőtt futtatnád a scriptet, gondold végig: **kinek szól a dokumentum?** A kulcsszavakat a célközönség tudásszintjéhez igazítsd.

## 3.1. BSc kezdő hallgató (termográfia, műszaki diagnosztika)

Olyan fogalmak, amelyeket először hall és nehéz megtalálni a szövegben: fizikai alapfogalmak (`feketetest`, `emissziós tényező`, `hősugárzás`, `termogram`), sugárzási törvények (`Planck-törvény`, `Stefan-Boltzmann-törvény`, `Wien-törvény`, `Kirchhoff-törvény`), spektrum (`LWIR`, `MWIR`, `SWIR`, `NIR`, `atmoszférikus ablak`), anyagi kölcsönhatások (`abszorpció`, `reflexió`, `transzmisszió`), mérési fogalmak (`NETD`, `IFOV`, `NUC`).

## 3.2. Haladó / mérnök

Inkább a ritkán előforduló, specifikus szakkifejezések (pl. `Micro-scan`, `sNETD`, `Lambert-sugárzó`).

## 3.3. Általános dokumentum

Csak a fejléc-alapú tartalomjegyzék elegendő -- kulcsszavak nélkül.

## 3.4. NLM mindmap-alapú lekérdezési stratégia

Az NLM mindmap-node-okra kattintva a rendszer hierarchikus kérdéssablonokat küld a notebooknak. Az alábbi sablon szerint kell a lekérdezéseket felépíteni:

**Fő node (gyökér, 1. szint):**
```
Beszélgessen az ezekben a forrásokban tárgyalt <fő node=X> témakörről.
```

**Gyerek node (2. szint):**
```
Beszélgessen az ezekben a forrásokban tárgyalt, a(z) <szülő node=X> tágabb kontextusába tartozó <gyerek node=Y> témakörről.
```

**Unoka node (3. szint és mélyebb):**
```
Beszélgessen az ezekben a forrásokban tárgyalt, a(z) <szülő node=Y> tágabb kontextusába tartozó <gyerek node=Z> témakörről.
```

Ahol: `<szülő node>` mindig az adott node közvetlen szülője (egy szinttel feljebb), nem a gyökér.

**Példa (Mátrix Profil mindmap):**

| Szint | Sablon kitöltve |
|-------|-----------------|
| 1 (fő) | `...tárgyalt <fő node=Mátrix Profil> témakörről.` |
| 2 (gyerek) | `...a(z) <szülő node=Mátrix Profil> tágabb kontextusába tartozó <gyerek node=Áttekintés> témakörről.` |
| 3 (unoka) | `...a(z) <szülő node=Áttekintés> tágabb kontextusába tartozó <gyerek node=Alapvető Eszköz Idősor Elemzéshez> témakörről.` |

**Workflow:** A mindmap összes releváns node-jára sorban le kell futtatni a megfelelő sablonnal. Az így kapott NLM-válaszok alkotják a `clean_sources/` bemeneti anyagát a 06-os lépéshez.

# 4. Workflow

1. **Célzás:** A felhasználó megad egy `.md` fájl elérési útját (és opcionálisan kulcsszó-listát). Ha nem ad meg kulcsszavakat, de a célközönség ismert, a fenti listából válassz relevánsakat a dokumentum témájához.

2. **Beolvasás:** Olvasd be a teljes fájlt a Read eszközzel.

3. **Python feldolgozás:** Futtasd le a `scripts/generate_index.py  # TODO: nem létezik, megírandó` scriptet:
   ```bash
   python3 <skill_dir>/scripts/generate_index.py  # TODO: nem létezik, megírandó \
     --file <útvonal> \
     [--keywords "kulcsszó1,kulcsszó2,kulcsszó3"]
   ```
   A script in-place módosítja a fájlt.

4. **Visszajelzés:** Közöld a felhasználóval, hogy hány fejléc és hány kulcsszó-link került az indexbe.

# 5. Formátum és stílus

- A tárgymutató blokkja `## Tárgymutató` fejléccel kezdődik
- Ha már létezik ilyen blokk, a script **felülírja** (nem duplikálja)
- A fejléc-linkek előtt szint-arányos behúzás: `##` → nincs, `###` → 2 szóköz, `####` → 4 szóköz
- A kulcsszavas mélylink-sorok a hierarchia végén, egy `**Kulcsszavak:**` alcím alatt jelennek meg
- Magyar szakmai hangnem a felhasználó felé

# 6. Fontos szabályok

- **Ne duplikálj:** Ha `## Tárgymutató` már létezik, cseréld le — ne szúrj be másodikat.
- **Ne módosítsd a tartalmat:** Csak a Tárgymutató blokkot és az `<a id>` horgonyokat kezeld.
- **Fejlécek kizárása az indexből:** A `# Főcím`, a `## Tárgymutató` és a `## Forrásjegyzék` blokkok ne szerepeljenek az indexben.


# Ismert hibák

Nincs ismert, skill-specifikus pitfall. Általános: [pitfalls.md](../pitfalls.md)

# Nyitott kérdések

- Pedagógiai output szekciók: mi a kötelező tartalom? Tanulási célok, főszöveg, kulcsfogalmak, összefoglaló, kérdések -- mennyi, milyen formátumban?
- Összefoglaló blokk: szürke háttér MD-ben lehetséges-e? (GFM `> [!NOTE]` callout megoldás?)

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-24 | 1.1 | §3.4 hozzáadva: NLM mindmap-alapú lekérdezési stratégia (hierarchikus sablon) |
