---
title: Self-Attention Log -- Termografia_teszt_v2
type: meta
status: active
version: 1.0
updated: 2026-05-24
description: Session-szintű agent-monitoring napló.
---

# Self-Attention Log -- Termografia_teszt_v2

# 1. Session meta

| Mező | Érték |
|:-----|:------|
| Session dátuma | 2026-05-24 |
| Notebook neve | Termografia_teszt_v2 |
| Kvalitatív szimulálás | igen (02, 04 checkpoint) |

# 2. Agent-megfigyelési napló

| # | Esemény | Döntés / Megjegyzés |
|:--|:--------|:--------------------|
| 001 | Kontextus-betöltés: project_status, nlm_integration, pipeline, 00b skill | Teljes kontextus OK |
| 002 | Self-attention értelmezés: saját agent-viselkedés monitorozása | Naplózás megkezdve |
| 003 | Mappastruktúra ellenőrzés: test_sources/termografia/ = 28 fájl, nincs forrasok/ alkönyvtár | ELTÉRÉS: CLAUDE.md forrasok/ subdirt ír, de fájlok a gyökérben. Döntés: tényleges struktúrához alkalmazkodás |

# 3. Self-check eredmények (fázisok után)

## 00b után (notebook setup)
[ Kitöltendő ]

## 01 után (NLM queries)
[ Kitöltendő ]

## 03-04 után (Excerpt + Citations)
[ Kitöltendő ]

## 06-07 után (Notes + Typesetter)
[ Kitöltendő ]

## 10 után (BSc filter -- végső audit)
[ Kitöltendő ]

# 4. Kockázatok (előzetes)

| Kockázat | Valószínűség | Mitigation |
|:---------|:-------------|:-----------|
| nlm login cookie lejárt | közepes | nlm login futtatás ellenőrzés |
| HTML forrás JS-renderelt | közepes | Claude in Chrome fallback |
| Ékezetes fájlnév PowerShell | magas | ASCII idézőjel + explicit encoding |
| NLM source feldolgozás >600s | alacsony | --wait-timeout 900 |

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-24 | 1.0 | Létrehozva |

| 004 | HTML mentés: Wikipedia Emissivity | web_fetch 244KB HTML; tail -n +4 HTTP header trim kellett; SingleFile szimuláció OK |

| 005 | NLM HTML lokális fájl upload | HIBA: lokalis HTML nem tölthető fel; megoldás: URL-ként adjuk hozzá (pitfall) |
| 006 | Thermodelta URL duplikáció | Error: Could not add url source -- de mégis feltöltődött; 9 forrás lett a várt 8 helyett |
| 007 | DOCX upload | PASS -- 12MB docx sikeresen feltöltve (nem volt dokumentálva, hogy támogatott) |
| 008 | Mindmap struktúra | 6 level-2 node azonosítva; conversation_id: f07d5b07 |

## Scope bővítés: mélységi próba (2026-05-24)

A self-attention log ezentúl kettős monitort futtat:
- **Op-minőség**: döntések, eltérések, hibák, automatizálhatóság
- **Output-minőség**: ékezetűség, citáció-sűrűség, struktúra-konzisztencia

| 009 | Q1-Q4 ékezetűség | 7.7-8.7% -- OK (küszöb: >1.5%) |
| 010 | Q1/Q3/Q4 citations=0 | NLM inline szöveges citációt adott [N] helyett; tartalom OK; Prompt B formátum inconsistens |
| 011 | Q2 citációk | 10 db numbered citation, 5 sources_used -- ideális; kontextustól függ |
| 012 | conversation_id konzisztencia | Minden Q ugyanaz az ID (f07d5b07) -- NLM session-on belül konzisztens |

| 013 | 06_notes_collector insert minta mismatch | HIBA: '---\n\n# 1_Jegyzet' != '---\n# 1_Jegyzet'; silent replace fail. Gyökérok: YAML frontmatter után 1 sortörés, nem 2. Javítás: re.sub rugalmas mintával. Pitfalls-ba jelölve. |
| 014 | 03_excerpt_block_maker fejezet összegzők | 4 fejezetből csak 1 🗺️ összegző jelent meg (chapter-matching logika hibás). Elfogadott hiányosság tesztre. |

| 015 | Self-check 08-10 false alarm | SZINT tag a Prezentációban nem elvárt -- check szabály hibás volt. Tényleges output OK. |
| 016 | PPTX generálás | Status 1 a konzolon, de fájl kész (105KB). Gyökérok: encoding hiba a print() outputban. |
| 017 | BSc filter | Prezentáció: -15 sor (MSc dia kiszűrve), Kérdések: -17 sor (MSc fejezet). |
