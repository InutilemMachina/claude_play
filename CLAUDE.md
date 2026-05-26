---
title: CLAUDE.md -- Tantárgy-fejlesztés Meta-Instrukciók
type: meta
status: active
version: 4.0
updated: 2026-05-24
description: Master index. Session startup, naming, struktúra, fájlkatalógus, PDCA protokoll.
---

# CLAUDE.MD -- Tantárgy-fejlesztés Meta-Instrukciók

# 0. Session indítás

**Beolvasandó minden session elején -- csak ez a két fájl:**

1. `CLAUDE.md` (ez a fájl) -- konvenciók, struktúra, katalógus
2. `.claude/pipeline.md` -- lépések 01-14, IO táblázat, mappastruktúra

**Más fájlt csak akkor olvass be, ha a feladat explicit igényli:**
- Skill fájl: ha az adott pipeline lépést futtatod
- `project_status.md`: ha Plan/Do/Check frissítés kell
- `pitfalls.md`: ha hibát diagnosztizálsz

**Ne gondolkozz feleslegesen.** Ha a feladat egyértelmű a pipeline.md alapján, kezdj el dolgozni.

# 1. Kommunikáció

## 1.1. Emoji státuszok

| Emoji | Jelentés |
|-------|----------|
| 🔲 | TODO |
| ✅ | KÉSZ / OK |
| ⚙️ | FÉLKÉSZ / WIP |
| ❌ | NOK / HIÁNYZIK |
| ❔ | KÉRDÉS / NYITOTT |
| ⚠️ | VIGYÁZAT / FONTOS |
| 🚦 | CHECKPOINT (🔴 blokkolt / 🟢 mehet) |
| ⚡ | HIBA / inkonzisztencia |
| 💬 | NOTE |
| 💡 | IDEA |

## 1.2. Szerepkörök

| Emoji | Ki | Mikor |
|-------|----|-------|
| 😎 | Felhasználó | Manuális teendő, döntés, checkpoint jóváhagyás |
| 🤖 | Claude | Pipeline lépések |
| 🐍 | Python script | MinerU, pptx, audit |
| 🔌 | NLM CLI | NLM lekérdezések (Windows-MCP PowerShell hídon) |
| 💻 | Bash/terminal | Fájlműveletek, szkript-futtatás |

# 2. Nevezéktan

## 2.1. Fejléc konvenció

- Dokumentum címe: `# Nagy Kezdőbetűk`
- Első szint: `# 1. Főcím első betű nagy`
- Második szint: `## 1.1. Alcím első betű nagy`
- Sorszámozás kötelező; utolsó szám után `. `; `#` után szóköz.
- Nincs `---` vízszintes vonal (kivétel: prezentációk, YAML frontmatter).

## 2.2. Fájlnév konvenció

- Tananyag (végtermék): mindig **magyar** nyelv
- Meta és skill fájlok neve: **angol**; tartalmuk: **magyar**
- Python script-ek: `NN_script_neve.py` (NN = pipeline lépés); tartalmuk: **angol**
- Heti outputok (`N` = hét száma): `N_Szozedet.md`, `N_Mindmap.md`, `N_Jegyzet.md`, `N_Prezentacio.md`, `N_Kerdesek.md`
- Szóköz tilos -- alulvonás
- Forrás PDF-ek: `vezeteknev2024_tipus.pdf`; azonos esetben: `vezeteknev2024a_tipus.pdf`

# 3. Mappastruktúra

```
claude_play/
├── CLAUDE.md                    ez a fájl (session startup)
├── .claude/
│   ├── pipeline.md              pipeline lépések 01-14
│   ├── project_status.md        PDCA log
│   ├── pitfalls.md              ismert hibák (skills ide linkelnek)
│   ├── nlm_prompts.md           NLM Prompt B, C szövegek
│   ├── skills/NN_*.md           pipeline skill-ek (01-14)
│   └── archive/                 elavult fájlok
├── templates/
│   ├── context_sablon.md
│   └── assets/
├── scripts/NN_*.py              pipeline script-ek (NN prefix)
├── test_sources/[tema]/         nyers forrás PDF-ek topik szerint
└── test_outputs/<TantargyNeve>/ teszt kimenetek
    └── N_het/
        ├── 1_raw_inputs/          nyers forrás fájlok (01 gyűjti)
        │   └── citations_seed.json
        ├── 2_clean_inputs/        MinerU kimenet per-forrás (03 állítja elő)
        │   └── <forrasnev>/
        ├── 3_raw_outputs/         NLM CLI kimenetek (04 állítja elő)
        ├── 4_wip_outputs/         md + konverziók (06-13)
        └── 5_clean_outputs/       végtermékek -- camera-ready (12, 14)
            └── (_bsc suffix outputok)
```

# 4. Dokumentálási protokoll

| Mi történt | Hova | Formátum |
|-----------|------|----------|
| Teszt lefutott | `project_status.md` > Do | Dátum + checklist |
| Új hiba | `pitfalls.md`, új szekció | Tünet / Gyökérok / Megoldás |
| Skill javítva | `skills/NN_*.md` > Változásjegyzék | Táblasor |
| Pipeline változott | `pipeline.md` | In-place |
| Következő teendők | `project_status.md` > Plan | Prioritástáblázat |

**Aranyszabály:** Skills LINKELNEK `pitfalls.md`-be -- sosem másolják.
**Token-takarék:** fájlmásolás `bash cp`; JSON/ékezetes tartalom `bash heredoc`; szerkesztés `Edit tool`.

# 5. Fájlkatalógus

| Fájl | Leírás |
|------|--------|
| [pipeline.md](.claude/pipeline.md) | Pipeline lépések 01-14, IO táblázat, mappastruktúra |
| [project_status.md](.claude/project_status.md) | PDCA log: Plan / Do / Check |
| [pitfalls.md](.claude/pitfalls.md) | Ismert hibák + megoldások |
| [nlm_prompts.md](.claude/nlm_prompts.md) | NLM Configure Chat promptok (Prompt B, C) |
| `.claude/skills/NN_*.md` | Pipeline skill-ek 01-14 |
| `.claude/archive/` | Elavult fájlok -- nem töröljük |

# 6. Nyitott kérdések

| # | Kérdés | Hol részletesen |
|:--|:-------|:----------------|
| 1 | Tantárgy .claude/: másolás vs hivatkozás éles tantárgynál? | Architektúra döntés |
| 2 | context_sablon.md lépésszámok (C00-C08 → 01-14) frissítése | [templates/context_sablon.md](templates/context_sablon.md) |
| 3 | ~~bsc/ struktúra lapítása~~ | ✅ Lezárva: `_bsc` suffix döntve, `5_clean_outputs/` lapos |
| 4 | NLM notebook-lista frissítése (Termografia_teszt_v2 + v3) | [skills/02_nlm_notebook_setup.md](.claude/skills/02_nlm_notebook_setup.md) |

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-21 | 1.0 | Létrehozva |
| 2026-05-23 | 3.0 | Master index refaktor; merge .claude/CLAUDE.md |
| 2026-05-26 | 5.0 | M3: mappanév konvenció bevezetve (1_raw_inputs..5_clean_outputs); §6 Q3 lezárva; script-ek 06b/03b/03c átnevezve |
| 2026-05-24 | 4.0 | §0 Session indítás szekció; 01-14 skill számozás; 1_raw_inputs/2_clean_inputs/3_raw_outputs/4_wip_outputs/5_clean_outputs mappastruktúra; kepek_workflow + nlm_integration archivált |
