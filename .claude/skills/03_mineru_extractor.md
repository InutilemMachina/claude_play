---
name: 03_mineru_extractor
title: 03_MINERU_EXTRACTOR -- MinerU Extractor
type: skill
tags: [meta, skill, figures]
status: active
version: 3.0
updated: 2026-05-26
description: MinerU futtatása 1_raw_inputs/*.pdf-re. figure_catalog.json építése content_list.json alapján. Pipeline 03. lépése.
---

# 03_MINERU_EXTRACTOR

## 1. Cél

A forrás-PDF-ekből képek, táblázatok és egyenletek kinyerése MinerU-val, és `figure_catalog.json` építése a 09_figure_mapper számára.

## 2. Bemenetek

- `1_raw_inputs/*.pdf` -- forrás PDF-ek
- `scripts/03_run_mineru_pipeline.py` -- ajánlott futtatási szkript

**Előfeltétel:** `mineru` conda környezet aktív.

## 3. Eljárás

### 3.1. Futtatás (ajánlott: pipeline script)

```powershell
# Teljes tantárgy (minden N_*/1_raw_inputs/*.pdf)
conda run -n mineru python scripts/03_run_mineru_pipeline.py --root <tantargy_mappa>

# Nagy fájl figyelmeztetési határ módosítása (alap: 20 MB)
conda run -n mineru python scripts/03_run_mineru_pipeline.py --root <tantargy_mappa> --warn-mb 50
```

**Manuális (egy PDF):**
```powershell
conda run -n mineru python scripts/03_util_mineru_pdf.py 1_raw_inputs/ --output 2_clean_inputs/kepek/
conda run -n mineru python scripts/03_util_figure_catalog.py 2_clean_inputs/kepek/
```

MinerU futása lassú: **1-5 perc/PDF**. A feldolgozás 😎 manuális lépésként kezelendő (külön terminálból), mivel az MCP timeout ~30s.

### 3.2. figure_catalog.json séma

A `03_util_figure_catalog.py` a `*_content_list.json` fájlokból építi a katalógust:

```json
{
  "yeh2016-img-1-p3": {
    "source": "yeh2016_paper.pdf",
    "page": 3,
    "type": "image",
    "caption": "Figure 1: An example matrix profile...",
    "path": "2_clean_inputs/yeh2016_paper/images/fig_001_p003.jpg",
    "keywords": [],
    "vlm_done": false
  }
}
```

Generált kulcs formátuma: `{source_stem}-{type}-{n}-p{page}`

Mezők:
- `type`: `image`, `table`, `chart`, `equation`, `seal`
- `caption`: `image_caption`, `table_caption`, `chart_caption` (lista)
- `keywords`: a 03-1_qfig_parser tölti ki
- `vlm_done`: `true` ha caption + keywords már feltöltve

### 3.3. Ismételt futtatás

A `03_util_mineru_pdf.py` `SKIP_FILES` listával kihagyja a már kész PDF-eket.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `2_clean_inputs/<forrasnev>/images/*.jpg` | Átnevezett képek |
| `2_clean_inputs/<forrasnev>/<forrasnev>.md` | Teljes szöveg MinerU-Markdown-ban |
| `3_raw_outputs/figure_catalog.json` | Egységes katalógus (minden PDF-ből) |

## 5. Ellenőrzés

- [ ] Minden PDF-hez létrejött `2_clean_inputs/<forrasnev>/` mappa
- [ ] `figure_catalog.json` létezik, bejegyzések `keywords: []` mezőkkel
- [ ] Képek számozása `fig_NNN_pPPP_*.jpg` formátumban
- [ ] Részleges futás: `source_count` mező jelzi a feldolgozott fájlok számát

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `2_clean_inputs/` létrejött, de 0 kép | MinerU részlegesen futott | `conda run -n mineru python scripts/03_run_mineru_pipeline.py` újrafuttatás |
| Output `<stem>/<stem>/auto/` dupla szint | MinerU maga hozza létre `<stem>/`-t az `-o` alatt | `-o clean_dir` (nem `clean_dir/<stem>`); MinerU generálja a `<stem>/` szintet |
| HTML fájl nem dolgozható fel | MinerU csak PDF/DOCX | Weblapot Edge → Nyomtatás → PDF mentése, `--file` a PDF-re |
| `conda run + Start-Job` visszatér, MinerU még fut | `conda run` nem vár gyermekprocesszre | MinerU futtatása Git Bash-ből szinkron módon; ne `Start-Job` |
| conda interaktív bug-report prompt blokkolja a futást | conda hibát észlel és megkérdezi, küldje-e a jelentést | `echo N \| conda run ...` -- a prompt automatikusan elutasítva |
| 50+ oldalas PDF-nél óráig fut | MinerU oldalanként, lineárisan | `--warn-pages 50` figyelmeztet; `--yes` kihagyja; `--backend vlm-sglang` GPU-n gyorsabb |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [scripts/03_run_mineru_pipeline.py](../../scripts/03_run_mineru_pipeline.py)
- [09_figure_mapper.md](09_figure_mapper.md) -- a catalog felhasználója

## 8. Visszajelzések

- ✅ MinerU futás sikeres (tesztelve 2026-05-27, meta_file_updates_test): 1_het 4/4 mappa, 2_het 4/4 mappa. Minden forráshoz: `.md` szöveg + `content_list.json` + képek keletkeztek. Részletek: 1_het: ahrens(20 kép), bekele(35), mit(1), oppenheim(38). 2_het: chattopadhyay(3), grundfos(5), nagyi(24), tavakoli(6). Kimenet struktúra: `2_clean_inputs/<forrasnev>/auto/` (MinerU `auto/` aldirektóriát hoz létre).
- 🔲 TODO: MinerU automatikusan induljon, miután a user a forrásokat jóváhagyta és auditálta
- 💬 NOTE: A `03_run_mineru_pipeline.py --root` argumentuma a **tantárgy gyökerét** várja (pl. `test_outputs/meta_file_updates_test`), nem a heti mappát. A `discover_notebooks()` `root/N_*/1_raw_inputs/*.pdf` mintát keres -- ha heti mappa kerül `--root`-ba, a script "nincs PDF" hibával leáll.
- 🔲 TODO: A user nem kap vizuális visszajelzést a futásról: hány hét / hány forrás / MinerU feldolgozási %-os állapot. Megoldás: a script indítson egy látható terminálablakot (`Start-Process cmd` vagy Windows Terminal), amelyben a rich progress bar megjelenik. Jelenlegi állapot: a PowerShell háttérprocessz stdout-ja nem látszik.
- 🔲 TODO: Nem egyértelmű, hogy a MinerU CPU-t vagy GPU-t használ-e, és hány magot. A pipeline elve: nagyobb teljesítménytől induljon (GPU ha elérhető, CPU fallback). A terminálkimenetnek tájékoztatni kell: backend típusa (pipeline/vlm-sglang), GPU/CPU detektálás eredménye, magszám. Jelenleg ez hiányzik a script outputból. (input_audit_trail.md kész + citations_seed.json UUID-ek kitöltve). Jelenleg manuális lépés -- a 02 checkpoint után automatikusan triggerelendő.
- 🔲 TODO: Nem-PDF forrástípusok (HTML, PPTX, DOCX) feldolgozása nincs meghatározva. Minden forrástípushoz definiálni kell egy determinisztikus extraktort -- részletek a pipeline.md §6-ban.
- 🔲 TODO: GPU-használat ellenőrizendő: a `03_run_mineru_pipeline.py` `-b pipeline` backend CPU-t vagy GPU-t használ-e alapértelmezetten? Ha CPU, explicit GPU-flag szükséges a gyorsabb futáshoz.
- ✅ Oldalszám-alapú figyelmeztetés kész: `--warn-pages 50` (default), `--yes` flag az automatizált futtatáshoz, `--backend` GPU-választáshoz (`vlm-sglang`). `03_run_mineru_pipeline.py` v2 (2026-05-26).
- 💬 NOTE: MinerU a kimenetet `2_clean_inputs/<forrasnev>/auto/` alá írja, nem közvetlenül `<forrasnev>/` alá. Esztétikailag nem ideális, de a pipeline downstream lépései (03_util_figure_catalog.py, 05_assemble.py stb.) valószínűleg kezelik -- ellenőrzendő.
- 💬 NOTE: Kéthasábos akadémiai PDF-nél a caption és a kép párosítása nem mindig pontos.
- 💬 NOTE: Egyenlet-képek (`equation_N_pP.jpg`) általában nem kerülnek a Jegyzetbe (LaTeX-képletként szerepelnek).
- 💬 NOTE: MinerU MCP-n át nem futtatható (hard timeout ~30s). Természetes pipeline-szünet: 😎 manuálisan vagy külön terminálból indítandó.
- 🔲 TODO: `scripts/03_util_figure_catalog.py` szintaktikai hiba: `run_vlm_on_catalog()` függvény paramétere `2_clean_inputs_dir: Path,` (sor 119) és `week_dir = 2_clean_inputs_dir.parent` (sor 128) -- érvénytelen Python azonosító (számmal kezdődik). A fájl egyáltalán nem importálható/futtatható -- Python parse error. A `build_catalog()` és `main()` logika helyes, csak a `run_vlm_on_catalog()` rontja el az egész fájlt. Javítandó: `clean_inputs_dir` névre átnevezni mindkét előfordulást.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-26 | 3.0 | Overhaul: template-alapú átírás; §8 Visszajelzések; kepek_workflow.md tartalom konszolidálva; pipeline diagram eltávolítva |
| 2026-05-24 | 2.0 | Kepek_workflow.md beolvasztva; 03_run_mineru_pipeline.py ajánlottá téve |
| 2026-05-23 | 1.2 | Útvonalak frissítve: forrasok/ → 2_clean_inputs/ |
| 2026-05-22 | 1.0 | Létrehozva |
