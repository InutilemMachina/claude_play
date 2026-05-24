---
title: CLAUDE.md -- Tantárgy-fejlesztés Meta-Instrukciók
type: meta
status: active
version: 3.0
updated: 2026-05-23
description: Master index. Naming, struktúra, fájlkatalógus, PDCA protokoll.
---

# CLAUDE.MD -- Tantárgy-fejlesztés Meta-Instrukciók

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
| 📎 | LINK (projekten belül) |
| 🔗 | LINK (projekten kívülre) |

## 1.2. Szerepkörök

| Emoji | Ki | Mikor |
|-------|----|-------|
| 😎 | Felhasználó | Manuális teendő, döntés, checkpoint jóváhagyás |
| 🤖 | Claude | Pipeline lépések (01-10) |
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
- Python kódok: **angol** (name + content); magyarázat: **magyar**
- Heti outputok (`N` = hét száma): `N_Szozedet.md`, `N_Mindmap.md`, `N_Jegyzet.md`, `N_Prezentacio.md`, `N_Kerdesek.md`
- Szóköz tilos -- alulvonás
- Forrás PDF-ek: `vezeteknev2024_tipus.pdf`; azonos esetben: `vezeteknev2024a_tipus.pdf`

# 3. Mappastruktúra

```
claude_play/
├── CLAUDE.md               ez a fájl
├── .claude/
│   ├── skills/NN_*.md      pipeline skill-ek
│   ├── archive/            elavult fájlok
│   └── settings.local.json
├── templates/              shared -- nincs per-teszt másolat
│   ├── du_template.pptx
│   ├── context_sablon.md
│   └── assets/
├── scripts/                Python szkriptek
├── test_sources/[tema]/    nyers forrás PDF-ek, HTML-ek topik szerint
│   └── forrasok/
└── [TantargyNeve]/         éles tantárgy (tesztkör végén törlendő)
    ├── context.md          leíró + pipeline státusz + blokkolók
    └── N_[tema]/
        ├── raw_sources/    junction → test_sources/[tema]/forrasok/
        ├── clean_sources/  feldolgozott forrásanyag
        ├── bsc/
        └── N_*.md          heti outputok
```

Tantárgy-szintű context.md: ld. `templates/context_sablon.md`.

# 4. Dokumentálási protokoll

Az általános elvek (architektúra, hibakezelés, token-takarék, PDCA) a Cowork Instructions mezőben vannak rögzítve. Az alábbi tábla a projekt-specifikus célokat mutatja.

| Mi történt | Hova | Formátum |
|-----------|------|----------|
| Teszt lefutott | `project_status.md` > Do | Dátum + checklist |
| Új hiba | `pitfalls.md`, új szekció | Tünet / Gyökérok / Megoldás |
| Skill javítva | `skills/NN_*.md` > Változásjegyzék | Táblasor |
| Pipeline változott | `pipeline.md` | In-place |
| Képpipeline változott | `kepek_workflow.md` | In-place |
| Következő teendők | `project_status.md` > Plan | Prioritástáblázat |

**Aranyszabály:** Skills LINKELNEK `pitfalls.md`-be -- sosem másolják.

# 5. Fájlkatalógus

| Fájl | Leírás |
|------|--------|
| [pipeline.md](.claude/pipeline.md) | Pipeline flowchart, IO táblázat, checkpointok |
| [project_status.md](.claude/project_status.md) | PDCA log: Plan / Do / Check |
| [pitfalls.md](.claude/pitfalls.md) | Ismert hibák + megoldások (skills ide linkelnek) |
| [nlm_integration.md](.claude/nlm_integration.md) | NLM CLI, Export-Tool, auth, notebook-lista |
| [nlm_prompts.md](.claude/nlm_prompts.md) | NLM Configure Chat promptok (Prompt B, C) |
| [kepek_workflow.md](.claude/kepek_workflow.md) | Képpipeline: MinerU → figure_catalog → 05b |
| `.claude/skills/NN_*.md` | Pipeline skill-ek (00--10) |
| `.claude/archive/` | Elavult fájlok -- nem töröljük |

Pipeline részletek és NLM parancsok: ld. a fenti linkeken.

# 6. Nyitott kérdések

| # | Kérdés | Hol részletesen |
|:--|:-------|:----------------|
| 1 | Tantárgy .claude/: másolás vs hivatkozás éles tantárgynál? | Architektúra |
| 2 | pymupdf telepítve a mineru env-be? Ha igen, mire? | Környezet |
| 3 | Pedagógiai output szekciók kötelező tartalma, összefoglaló blokk formátuma | [skills/06_notes_collector.md](.claude/skills/06_notes_collector.md) |
| 4 | Nagy témák (3+ hét) NLM notebook felosztás | [.claude/pipeline.md](.claude/pipeline.md) |
| 5 | Export-Tool automatizálás, NLM CLI skill-ek | [skills/00b_nlm_notebook_setup.md](.claude/skills/00b_nlm_notebook_setup.md) |
| 6 | bsc/ struktúra lapítása | [skills/10_bsc_filter.md](.claude/skills/10_bsc_filter.md) |

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-21 | 1.0 | Létrehozva |
| 2026-05-23 | 2.0 | Master index refaktor; PDCA protokoll; fájlkatalógus |
| 2026-05-23 | 3.0 | Merge: .claude/CLAUDE.md beolvadt ide; §2.3 pipeline tábla → link; §6 quick-ref → link; §9 nyitott kérdések elosztva skill-ekbe |
