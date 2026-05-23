---
title: FIGURE_PIPELINE_DESIGN.MD -- Ábrapipeline tervezési dokumentum
type: research
tags: [meta, design, figures]
updated: 2026-05-22
description: Az ábrák kezelésének tervezési problémája és javasolt megoldás. NLM csak szöveget ad, MinerU csak képet. Híd szükséges.
---

# Figure Pipeline Design -- Ábrapipeline Tervezési Dokumentum

# 1. A probléma

A jelenlegi pipeline két különálló forrásból dolgozik, amelyek között nincs összeköttetés:

```
NLM (szöveg) --> 1_Jegyzet.md       (nincs ábra)
MinerU (képek) --> forrasok/kepek/  (nincs szövegkontextus)
```

NLM adja: pedagógiailag szervezett szöveg, citáció-JSON, definíciók.
NLM NEM adja: ábrahivatkozásokat, konkrét figure-számokat, képfájlokat.

MinerU adja: image_N_pP.jpg, table_N_pP.jpg, *_content_list.json
(típus, oldalszám, képfájl-útvonal, szomszédos szövegkörnyezet).
MinerU NEM adja: pedagógiai relevancia, melyik Jegyzet-szekcióba való.

# 2. A hiányzó adatok

| Adat | Honnan kellene | Jelenleg |
|:-----|:--------------|:---------|
| Figure caption | content_list.json text mező | elerheto |
| Figure page | content_list.json page_idx | elerheto |
| Figure source PDF | fájlnév prefix | elerheto |
| Melyik Jegyzet-szekcióba való | --- | HIÁNYZIK |
| Ábrahivatkozás a szövegben | NLM Q5 vagy kézi | HIÁNYZIK |

# 3. Javasolt megoldás -- kétfázisú megközelítés

## 3.1. 00c_mineru_extractor (új lépés)

Helye a pipelineban: 00_references_collector → 00c → 00b_nlm_notebook_setup

Feladata:
1. MinerU futtatás minden forrasok/*.pdf-re (conda run -n mineru)
2. Output: forrasok/kepek/SOURCE_NAME/images/image_N_pP.jpg
3. figure_catalog.json építése a *_content_list.json alapján

figure_catalog.json struktúra:
{
  "yeh2016-img-1-p3": {
    "source": "yeh2016_paper.pdf",
    "page": 3,
    "type": "image",
    "caption": "Figure 1: An example matrix profile P and matrix profile index I...",
    "path": "forrasok/kepek/yeh2016_paper/images/image_1_p3.jpg",
    "keywords": []
  }
}

## 3.2. NLM Q5 -- ábra-lekérdezés (01_nlm_query_runner bővítése)

Az 01 lépés Q5 queryjét ábra-azonosításra is használjuk:

Q5 prompt: "Melyik ábra/diagram/táblázat illusztrálja legjobban a következő
témákat: (1) MP vektor és index felépítése, (2) STAMP/STOMP/SCRIMP++
összehasonlítás, (3) Motívum és diszkord keresés?
Nevezd meg a szerzőt és az ábra feliratát pontosan."

NLM ismeri a PDF-eket, visszaadja pl.:
"Yeh et al. (2016), Figure 1: 'An example matrix profile...'"
→ egyeztethetjük a figure_catalog.json caption mezőivel.

Output: forrasok/nlm_q5_raw.txt

## 3.3. 05b_figure_mapper (új lépés)

Helye: 05_mindmap_manager → 05b → 06_notes_collector

Feladata:
1. figure_catalog.json + nlm_q5_raw.txt beolvasása
2. Q5 szöveges leírás <-> figure_catalog caption egyeztetés
   Fallback: caption kulcsszó-egyezés a Jegyzet szekció-fejlécekkel
3. REVIEW placeholder-ek beszúrása:

  <!-- FIG:yeh2016-img-1-p3:REVIEW -->
  ![Matrix Profile P és I vektor (Yeh et al., 2016, Fig. 1)](forrasok/kepek/yeh2016_paper/images/image_1_p3.jpg)
  *ábra: Matrix Profile P és I vektor felépítése* [ref]
  <!-- /FIG -->

4. A REVIEW flag jelöli: felhasználónak kell elfogadni vagy elvetni.
   Opcionálisan: FIG:auto (kulcsszó-egyezés) vs FIG:nlm (NLM Q5 javasolta).

Felelős: Claude (Python + NLM Q5 egyeztetés)

# 4. Frissített pipeline

00_references_collector
→ 00c_mineru_extractor (ÚJ, 🐍 conda/mineru)
→ 00b_nlm_notebook_setup (🔌 CLI)
→ 01_nlm_query_runner  (Q5 = ábra-query is)
→ 02_source_controller 🛑
→ 03_excerpt_block_maker
→ 04_citations_maker 🛑
→ 05_mindmap_manager
→ 05b_figure_mapper (ÚJ, 🤖 REVIEW flag-ekkel)
→ 06_notes_collector
→ 07_typesetter
→ 08_presentation_maker
→ 09_question_bank_collector
→ 10_bsc_filter

# 5. Egyeztetési stratégiák prioritása

1. NLM Q5 caption match (legmegbízhatóbb: NLM "látta" a PDF-et)
2. Caption kulcsszó-egyezés (automatikus fallback)
3. Oldalszám-alapú egyezés (ha NLM oldalt említ)
4. Kézi mapping (ismeretlen ábrákhoz)

# 6. Nyitott kérdések

- MinerU output minősége kéthasábos akadémiai PDF-nél nem mindig pontos.
  Kell-e kézi kurálás a figure_catalog-hoz?
- NLM figure recall: megbízhatóan emlékszik-e konkrét figure-számokra?
  Tesztelni kell Q5-tel.
- 08_presentation_maker külön ábra-szelekciót igényel (kevesebb, hangsúlyosabb).
  Külön Q5 prezentáció-változat?
- 00c helye: MinerU lassú (1-5 perc/PDF), párhuzamosítható a 00b-vel.
- Képjogok: oktatási célú, forrás megjelölve -- elfogadható.

# Változásjegyzék

- 2026-05-22 -- Létrehozva (PoC teszt alapján azonosított hiány)
