A képfájlok elnevezési logikája

Jelenlegi nevezéktan: SHA-256 hash
A forráskód alapján pontosan megérthető, miért olyan hosszú, érthetetlen nevük van a képeknek. Két különböző helyen generálódik hash-alapú fájlnév:

1. PDF-ből kivágott képek (pdf_image_tools.py → cut_image()):

```python
# A fájlnév összetétele:
filename = f"{page_num}_{int(bbox[0])}_{int(bbox[1])}_{int(bbox[2])}_{int(bbox[3])}"
img_path = f"{return_path}_{filename}"   # pl: "image/abc123md5_0_52_294_731"
img_hash256_path = f"{str_sha256(img_path)}.jpg"  # → SHA-256 hash + .jpg
```

Tehát: az `oldalszám + bbox koordináták` sztringből SHA-256 hash képződik → ez lesz a fájlnév. A megjegyzésben is látható az eredeti elképzelés (`img_path.jpg`), de azt felváltotta a hash.

2. Base64-kódolt képek (VLM backend, táblázatokban lévő képek, `html_image_utils.py`):

```python
img_path = f"{str_sha256(b64_data_uri)}.{fmt}"
```

Itt magának a base64 adatnak a SHA-256 hash-e adja a fájlnevet — ez deduplicationt is biztosít (azonos kép = azonos fájlnév).

Van-e beépített lehetőség az átnevezésre?
Röviden: nincs. A kódban nincs semmilyen CLI kapcsoló, konfig opció vagy környezeti változó, amely befolyásolná a képek fájlnevét. A hash-alapú elnevezés mélyen be van égetve a kódba, és a tervezési szándék szerint marad is, mert a deduplication és az egyediség biztosítása érdekében szükséges.

# TODO: Hogyan lehetne mégis caption/sorszám alapján elnevezni?

## Caption/sorszám alapú képelnevezés – részletes megközelítések

A korábbi kutatás alapján a legpraktikusabb megoldás egy **post-processing script**, amely a MinerU által már legenerált `content_list.json` fájlt dolgozza fel. Nincs szükség a MinerU belsejébe nyúlni.

---

### Az adatforrás: mit tartalmaz a `content_list.json`?

Minden képhez ilyesmi struktúra áll rendelkezésre:

```json
{
  "type": "image",
  "img_path": "images/1d6d1d9de5233b0b8bbf...jpg",
  "image_caption": ["Fig. 3. Annual flow duration curves of daily flows..."],
  "image_footnote": [],
  "bbox": [62, 480, 946, 904],
  "page_idx": 1
}
```

Tehát adott: az eredeti hash-es fájlnév, a caption szövege és az oldalszám. Ebből már dolgozhatsz.

---

### 1. megközelítés: Caption szövege alapján (ha van felirat a dokumentumban)

```python
import json, os, shutil, re

def sanitize(text, max_len=60):
    """Caption szövegből filesystem-safe fájlnevet csinál."""
    text = re.sub(r'[\\/*?:"<>|\n\r\t]', '_', text)
    text = re.sub(r'\s+', '_', text.strip())
    text = re.sub(r'_+', '_', text)  # dupla aláhúzások összevonása
    return text[:max_len].rstrip('_')

def rename_images(parse_dir):
    """
    parse_dir: a MinerU kimeneti könyvtár, pl. 'output/Tavakoli2004.../auto'
    """
    cl_path = os.path.join(parse_dir, f"{os.path.basename(parse_dir)}_content_list.json")
    # Valójában a fájlnév az eredeti dokumentum nevéből képződik, pl:
    # output/Tavakoli2004-AnOverview.../auto/Tavakoli2004-AnOverview..._content_list.json
    # Egyszerűbben: keressük meg a content_list.json-t
    for fn in os.listdir(parse_dir):
        if fn.endswith('_content_list.json'):
            cl_path = os.path.join(parse_dir, fn)
            md_stem = fn.replace('_content_list.json', '')
            break

    img_dir = os.path.join(parse_dir, 'images')
    md_path = os.path.join(parse_dir, f'{md_stem}.md')

    with open(cl_path, encoding='utf-8') as f:
        items = json.load(f)

    rename_map = {}
    used_names = set()

    for item in items:
        if item.get('type') not in ('image', 'chart', 'table'):
            continue
        if not item.get('img_path'):
            continue

        old_name = os.path.basename(item['img_path'])
        ext = os.path.splitext(old_name)[1]
        page = item.get('page_idx', 0)

        # Caption lekérése
        caption_list = item.get('image_caption') or item.get('table_caption') or []
        caption = sanitize(caption_list[0]) if caption_list else ''

        # Fájlnév összeállítása
        type_prefix = {'image': 'fig', 'chart': 'chart', 'table': 'table'}
        prefix = type_prefix.get(item['type'], 'img')

        if caption:
            base_stem = f"p{page:03d}_{prefix}_{caption}"
        else:
            base_stem = f"p{page:03d}_{prefix}"

        new_name = f"{base_stem}{ext}"

        # Ütközés kezelése
        counter = 2
        while new_name in used_names:
            new_name = f"{base_stem}_{counter}{ext}"
            counter += 1

        used_names.add(new_name)
        rename_map[old_name] = new_name

    # Fájlok fizikai átnevezése
    for old, new in rename_map.items():
        src = os.path.join(img_dir, old)
        dst = os.path.join(img_dir, new)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"  {old[:20]}...  →  {new}")

    # Markdown hivatkozások frissítése
    if os.path.exists(md_path):
        with open(md_path, encoding='utf-8') as f:
            md = f.read()
        for old, new in rename_map.items():
            md = md.replace(f'images/{old}', f'images/{new}')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md)
        print("Markdown hivatkozások frissítve.")

# Használat:
rename_images(r"C:\...\output\Tavakoli2004-AnOverviewOfCompressorInstabilities\auto")
```

**Eredmény példa:**
```
p001_fig_Fig._3._Annual_flow_duration_curves.jpg
p005_table_Table_2_Significance_of_the_rainfall.jpg
p002_fig.jpg   ← ha nincs caption
```

---

### 2. megközelítés: Sorszámalapú (globális számozás, caption nélkül is működik)

Ha a dokumentumban nincs caption, vagy egyszerűen csak szekvenciális sorszámot szeretnél:

```python
# A fenti kódban a fájlnév-generálási részt cseréld erre:

counters = {'image': 0, 'chart': 0, 'table': 0}

for item in items:
    if item.get('type') not in ('image', 'chart', 'table'):
        continue
    t = item['type']
    counters[t] += 1
    page = item.get('page_idx', 0)
    ext = os.path.splitext(os.path.basename(item['img_path']))[1]

    prefix = {'image': 'fig', 'chart': 'chart', 'table': 'table'}[t]
    new_name = f"{prefix}_{counters[t]:03d}_p{page:03d}{ext}"
    # → fig_001_p001.jpg, fig_002_p003.jpg, table_001_p005.jpg
```

---

### 3. megközelítés: Kombinált – sorszám + caption rövid kulcsszava

```python
# Caption-ből csak az első 2-3 "kulcsszót" veszi ki (eldobja a "Fig. 3." típusú prefixeket)
def extract_keywords(caption, max_words=4):
    # Levágjuk a "Fig. 3.", "Table 2." típusú prefixeket
    caption = re.sub(r'^(fig\.?|figure|table|chart|ábra|táblázat)[\s\d.:]+', 
                     '', caption, flags=re.IGNORECASE)
    words = re.findall(r'[A-Za-z]{4,}', caption)  # csak legalább 4 betűs szavak
    return '_'.join(words[:max_words]).lower()

# Eredmény pl: "fig_003_annual_flow_duration.jpg"
keywords = extract_keywords("Fig. 3. Annual flow duration curves of daily flows")
# → "annual_flow_duration_curves"
new_name = f"{prefix}_{counters[t]:03d}_{keywords}{ext}" if keywords else f"{prefix}_{counters[t]:03d}{ext}"
```

---

### Melyiket válaszd?

| Helyzet | Ajánlott módszer |
|---|---|
| Dokumentumban sok ábracím van | Caption-alapú (1. módszer) |
| Nincs vagy ritka a caption | Sorszámalapú (2. módszer) |
| Vegyes dokumentum | Kombinált (3. módszer) |
| Batch feldolgozás, sok PDF | Sorszámalapú – egyszerűbb és megbízhatóbb |

A legrobusztusabb a **kombinált megközelítés**: ha van caption, abból vesz kulcsszavakat, ha nincs, csak a sorszámot használja. Az oldalszámot érdemes mindig belerakni, mert segít a dokumentumban való navigálásban.


## A `content_list.json` fájl – lehetséges `type` értékek

A fájl generálásának helye: `mineru/backend/pipeline/pipeline_middle_json_mkcontent.py` (pipeline backend) és `mineru/backend/vlm/vlm_middle_json_mkcontent.py` (VLM backend). A típusok a `mineru/utils/enum_class.py`-ban definiált `ContentType` osztályból származnak, és a `docs/en/reference/output_files.md` dokumentációban vannak részletezve.

---

### Pipeline backend – `content_list.json` type értékek

| `type` | Leírás |
|--------|--------|
| `text` | Szöveg / cím (a szintet a `text_level` mező jelzi) |
| `image` | Kép |
| `table` | Táblázat |
| `chart` | Diagram |
| `equation` | Sorközi (interline) képlet |
| `seal` | Bélyegző/pecsét |

---

### VLM backend – kiegészítő `type` értékek (a fentiek mellett)

| `type` | Leírás |
|--------|--------|
| `code` | Kódrészlet vagy algoritmus blokk (`sub_type`: `code` vagy `algorithm`) |
| `list` | Lista vagy hivatkozáslista (`sub_type`: `text` vagy `ref_text`) |
| `header` | Oldalfejléc |
| `footer` | Oldallábléc |
| `page_number` | Oldalszám |
| `aside_text` | Margójegyzet / oldalsáv szöveg |
| `page_footnote` | Oldal lábjegyzet |

---

### Összefoglalás

A `content_list.json`-ban előforduló összes lehetséges `type` érték:

- **`text`** – szöveg és cím (szintet `text_level` különbözteti meg)
- **`image`** – kép
- **`table`** – táblázat
- **`chart`** – diagram
- **`equation`** – képlet (interline)
- **`seal`** – pecsét/bélyegző
- **`code`** *(csak VLM)* – kód / algoritmus blokk
- **`list`** *(csak VLM)* – lista / hivatkozáslista
- **`header`** *(csak VLM)* – fejléc
- **`footer`** *(csak VLM)* – lábléc
- **`page_number`** *(csak VLM)* – oldalszám
- **`aside_text`** *(csak VLM)* – margószöveg
- **`page_footnote`** *(csak VLM)* – lábjegyzet

A fájl az `{original_filename}_content_list.json` névmintával jön létre, és a `MakeMode.CONTENT_LIST` mód aktiválásakor generálódik a `union_make()` függvényen belül.