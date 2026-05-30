---
title: Instructions
type: project_constitution
tags: [meta]
version: 2.3
updated: 2026-05-29
description: Projekt-szintű elvek, jelölések és dokumentációs szabványok.
---

# Instructions

## 1. Cél

Ez a mappa egy NLM-alapú tananyagfejlesztési pipeline prototípusának fejlesztésére szolgál.

## 2. Alapelvek

- Az egyszerűbb megoldás előnyösebb.
- Egy fájl = egy cél.
- Minden információ csak egyetlen kanonikus helyen szerepel.
- A dokumentáció legyen rövid, világos, szabványos.
- A pipeline legyen lehetőleg automatizált, determinisztikus és minimalista.
- Az agent-ek száma legyen a lehető legkisebb.
- A részletek ne ismétlődjenek különböző fájlokban.
- A pipeline fokozatosan mentesüljön a Claude/emberi vezérléstől: az automatizálható lépések script-eket kapjanak.

## 3. Dokumentációs hierarchia

A kanonikus sorrend:

1. [CLAUDE.md](CLAUDE.md) -- belépési pont és index
2. [Instructions.md](Instructions.md) -- stabil projekt-alkotmány
3. [.claude/pipeline.md](.claude/pipeline.md) -- futási gráf és lépések
4. [.claude/project_status.md](.claude/project_status.md) -- aktuális iterációs állapot + Backlog
5. [.claude/skills/](.claude/skills/) -- egy-egy lokális skill (§6: hibakezelés, §8: visszajelzések)
6. [scripts/](scripts/) -- végrehajtó automatizmusok

## 4. Jelöléstan

### 4.1. Emoji státuszok

- 🔲: TODO
- ✅: KÉSZ / OK
- ⚙️: FÉLKÉSZ / WIP
- ❌: NOK / HIÁNYZIK
- ❔: KÉRDÉS / NYITOTT
- ⚠️: VIGYÁZAT / FONTOS
- 🚦: CHECKPOINT :
    - 🔴: ÁLLJ / STOP
    - 🟡: FELTÉTELESEN TOVÁBB ENGEDVE (feltétel dokumentálásával)
    - 🟢: MEHET
- ⚡: HIBA / inkonzisztencia
- 💬: NOTE
- 💡: IDEA

Ezeket az emoji státuszokat mindig a szöveggel is ki kell egészíteni, pl.: `💡 IDEA: Az ötlet`


### 4.2. Szerepkörök

| Jelölés | Szerep | Használat |
|---|---|---|
| 😎 | Felhasználó | Manuális döntés, jóváhagyás, checkpoint |
| 🤖 | Claude | Pipeline-lépések, dokumentumfrissítés |
| 🐍 | Python script | Konverzió, audit, tömeges feldolgozás |
| 🔌 | NLM CLI | NotebookLM műveletek |
| 💻 | Terminál / shell | Fájlműveletek, script futtatás |

## 5. Nevezéktan

### 5.1. Fejléc konvenció

- Címsorok hierarchikusan számozottak.
- A szintek következetesek.
- A címek tömörek.
- A dokumentumok nem tartalmaznak felesleges elválasztó vonalakat.

### 5.2. Fájlnév konvenció

- Meta- és skillfájlok címe: angol.
- Meta- és skillfájlok nyelve: magyar (esetleges angol kifejezésekkel).
- A fájlnevek legyenek beszédesek, rövidek és stabilak.
- Szóköz tilos.
- Alulvonás használható.
- A pipeline lépések számozása stabil maradjon.
- A végrehajtó script-ek száma és neve feleljen meg a pipeline logikájának.
- Egy script kiegészítése a sorszámozásban kötőjellel írható, pl. 03b_substep.py helyett 03-1_substep.py

### 5.3. YAML fejléc -- `tags` séma

Minden `.md` fájl YAML fejléce tartalmazzon egy **scope-tag-et** a `tags` mező első elemeként. Ez a fájl hatókörét jelöli (ortogonális a `type:` műfaj-mezőre):

| Scope-tag | Jelentés | Hol |
|---|---|---|
| `meta` | Projekt-infrastruktúra (alkotmány, pipeline, prompt, sablon) | `.claude/`, gyökér |
| `skill` | Pipeline-lépés működési protokollja | `.claude/skills/` |
| `test` | Teszt-tananyag (eldobható kísérlet) | `test_outputs/` |
| `prod` | Éles tantárgyi tananyag | éles tantárgy-mappa |

Példa: `tags: [meta, prompt]` -- scope `meta`, műfaj `prompt`.

## 6. Mappastruktúra

### 6.1. Kánon

```text
claude_play/
├── CLAUDE.md
├── Instructions.md
├── .claude/
│   ├── pipeline.md
│   ├── project_status.md
│   ├── skill_template.md    ← skill sablon
│   ├── nlm_prompts.md
│   └── skills/
│       └── NN_skill.md
├── scripts/
└── templates/
|   └── assets/
└── test_outputs/
```

### 6.2. Elv

- A struktúra legyen laposabb, ha a feladat ezt megengedi.
- A mélyítés csak akkor indokolt, ha az elkülönítés valódi szervezési előnyt ad.
- Egy mappa ne tároljon kevert célú fájlokat.

## 7. Szerkesztési szabályok

- Csak a szükséges részt módosítsd.
- Kerüld a teljes fájlok fölösleges újragenerálását.
- A változás legyen visszakövethető.
- A redundancia csökkentése elsődleges szempont.
- A lényegi információt ne másold át több fájlba.

## 8. Hivatkozási szabály

- A globális szabályokra mindig az `Instructions.md` az elsődleges hivatkozás.
- A futási sorrendre mindig a `.claude/pipeline.md` az elsődleges hivatkozás.
- Az adott működés részleteire mindig az adott skill a hivatkozási pont.
- **A hibákra az adott lépés skill-jének `§6 Hibakezelés` szekciója az elsődleges hivatkozás.** Minden felfedezett hibát ott kell dokumentálni, nem külön fájlban.
- **Fájlhivatkozás formátuma:** relatív markdown link (`[név](relatív/út)`), nem csupasz backtick-path. Így a hivatkozás kattintható és a fájlmozgatás követhető.

## 9. Token-takarékosság

- Használj minimális szöveget.
- A dokumentumok ne magyarázzanak túl.
- A szabályok csak egyszer legyenek leírva.
- A skill-ek ne ismételjék meg a pipeline teljes szövegét.

## 10. Változtatási rend

- A stabil elvek ritkán változnak.
- A pipeline részletei változhatnak.
- A skill-ek kis lépésekben frissülnek.
- A hibákból tanulság lesz, nem dokumentum duzzasztás.

### 10.1. Hard-cap szabály -- ne nőjön a komplexitás (2026-05-30)

**Minden commit net-flat vagy csökkenjen.** Új hozzáadáshoz ekvivalens komplexitás-csökkentés tartozik. Mérce: `python scripts/15_backlog_index.py` output (összesítő szám) a commit előtt és után -- **nem nőhet**.

Konkrét szabályok:

- **Új TODO a `§8 Visszajelzések`-be → zárj le egy régit ugyanott.** Lezárás = törlés (✅-jelölés + áthelyezés a Változásjegyzékbe), nem maradás.
- **Új script → vagy törölj egyet, vagy mergelj kettőt.** Új feature-flag → érvelj miért nem opció a meglévő flag-ek redukciójával.
- **Új skill / új meta-fájl → indokold miért nem fér el meglévőben.**
- **Számozott névadás (`03-1`, `06b`, `07-2`) konzerválja az inkonzisztenciát.** Új script ne kapjon "ragozott" sorszámot -- vagy beszúrod a fő sorrendbe, vagy átnevezed a környezetet is.
- **Backward-compat flag nem tartós megoldás.** Ha új API-t vezetsz be (pl. `--week-dir`), a régi (direkt arg) deprecation warning + 2 commit múlva eltávolításra kerül.

**Miért:** A `mini2` end-to-end teszt utáni audit kimutatta, hogy 61 nyitott TODO valójában 3 visszatérő gyökérokra vezethető vissza, nem 61 különálló bugra. Ennek ellenére a fejlesztés mégis tünet-orvosló (+ flag, + script, + TODO), nem strukturális (gyökérok-fix). A hard-cap kényszeríti a strukturális gondolkodást.

## 11. Visszajelzések protokoll

A tesztelés során felmerülő bejegyzések jelölése egységes:

| Jelölés | Típus | Mikor kerül ide |
|---|---|---|
| 🔲 TODO | Elvégzendő feladat | Ha a módosítás nem azonnali |
| 💬 NOTE | Megfigyelés, tapasztalat | Ha a jövőbeni futtatáshoz releváns |
| ❔ QUESTION | Nyitott kérdés | Ha döntés szükséges |
| ⚠️ WARNING | Fontos korlát | Ha figyelmen kívül hagyva hibát okoz |

Lezárt vagy beépített tétel → átvezetés a Változásjegyzékbe, törlés a Visszajelzésekből.

### 11.1. Hol gyűlnek a bejegyzések (kanonikus hely)

**Inline TODO/NOTE a szövegtörzsben TILOS** — minden bejegyzés a saját fájl dedikált szekciójába kerül, a kontextusa mellé:

| Forrás | Kanonikus hely |
|---|---|
| Skill működése | az adott skill `## 8. Visszajelzések` |
| Hiba egy lépésben | az adott skill `## 6. Hibakezelés` |
| Meta-fájl (CLAUDE.md, Instructions.md, pipeline.md, prompts/*, templates/*) | a fájl végén egy `## Nyitott pontok` szekció |
| wip/clean output -- **tartalmi/minőségi** (konkrét kimenetről) | a kimenet melletti `N_Review.md` (tantárgy-specifikus, eldobható a teszttel) |
| wip/clean output -- **pipeline-tanulság** (a kimenet hibát tár fel) | a megfelelő skill `## 8` (tartós) |

A wip/clean visszajelzésnél a **természet dönt**: a konkrét tananyagról szóló észrevétel a `N_Review.md`-be (lokális, eldobható); a pipeline-t érintő tanulság a skill `§8`-ba (tartós). Ha egy tartalmi észrevétel tartós pipeline-tanulsággá érik, átemelendő a skillbe.

**Elv: „lokálisan írni, centralizáltan olvasni".** A bejegyzés ott keletkezik, ahol releváns (lokális kontextus). Az operatív prioritási sort a `project_status.md` Backlog-szekciója adja — ez **nem másol**, csak hivatkozik a fenti forrásokra. Az aggregátor a `scripts/15_backlog_index.py`-vel regenerálható (nincs kézi karbantartás).

## 12. Nyitott kérdések

Architektúrális döntések, amelyek meghatározzák a projekt irányát, de még nem zártak.

| # | Kérdés | Érintett fájl |
|:--|:-------|:--------------|
| Q1 | Éles tantárgynál a `.claude/` meta-mappa másolódjon-e a tantárgy könyvtárába, vagy hivatkozás maradjon a `claude_play/` gyökérre? | Instructions.md §6, pipeline.md |

## 13. Nyitott pontok

- 💬 NOTE: Relatív-link elv rögzítve (§8) + belépési fájlok (CLAUDE.md, Instructions.md §3) kész. Hátra: a skillek közti hivatkozások teljes auditja (B-07).
- 💬 NOTE: YAML `tags` scope-séma rögzítve (§5.3). Hátra: a meglévő fájlok `tags` mezőinek átállítása a sémára (B-08).
- 🔲 TODO: **Prompt automatizálás -- Claude vs. 😎 feladatszétosztás nincs rögzítve (tesztelve 2026-05-30, mini2).** A pipeline promptjait Claude automatikusan futtatja és menti az eredményt; csak akkor kér emberi beavatkozást, ha technikailag lehetetlen az automatizálás. Kanonikus szétosztás: (1) **CLI-n futtatható → Claude feladata**: Prompt D (szószedet), Prompt E (kérdésbank); (2) **NLM Studio UI szükséges → 😎 feladata**: Prompt C.1 (forrásáttekintő), C.2 (fogalomtérkép), C.3 (ábrajegyzék), C.4 (kérdésbank alap) -- ezek Data Tables prompts, CLI-n nem futtathatók; mindmap export (Ultra Explorer); (3) **Mindkettő kezelhető → Claude preferált**: bármilyen `nlm query notebook`-kal elérhető prompt. Ezt a szétválasztást a pipeline.md §1 IO táblájának `Automatizáltság` oszlopa és minden érintett skill `§3 Eljárás` szekciója tartalmazza -- frissítendők.