---
name: 12_presentation_maker
title: 12_PRESENTATION_MAKER -- Presentation Maker
type: skill
tags: [meta, skill]
status: active
version: 2.0
updated: 2026-05-26
description: N_Jegyzet.md → N_Prezentacio.md (Marp) + N_Prezentacio.pptx (python-pptx). du_template.pptx sablont használ. Pipeline 12. lépése.
---

# 12_PRESENTATION_MAKER

## 1. Cél

A `4_wip_outputs/N_Jegyzet.md`-ből Marp-alapú diasort (`N_Prezentacio.md`) és PPTX fájlt (`5_clean_outputs/N_Prezentacio.pptx`) generál.

## 2. Bemenetek

- `4_wip_outputs/N_Jegyzet.md` -- 11_typesetter kimenet
- `templates/due_presentation_template.pptx` -- 😎 egyszer feltöltve (**🛑 nélküle nem generál PPTX-t**)

## 3. Eljárás

### 3.1. Marp diasor struktúrája

Bevezetés → Főtémák (fejezetenként 1-2 dia) → Összefoglalás → Kérdések

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

### 3.2. PPTX generálás

```bash
python scripts/12_pptx_gyarto.py N_Prezentacio.md --template templates/due_presentation_template.pptx
```

MSc diák: `<!-- MSc -->` blokkon belül -- `14_bsc_filter` kihagyja.

## 4. Kimenetek

- `4_wip_outputs/N_Prezentacio.md` -- Marp forrás
- `5_clean_outputs/N_Prezentacio.pptx` -- camera-ready PPTX

## 5. Ellenőrzés

- [ ] `N_Prezentacio.md` Marp szintaxis helyes
- [ ] `N_Prezentacio.pptx` generálódott
- [ ] Sablon (`due_presentation_template.pptx`) layoutjai alkalmazódtak
- [ ] MSc diák `<!-- MSc -->` blokkban
- [ ] 😎 checkpoint: PPTX átnézve

## 6. Hibakezelés

- Tünet: PPTX generálás sikertelen
- Gyökérok: sablon fájl hiányzik
- Megoldás: `templates/due_presentation_template.pptx` feltöltése

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [scripts/12_pptx_gyarto.py](../../scripts/)
- [14_bsc_filter.md](14_bsc_filter.md) -- MSc szűrés

## 8. Visszajelzések

- ⚠️ WARNING: A `12_pptx_gyarto.py` nem a `due_presentation_template.pptx` layoutjait használja -- a Marp tartalom a sablon-diák után kerül beillesztésre, nem felül. A sablon XML-ben nincs placeholder mapping kódolva. Ez ismert korlát.
- ⚠️ WARNING: Nyers Markdown szintaxis jelenik meg a diákon (`**félkövér**` helyett félkövér formázás). A `12_pptx_gyarto.py` nem értelmezi a Markdown inline formázást python-pptx szinten.
- 💬 NOTE: Nincs TOC-dia; kevés szöveg a diákon (csak bullet-ok, speaker notes hiányzik). A 06_excerpt_block_maker `💡 Lényeg` blokkjai ideálisak lennének speaker notes-ként.
- ❔ QUESTION: Három lehetséges irány: (1) XML-alapú PowerPoint sablon (python-pptx placeholder mapping); (2) Pandoc (Marp MD → PPTX); (3) fejlesztett Marp + Headless Chrome export. Döntés szükséges a következő iteráció előtt.
- 💬 NOTE: A `Mindmap camera-ready` hiányzik: az `N_Mindmap.md` DRAFT státuszban van. A 12. vagy 14. lépés felelőssége definiálandó.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-26 | 2.0 | Overhaul: template-alapú átírás; §8 Visszajelzések; lépésszám javítva (08→12) |
| 2026-05-21 | 1.0 | Létrehozva |
