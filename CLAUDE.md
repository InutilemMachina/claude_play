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

| Emoji | Jelentés | | Emoji | Ki | Mikor |
|-------|----------|-|-------|----|-------|
| ✅ | KÉSZ | | 😎 | Felhasználó | Döntés, checkpoint |
| ⚙️ | WIP | | 🤖 | Claude | Pipeline 01-10 |
| ❌ | NOK | | 🐍 | Python script | MinerU, pptx |
| ⚠️ | VIGYÁZAT | | 🔌 | NLM CLI | PowerShell hídon |
| 🛑 | Checkpoint -- 😎 jóváhagyás kell | | 💻 | Bash | Fájlműveletek |
| 📎 | Link (belső) / 🔗 Link (külső) | | | | |

# 2. Nevezéktan

**Fejléc:** `# 1. Főcím` / `## 1.1. Alcím` -- sorszám kötelező, utolsó szám után pont + szóköz.

**Fájlnév:** szóköz tilos (alulvonás); végtermék: **magyar**; meta/skill: **angol** (tartalom: magyar); Python: **angol**.

**Heti outputok** (`N` = hét): `N_Szozedet.md` · `N_Mindmap.md` · `N_Jegyzet.md` · `N_Prezentacio.md` · `N_Kerdesek.md`

**Forrás PDF-ek:** `vezeteknev2024_tipus.pdf` (típus: paper / book / chapter / webpage / slides); azonos: `vezeteknev2024a_tipus.pdf`

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
│   ├── project_status_sablon.md
│   └── assets/
├── scripts/                Python szkriptek
└── tests/[tema]/
    ├── forrasok/            topic-szintű PDF-ek, HTML-ek
    └── N_het/
        ├── forrasok/        NLM queryok, citations, kepek/
        ├── N_*.md
        └── bsc/
```

Tantárgy-szintű struktúra (éles, `claude_play/` testvérmappái): ld. `templates/context_sablon.md`.

# 4. Dokumentálási protokoll

| Mi történt | Hova | Formátum |
|-----------|------|----------|
| Teszt lefutott | `project_status.md §Do` | Dátum + checklist |
| Új hiba | `pitfalls.md` új §N.M | Tünet / Gyökérok / Megoldás |
| Skill javítva | `skills/NN_*.md §Változásjegyzék` | Táblasor |
| Pipeline változott | `pipeline.md` | In-place |
| Képpipeline változott | `kepek_workflow.md` | In-place |
| Következő teendők | `project_status.md §Plan` | Prioritástáblázat |

**Aranyszabály:** Skills LINKELNEK `pitfalls.md`-be -- sosem másolják. Minden információnak egyetlen authoritative home-ja van; máshol: 1 sor + link.

**Token-takarék:** `bash cp` sablonok másolásához · `bash cat << 'EOF'` JSON/ékezetes fájlhoz · Edit tool (csak a változó rész, nem teljes újraírás).

# 5. Fájlkatalógus

| Fájl | Leírás |
|------|--------|
| [pipeline.md](.claude/../pipeline.md) | Pipeline flowchart, IO táblázat, checkpointok |
| [project_status.md](.claude/../project_status.md) | PDCA log: Plan / Do / Check |
| [pitfalls.md](.claude/../pitfalls.md) | Ismert hibák + megoldások (skills ide linkelnek) |
| [nlm_integration.md](.claude/../nlm_integration.md) | NLM CLI, Export-Tool, auth, notebook-lista |
| [nlm_prompts.md](.claude/../nlm_prompts.md) | NLM Configure Chat promptok (Prompt B, C) |
| [kepek_workflow.md](.claude/../kepek_workflow.md) | Képpipeline: MinerU → figure_catalog → 05b |
| `.claude/skills/NN_*.md` | Pipeline skill-ek (00--10) |
| `.claude/archive/` | Elavult fájlok -- nem töröljük |

Pipeline részletek és NLM parancsok: ld. a fenti linkeken.

# 6. Nyitott kérdések

| # | Kérdés | Hol részletesen |
|:--|:-------|:----------------|
| 1 | Tantárgy .claude/: másolás vs hivatkozás éles tantárgynál? | Architektúra |
| 2 | Nagy témák (3+ hét): hogyan osztja meg a forrást több NLM notebook? | [pipeline.md](pipeline.md) |
| 3 | Export-Tool Chrome-bővítmény automatizálható-e Claude in Chrome-mal? | [skills/00b](skills/00b_nlm_notebook_setup.md) |
| 4 | pymupdf telepítve a mineru env-be? Ha igen, mire? | Környezet |

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-21 | 1.0 | Létrehozva |
| 2026-05-23 | 2.0 | Master index refaktor; PDCA protokoll; fájlkatalógus |
| 2026-05-23 | 3.0 | Merge: .claude/CLAUDE.md beolvadt ide; §2.3 pipeline tábla → link; §6 quick-ref → link; §9 nyitott kérdések elosztva skill-ekbe |
