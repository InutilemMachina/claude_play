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
# --root = test_outputs/<TantargyNeve>  (a tantárgy mappája, NEM a heti mappa!)
# --no-capture-output: kötelező, különben a terminal nem mutat semmit!
# chcp 65001: kötelező a box-drawing karakterek helyes megjelenítéséhez (UTF-8 konzol)
chcp 65001
conda run -n mineru --no-capture-output python scripts/03_run_mineru_pipeline.py --root test_outputs/<TantargyNeve>

# Nagy fájl figyelmeztetési határ módosítása (alap: 20 MB)
conda run -n mineru --no-capture-output python scripts/03_run_mineru_pipeline.py --root test_outputs/<TantargyNeve> --warn-mb 50
```

**Manuális (egy PDF):**
```powershell
conda run -n mineru python scripts/03_util_mineru_pdf.py 1_raw_inputs/ --output 2_clean_inputs/kepek/
conda run -n mineru python scripts/03_util_figure_catalog.py 2_clean_inputs/kepek/
```

⚠️ **MinerU futása lassú: 1-5 perc/PDF.** Két eset: (1) Ha **Claude futtatja** a Bash tool-lal: ~30s után timeout-ol, visszajelzés nem jelenik meg — ilyenkor külön PowerShell / Windows Terminal ablakot kell nyitni. (2) Ha a **user manuálisan futtatja** a Claude Code beépített termináljában: rendben lefut, csak türelem kell (a prompt visszatéréséig). Befejezéskor a `2_clean_inputs/<forrasnev>/` almappák megjelennek.

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
- ✅ **Nincs terminál-visszajelzés -- javítva (2026-05-30).** Gyökérok: `conda run` alapból elnyeli a subprocess stdout-ját. Fix: `--no-capture-output` flag a conda run hívásban. A §3 parancsok frissítve.
- 🔲 TODO: Nem egyértelmű, hogy a MinerU CPU-t vagy GPU-t használ-e, és hány magot. A pipeline elve: nagyobb teljesítménytől induljon (GPU ha elérhető, CPU fallback). A terminálkimenetnek tájékoztatni kell: backend típusa (pipeline/vlm-sglang), GPU/CPU detektálás eredménye, magszám. Jelenleg ez hiányzik a script outputból. (input_audit_trail.md kész + citations_seed.json UUID-ek kitöltve). Jelenleg manuális lépés -- a 02 checkpoint után automatikusan triggerelendő.
- 🔲 TODO: Nem-PDF forrástípusok (HTML, PPTX, DOCX) feldolgozása nincs meghatározva. Minden forrástípushoz definiálni kell egy determinisztikus extraktort -- részletek a pipeline.md §6-ban.
- 💬 NOTE: **HTML extrakció navigációs zaj (tesztelve 2026-05-30, mini2).** A `03_util_source_extractor.py` BeautifulSoup-alapú HTML extrakció a `<nav>`, menü és fejléc elemeket nem szűri ki -- ezek listaként bekerülnek a `.md` kimenetbe (pl. `- Főoldal`, `- Kapcsolat`). Érdemi szöveges tartalom helyes, de a navigációs elemek zaj. Hatás: ha az NLM-be URL-ként töltöttük fel a forrást (nem fájlként), ez a `.md` csak helyi szöveges feldolgozáshoz használatos -- a zaj minimális hatású. Ha fájlként kerülne NLM-be, a navigációs listák félrevezethetnék a lekérdezéseket. Fix: `<nav>`, `<header>`, `<footer>`, `<aside>` tagek szűrése a BeautifulSoup feldolgozás előtt.
- ⚡ **`03_util_figure_catalog.py` nem halmoz — ha a catalog fájl már létezik, csak betölti, nem bővíti (tesztelve 2026-05-30, mini2).** Ha egymás után hívják különböző `kepek_dir`-rel, a második hívás nem adja hozzá az új forrásokat. Helyes hívás: a `2_clean_inputs/` gyökeret add meg, ne az egyes `SOURCE/auto/` almappákat — az `rglob` megtalál minden `*_content_list.json`-t. Ha újra kell buildelni: töröld a meglévő catalog fájlt, majd: `python scripts/03_util_figure_catalog.py <week_dir>/2_clean_inputs --output <week_dir>/3_raw_outputs/figure_catalog.json`
- 🔲 TODO: GPU-használat ellenőrizendő: a `03_run_mineru_pipeline.py` `-b pipeline` backend CPU-t vagy GPU-t használ-e alapértelmezetten? Ha CPU, explicit GPU-flag szükséges a gyorsabb futáshoz.
- 🔲 TODO: **Kettős script UX probléma -- egységes belépési pont hiányzik (tesztelve 2026-05-30, mini2).** A 03. lépéshez jelenleg két különálló parancs kell: (1) `python scripts/03_util_source_extractor.py --week-dir ...` a nem-PDF forrásokhoz; (2) `conda run -n mineru python scripts/03_run_mineru_pipeline.py --root ...` a PDF-ekhez. A user jogosan várja, hogy a `--week-dir` parancs MINDEN forrást feldolgoz. A szétválasztás oka: MinerU külön conda környezetet igényel. Megoldási irányok: (a) wrapper script (`03_all.py`), amely mindkettőt hívja sorban; (b) `03_util_source_extractor.py` detektálja a PDF-eket és figyelmeztet hogy MinerU-val kell futtatni őket; (c) dokumentáció egyértelműsítése a pipeline.md §1 IO táblájában.
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
