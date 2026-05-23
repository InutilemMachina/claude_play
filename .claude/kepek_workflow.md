---
title: Kepek Workflow -- Képek integrálása a pipeline-ba
type: meta
status: active
version: 2.0
updated: 2026-05-23
description: Teljes képpipeline: probléma, MinerU futtatás, névadás, figure_catalog, NLM Q5, 05b_figure_mapper, placeholder logika. Cross-cutting: 00c, 03, 05b, 07, 08, 10 lépések.
---

# Kepek Workflow -- Képek Integrálása a Pipeline-ba

# 1. A probléma

A pipeline két különálló forrásból dolgozik összeköttetés nélkül:

```
NLM (szöveg) --> N_Jegyzet.md       (nincs ábra)
MinerU (képek) --> forrasok/kepek/  (nincs szövegkontextus)
```

NLM adja: pedagógiailag szervezett szöveg, citáció-JSON, definíciók.
NLM NEM adja: ábrahivatkozásokat, konkrét figure-számokat, képfájlokat.

MinerU adja: image_N_pP.jpg, table_N_pP.jpg, *_content_list.json.
MinerU NEM adja: pedagógiai relevancia, melyik Jegyzet-szekcióba való.

| Szükséges adat | Honnan | Státusz |
|:--------------|:-------|:--------|
| Figure caption | content_list.json text mező | ✅ elérhető |
| Figure page | content_list.json page_idx | ✅ elérhető |
| Figure source PDF | fájlnév prefix | ✅ elérhető |
| Melyik Jegyzet-szekcióba való | NLM Q5 vagy kézi | ❔ hiányzik |
| Ábrahivatkozás a szövegben | NLM Q5 | ❔ hiányzik |

Megoldás: Kétfázisú megközelítés -- ld. §4 (figure_catalog) és §5 (NLM Q5 + 05b_figure_mapper).

# 2. Pipeline összefoglalás

```
PDF forrás
  → 🐍 00c_mineru_extractor   (PDF → kepek/ + content_list.json → figure_catalog.json)
  → 🔌 01_nlm_query_runner    (Q5 = ábra-lekérdezés NLM-ből)
  → 🤖 05b_figure_mapper      (figure_catalog + Q5 → REVIEW placeholder-ek)
  → 🤖 03_excerpt_block_maker (PLACEHOLDER blokkok a Md-ban)
  → 🤖 07_typesetter          (üres sorok képblokkok körül)
  → 🤖 08_presentation_maker  (képek diákra)
  → 🐍 10_bsc_filter          (MSc kép-blokkok kihagyása)
```

# 3. MinerU futtatás (🐍 00c_mineru_extractor)

## 3.1. Futtatás

```bash
conda run -n mineru python scripts/mineru_pdf.py tests/[tema]/N_het/forrasok/szerzo2024.pdf
conda run -n mineru python scripts/mineru_pdf.py tests/[tema]/N_het/forrasok/
```

Kimenet:
```
forrasok/kepek/
└── szerzo2024/
    └── auto/
        ├── szerzo2024.md
        ├── szerzo2024_content_list.json
        └── images/
            ├── <sha256hash>.jpg
            └── ...
```

⚠️ Extra auto/ könyvtárszint: MinerU kepek/szerzo2024/auto/ alá ír.
A build_figure_catalog.py ezért cl_file.parent.parent.name-t használ.

## 3.2. Átnevezés

```bash
python scripts/mineru_rename.py forrasok/kepek/szerzo2024/auto/ --dry-run
python scripts/mineru_rename.py forrasok/kepek/szerzo2024/auto/
```

Eredmény: fig_001_p001_matrix_profile_overview.jpg
Névadás: {content_type}_{sorszam:03d}_p{oldal:03d}_{caption_kulcsszo}.{ext}

Képeket másold (ne mozgasd) ide: N_het/forrasok/kepek/

## 3.3. SHA-256 névadás -- miért?

MinerU oldalszám + bbox koordinátákból képez SHA-256 hash-t fájlnévként:

```python
filename = f"{page_num}_{int(bbox[0])}_{int(bbox[1])}_{int(bbox[2])}_{int(bbox[3])}"
img_hash256_path = f"{str_sha256(img_path)}.jpg"
```

Base64-kódolt képeknél (VLM, táblázatok): str_sha256(b64_data_uri).ext
Ezért szükséges a mineru_rename.py post-processing.

## 3.4. Ismert korlátok

→ [pitfalls.md §4](pitfalls.md): HTML nem feldolgozható, conda run timeout, 50+ oldalas PDF

# 4. figure_catalog.json

A scripts/build_figure_catalog.py a *_content_list.json fájlokból épít katalógust.

```json
{
  "yeh2016-img-1-p3": {
    "source": "yeh2016_paper.pdf",
    "page": 3,
    "type": "image",
    "caption": "Figure 1: An example matrix profile P and matrix profile index I...",
    "path": "forrasok/kepek/yeh2016_paper/auto/images/fig_001_p003_matrix_profile.jpg",
    "keywords": []
  }
}
```

Helye: N_het/forrasok/figure_catalog.json

# 5. NLM Q5 ábra-lekérdezés

Az 01_nlm_query_runner Q5 queryjét ábra-azonosításra is használjuk.

Q5 prompt minta:
```
Melyik ábra/diagram/táblázat illusztrálja legjobban a következő témákat:
(1) MP vektor és index felépítése, (2) STAMP/STOMP összehasonlítás?
Nevezd meg a szerzőt és az ábra feliratát pontosan.
```

NLM visszaad pl.: "Yeh et al. (2016), Figure 1: 'An example matrix profile...'"
Ez egyeztethető a figure_catalog.json caption mezőivel.

Output: forrasok/nlm_q5_raw.txt

Egyeztetési stratégiák prioritása:
1. NLM Q5 caption match (legmegbízhatóbb)
2. Caption kulcsszó-egyezés (automatikus fallback)
3. Oldalszám-alapú egyezés
4. Kézi mapping

# 6. 05b_figure_mapper lépés

figure_catalog.json + nlm_q5_raw.txt alapján REVIEW flaggel jelölt placeholdereket szúr be:

```markdown
<!-- FIG:yeh2016-img-1-p3:REVIEW -->
![Matrix Profile P és I vektor](forrasok/kepek/yeh2016_paper/auto/images/fig_001_p003.jpg)
*ábra: Matrix Profile P és I vektor felépítése* [ref]
<!-- /FIG -->
```

FIG:auto = kulcsszó-egyezés alapján; FIG:nlm = NLM Q5 javasolta.
Felhasználó elfogadja vagy elveti a REVIEW flaggel jelölt blokkokat.

# 7. Kép-hivatkozás formátumok

## 7.1. Inline kép

```markdown
![Figure 3: Matrix profile (P)](forrasok/kepek/fig_003_p003_matrix_profile_overview.jpg)
*Figure 3. Forrás: Matrix Profile I.pdf, 18. o.*
```

## 7.2. Placeholder (MinerU még nem futott)

```markdown
![PLACEHOLDER: Figure 3](forrasok/kepek/PLACEHOLDER_fig_003.png)
*[Kép betöltendő: Matrix Profile I.pdf, Figure 3, 18. o.]*
```

## 7.3. MSc-jelölt kép blokk

```markdown
<!-- MSc -->
![Figure 7: GPU-STOMP](forrasok/kepek/fig_007_p007_gpu_stomp.jpg)
*Figure 7. Forrás: Matrix Profile II.pdf*
<!-- /MSc -->
```

# 8. Placeholder csere valódi képre

👤 Manuális lépés, egyszer PDF-enként:
1. mineru_pdf.py futtatása
2. mineru_rename.py futtatása
3. Képek másolása forrasok/kepek/-be
4. PLACEHOLDER hivatkozások cseréje valódi fájlnevekre

# 9. Nyitott kérdések

| # | Kérdés | Prioritás |
|:--|:-------|:---------|
| 1 | NLM figure recall megbízhatósága: Q5-tel tesztelni | Magas |
| 2 | 08_presentation_maker: külön Q5 prezentáció-változat kell? | Közepes |
| 3 | 00c párhuzamosítható-e 00b-vel? | Alacsony |

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-22 | 1.0 | kepek_workflow.md létrehozva (operatív workflow) |
| 2026-05-22 | 1.1 | figure_pipeline_design.md létrehozva (design) |
| 2026-05-23 | 2.0 | Egyesítve: figure_pipeline_design.md + mineru_kepek_nevezektan.md beolvasztva |
