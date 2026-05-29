---
title: Instructions
type: project_constitution
tag: [meta]
version: 2.0
updated: 2026-05-26
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

1. `CLAUDE.md` -- belépési pont és index
2. `Instructions.md` -- stabil projekt-alkotmány
3. `.claude/pipeline.md` -- futási gráf és lépések
4. `.claude/project_status.md` -- aktuális iterációs állapot
5. `.claude/skills/*.md` -- egy-egy lokális skill (§6: hibakezelés, §8: visszajelzések)
6. `scripts/*.py` -- végrehajtó automatizmusok

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

## 11. Visszajelzések protokoll

Minden skill `## 8. Visszajelzések` szekciójában gyűlnek a tesztelés során felmerülő bejegyzések.

| Jelölés | Típus | Mikor kerül ide |
|---|---|---|
| 🔲 TODO | Elvégzendő feladat | Ha a módosítás nem azonnali |
| 💬 NOTE | Megfigyelés, tapasztalat | Ha a jövőbeni futtatáshoz releváns |
| ❔ QUESTION | Nyitott kérdés | Ha döntés szükséges |
| ⚠️ WARNING | Fontos korlát | Ha figyelmen kívül hagyva hibát okoz |

Lezárt vagy beépített tétel → átvezetés a Változásjegyzékbe, törlés a Visszajelzésekből.

## 12. Nyitott kérdések

Architektúrális döntések, amelyek meghatározzák a projekt irányát, de még nem zártak.

| # | Kérdés | Érintett fájl |
|:--|:-------|:--------------|
| Q1 | Éles tantárgynál a `.claude/` meta-mappa másolódjon-e a tantárgy könyvtárába, vagy hivatkozás maradjon a `claude_play/` gyökérre? | Instructions.md §6, pipeline.md |

TODO: itt is relatív linkek alkalmazása
TODO: már itt felvezetni, hogy minden fájl YAML header `tag` értéke `meta`/`skill`/`test`/`prod`/