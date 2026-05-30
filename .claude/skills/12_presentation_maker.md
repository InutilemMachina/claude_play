---
name: 12_presentation_maker
title: 12_PRESENTATION_MAKER -- Presentation Maker
type: skill
tags: [meta, skill]
status: active
version: 3.0
updated: 2026-05-30
description: N_Prezentacio.md (Marp) → N_Prezentacio.pptx (DUE template). Pipeline 12. lépése. Két mód: Marp-alapú (12_pptx_gyarto.py) és strukturált (due_fill.py).
---

# 12_PRESENTATION_MAKER

## 1. Cél

A `4_wip_outputs/N_Prezentacio.md`-ből (Marp) PPTX fájlt generál a DUE sablon alapján.
Kimenet: `5_clean_outputs/N_Prezentacio.pptx`.

## 2. Bemenetek

- `4_wip_outputs/N_Prezentacio.md` — Marp-formátumú diasor
- `templates/due_refactored.pptx` — DUE PPTX template (named shape-ekkel)

## 3. Eljárás

### 3.1. Pipeline-futtatás (ajánlott)

```powershell
python scripts/12_pptx_gyarto.py --week-dir test_outputs/<Tantargy>/N_het
# Input:  4_wip_outputs/N_Prezentacio.md  (automatikus)
# Output: 5_clean_outputs/N_Prezentacio.pptx  (automatikus)
```

### 3.2. Marp diasor struktúrája

```markdown
---
marp: true
theme: default
paginate: true
---

# [Heti téma]
### N. hét

---

## [Fejezet]
- főpontok bullet-formában

---

<!-- MSc -->
## [MSc] Témacím
...
<!-- /MSc -->
```

MSc diák: `<!-- MSc -->` blokkon belül — `14_bsc_filter` kihagyja.

### 3.3. Strukturált mód (due_fill.py)

Claude-vezérelt, programmatikus feltöltés:

```python
from scripts.due_fill import DUEPresentation

prs = DUEPresentation("templates/due_refactored.pptx")
prs.set_global_footer("Dr. Neve", "2026.09.01.")
prs.set_title("Előadás főcíme", "Tantárgy • Intézet")
prs.add_toc("Tartalom", [("1. Fejezet", "h1"), ("1.1. Szakasz", "h2")])
prs.add_section("01", "Fejezet neve", "Rövid leírás.")
prs.add_content_slide("Cím", [("Bullet 1", "h1"), ("  Albullet", "h2")])
prs.add_table_slide("Táblázat", "1. táblázat: ...", ["Fejléc1","Fejléc2"], [["A","B"]])
prs.add_refs_slide(["[1] Szerző (2024). Cím. Kiadó."])
prs.save("output/prezentacio.pptx")
```

CLI pipeline-módban:
```powershell
python scripts/due_fill.py --week-dir test_outputs/<Tantargy>/N_het
# Output: 5_clean_outputs/N_Prezentacio.pptx
```

### 3.4. Mindmap variáns (due_mindmap_fill.py)

Ha a mindmap template-t (`due_prenetation_template_mindmap.pptx`) használják:

```python
from scripts.due_mindmap_fill import ChapterTree, Chapter, Section, fill_mindmap

tree = ChapterTree([
    Chapter("1", "Első fejezet", [Section("1.1", "Szakasz")]),
])
fill_mindmap("templates/due_prenetation_template_mindmap.pptx", out,
             tree, positions={3: "1.1"}, toc_slides=[1])
```

## 4. Kimenetek

- `5_clean_outputs/N_Prezentacio.pptx` — camera-ready PPTX

## 5. Ellenőrzés

- [ ] `5_clean_outputs/N_Prezentacio.pptx` létrejött
- [ ] DUE chrome (navy sáv, logó, footer) minden dián látható
- [ ] MSc diák `<!-- MSc -->` blokkban vannak
- [ ] 😎 checkpoint: PPTX átnézve (12 → 13-14 checkpoint)

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `Nem található hét-mappa` | `--week-dir` helytelen | Ellenőrizd a `N_het` formátumot |
| `4_wip_outputs/N_Prezentacio.md` hiányzik | 11_typesetter vagy Claude nem generálta | Futtasd előbb a 11. lépést |
| `FileNotFoundError: due_refactored.pptx` | Template hiányzik | `python templates/build_due_potx.py` |
| python-pptx import hiba | Hiányzó csomag | `pip install python-pptx lxml` |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md) — 12. lépés IO
- [scripts/12_pptx_gyarto.py](../../scripts/12_pptx_gyarto.py) — Marp→PPTX
- [scripts/due_fill.py](../../scripts/due_fill.py) — strukturált DUE fill
- [scripts/due_mindmap_fill.py](../../scripts/due_mindmap_fill.py) — mindmap breadcrumb
- [templates/due_refactored.pptx](../../templates/due_refactored.pptx) — DUE template
- [templates/due_presentation_master.potx](../../templates/due_presentation_master.potx) — letölthető sablon
- [14_bsc_filter.md](14_bsc_filter.md) — MSc szűrés

## 8. Visszajelzések

- 💬 NOTE: A `12_pptx_gyarto.py` a Marp slide-struktúrát olvassa és a `due_refactored.pptx` blank layoutját használja — nem a named shape placeholder-eket. A named shape-eket a `due_fill.py` (strukturált mód) kezeli.
- 💬 NOTE: Ha a DUE template módosul, `python templates/build_due_potx.py` regenerálja a `due_presentation_master.potx`-ot és `due_refactored.pptx`-et.
- 💬 NOTE: Mindmap variáns esetén a `due_mindmap_fill.py` automatikusan kitölti a breadcrumb sidebar-t a fejezet-fa alapján (diánkénti pozíció szükséges).

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-30 | 3.0 | Pipeline-integráció: --week-dir támogatás (12_pptx_gyarto, due_fill); due_fill.py + due_mindmap_fill.py dokumentálva; output: 5_clean_outputs/; ❔ QUESTION lezárva |
| 2026-05-26 | 2.0 | Overhaul: template-alapú átírás; §8 Visszajelzések; lépésszám javítva |
| 2026-05-21 | 1.0 | Létrehozva |
