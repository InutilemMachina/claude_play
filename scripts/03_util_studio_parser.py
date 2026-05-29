"""
03_util_studio_parser.py -- NLM Data Tables Studio output feldolgozó

Kezeli a C.1/C.3/C.4 Prompt output fájlokat és pipeline-kompatibilis
kimeneteket generál belőlük.

Üzemmódok:
  --c1  nlm_c1_forrasattekinto_raw.md  → 4_wip_outputs/N_Forrasattekinto.md
  --c3  nlm_c3_abrajegyzek_raw.md      → figure_catalog.json (keywords frissítés)
  --c4  nlm_c4_kerdesbank_raw.md       → 4_wip_outputs/N_Kerdesek.md

Bemeneti formátum: NLM Data Tables Studio GFM Markdown tábla
  - Fejléc nélküli: az első sor adat, második sor `| --- |` szeparátor
  - Fejléces: első sor fejléc, második sor szeparátor, többi adat

Usage:
    python scripts/03_util_studio_parser.py --week-dir <path> --c3
    python scripts/03_util_studio_parser.py --week-dir <path> --c1
    python scripts/03_util_studio_parser.py --week-dir <path> --c4
    python scripts/03_util_studio_parser.py --week-dir <path> --all
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Markdown table parser (fejléc nélküli is)
# ---------------------------------------------------------------------------

def parse_md_table(text: str) -> list[list[str]]:
    """
    Parse a GFM Markdown table into a list of row lists.
    Skips the separator row (|---|). Works with or without header row.
    Returns all non-separator rows as lists of cell strings.
    """
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line or not line.startswith('|'):
            continue
        if re.match(r'^\|[\s\-:|]+\|', line):
            continue  # separator row
        cells = [c.strip() for c in line.strip('|').split('|')]
        rows.append(cells)
    return rows


def normalize_source_name(name: str) -> str:
    """Strip citation suffixes like [1], trailing whitespace."""
    return re.sub(r'\s*\[\d+\]\s*$', '', name).strip()


# ---------------------------------------------------------------------------
# C.1 — Forrásáttekintő
# ---------------------------------------------------------------------------

C1_COLS = ['forrás', 'szerzők', 'típus', 'témakör', 'bsc_fogalmak',
           'msc_kiegészítés', 'kulcsadatok', 'felhasználhatóság', 'hivatkozás']


def process_c1(week_dir: Path) -> None:
    raw = week_dir / "3_raw_outputs" / "nlm_c1_forrasattekinto_raw.md"
    wip = week_dir / "4_wip_outputs"
    seed_path = week_dir / "1_raw_inputs" / "citations_seed.json"

    if not raw.exists():
        sys.exit(f"[C1] Nem található: {raw}")

    rows = parse_md_table(raw.read_text(encoding='utf-8-sig'))
    if not rows:
        sys.exit("[C1] Üres tábla vagy nem ismert formátum.")

    week_num = 1
    if seed_path.exists():
        seed = json.loads(seed_path.read_bytes().decode('utf-8-sig'))
        week_num = seed.get('_meta', {}).get('week', 1)

    # Build Markdown output
    out_lines = [
        f"# {week_num}. Forrásáttekintő\n",
        "_Forrás: NLM Data Tables Studio (Prompt C.1)_\n",
        "",
    ]
    for row in rows:
        if len(row) < 2:
            continue
        source = normalize_source_name(row[0]) if row else "?"
        authors = row[1] if len(row) > 1 else ""
        ftype   = row[2] if len(row) > 2 else ""
        topic   = row[3] if len(row) > 3 else ""
        bsc_kw  = row[4] if len(row) > 4 else ""
        msc_ext = row[5] if len(row) > 5 else ""
        keydata = row[6] if len(row) > 6 else ""
        use     = row[7] if len(row) > 7 else ""

        out_lines += [
            f"## {source}",
            "",
            f"**Szerzők/Év:** {authors}  ",
            f"**Típus:** {ftype}  ",
            f"**Témakör:** {topic}",
            "",
            f"**BSc kulcsfogalmak:** {bsc_kw}",
            f"**MSc kiegészítés:** {msc_ext}",
            f"**Kulcsadatok:** {keydata}",
            f"**Pipeline felhasználhatóság:** {use}",
            "",
        ]

    out_path = wip / f"{week_num}_Forrasattekinto.md"
    wip.mkdir(parents=True, exist_ok=True)
    out_path.write_text('\n'.join(out_lines), encoding='utf-8')
    print(f"[C1] OK -> {out_path} ({len(rows)} forrás)")


# ---------------------------------------------------------------------------
# C.3 — Ábrajegyzék (figure_catalog.json keywords frissítés)
# ---------------------------------------------------------------------------

def _match_source(catalog_key: str, query_source: str) -> bool:
    """Fuzzy source match: catalog key starts with source stem."""
    q = query_source.lower().replace(' ', '_').replace('.pdf', '').replace('.', '')
    k = catalog_key.lower()
    # Try stem match
    for sep in ['-image-', '-table-', '-chart-']:
        if sep in k:
            stem = k.split(sep)[0]
            if q in stem or stem in q:
                return True
    return False


_EN_HU_SYNONYMS = {
    "camera":        ["kamera"],
    "detector":      ["detektor"],
    "optical":       ["optika", "optikai"],
    "optics":        ["optika"],
    "atmospheric":   ["atmoszferikus", "légköri"],
    "attenuation":   ["csillapítás", "elnyelés"],
    "transmission":  ["transzmisszió", "áteresztés"],
    "absorption":    ["abszorpció", "elnyelés"],
    "spectral":      ["spektrális", "spektrum"],
    "blackbody":     ["feketetest"],
    "planck":        ["planck"],
    "wavelength":    ["hullámhossz"],
    "temperature":   ["hőmérséklet"],
    "radiation":     ["sugárzás"],
    "emissivity":    ["emisszivitás"],
    "infrared":      ["infravörös"],
    "diagram":       ["diagram"],
    "signal":        ["jel"],
    "processing":    ["feldolgozás"],
    "humidity":      ["páratartalom"],
    "windows":       ["ablakok"],
    "gases":         ["gázok"],
    "materials":     ["anyag", "anyagok"],
    "detector":      ["detektor"],
    "response":      ["válasz"],
    "emittance":     ["kisugárzás"],
    "curves":        ["görbék"],
}


def _expand_keywords_with_hu(keywords: list[str]) -> list[str]:
    """Add Hungarian synonyms for English keywords."""
    expanded = list(keywords)
    seen = set(k.lower() for k in expanded)
    for kw in keywords:
        kl = kw.lower().strip()
        for hu in _EN_HU_SYNONYMS.get(kl, []):
            if hu not in seen:
                expanded.append(hu)
                seen.add(hu)
    return expanded


def process_c3(week_dir: Path) -> None:
    raw  = week_dir / "3_raw_outputs" / "nlm_c3_abrajegyzek_raw.md"
    cat_path = week_dir / "3_raw_outputs" / "figure_catalog.json"

    if not raw.exists():
        sys.exit(f"[C3] Nem található: {raw}")
    if not cat_path.exists():
        sys.exit(f"[C3] figure_catalog.json nem található: {cat_path}")

    rows = parse_md_table(raw.read_text(encoding='utf-8-sig'))
    catalog = json.loads(cat_path.read_text(encoding='utf-8'))

    # C.3 column order: source | figure_num | caption | keywords | citation
    # (NLM outputs this without header row)
    updated = 0
    unmatched = []

    for row in rows:
        if len(row) < 4:
            continue
        src_raw   = normalize_source_name(row[0])
        fig_num   = row[1].strip()
        caption   = row[2].strip()
        kw_raw    = row[3].strip()

        keywords = _expand_keywords_with_hu(
            [k.strip() for k in kw_raw.split(',') if k.strip()]
        )

        # Find matching catalog entry (by source + order)
        candidates = [k for k in catalog if _match_source(k, src_raw)]
        if not candidates:
            unmatched.append(src_raw)
            continue

        # Pick best match: prefer entry where caption overlaps
        best = None
        best_score = -1
        cap_tokens = set(re.findall(r'\w{3,}', caption.lower()))
        for ckey in candidates:
            existing_cap = catalog[ckey].get('caption', '').lower()
            score = len(cap_tokens & set(re.findall(r'\w{3,}', existing_cap)))
            if score > best_score:
                best_score, best = score, ckey

        if best:
            # C.3 NLM keywords always win over caption-based fallback keywords
            catalog[best]['keywords'] = keywords
            if caption and (not catalog[best].get('caption') or
                            catalog[best]['caption'] == '(automatikus felirat)'):
                catalog[best]['caption'] = caption
            updated += 1
            print(f"  [C3] {best} <- {keywords[:3]}...")

    cat_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"[C3] OK: {updated} bejegyzés frissítve, {len(unmatched)} nem illeszkedett")
    if unmatched:
        print(f"  Nem illeszkedett: {unmatched}")


# ---------------------------------------------------------------------------
# C.4 — Kérdésbank
# ---------------------------------------------------------------------------

DIFF_MAP = {
    '1': 'Alapfogalom', '2': 'Alkalmazás',
    '3': 'Elemzés', '4': 'Értékelés', '5': 'Szintézis',
}


def process_c4(week_dir: Path) -> None:
    raw = week_dir / "3_raw_outputs" / "nlm_c4_kerdesbank_raw.md"
    wip = week_dir / "4_wip_outputs"
    seed_path = week_dir / "1_raw_inputs" / "citations_seed.json"

    if not raw.exists():
        sys.exit(f"[C4] Nem található: {raw}")

    rows = parse_md_table(raw.read_text(encoding='utf-8-sig'))
    if not rows:
        sys.exit("[C4] Üres tábla vagy nem ismert formátum.")

    week_num = 1
    if seed_path.exists():
        seed = json.loads(seed_path.read_bytes().decode('utf-8-sig'))
        week_num = seed.get('_meta', {}).get('week', 1)

    # C.4 columns: téma | kulcsállítás | helyes válasz | nehézség | szint | forrás
    out_lines = [f"# {week_num}. Kérdésbank\n",
                 "_Forrás: NLM Data Tables Studio (Prompt C.4)_\n", ""]

    bsc_qs, msc_qs = [], []
    for i, row in enumerate(rows, 1):
        if len(row) < 4:
            continue
        tema    = row[0].strip()
        kerdes  = row[1].strip()
        valasz  = row[2].strip()
        diff    = row[3].strip() if len(row) > 3 else "?"
        szint   = row[4].strip() if len(row) > 4 else "BSc"
        forras  = row[5].strip() if len(row) > 5 else ""

        diff_label = DIFF_MAP.get(diff, diff)
        entry = (
            f"**K{i}** `{tema}` — SZINT:{diff} ({diff_label})\n\n"
            f"{kerdes}\n\n"
            f"**Helyes válasz:** {valasz}\n\n"
            f"_Forrás: {forras}_\n"
        )
        if 'msc' in szint.lower():
            msc_qs.append(entry)
        else:
            bsc_qs.append(entry)

    if bsc_qs:
        out_lines += ["## BSc kérdések\n"]
        for q in bsc_qs:
            out_lines += [q, "---\n"]

    if msc_qs:
        out_lines += ["<!-- MSc -->\n", "## MSc kérdések\n"]
        for q in msc_qs:
            out_lines += [q, "---\n"]
        out_lines.append("<!-- /MSc -->\n")

    out_path = wip / f"{week_num}_Kerdesek.md"
    wip.mkdir(parents=True, exist_ok=True)
    out_path.write_text('\n'.join(out_lines), encoding='utf-8')
    print(f"[C4] OK -> {out_path} ({len(bsc_qs)} BSc, {len(msc_qs)} MSc kérdés)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="NLM Data Tables Studio output feldolgozó (C.1 / C.3 / C.4)"
    )
    parser.add_argument("--week-dir", required=True, type=Path)
    parser.add_argument("--c1", action="store_true", help="Forrásáttekintő feldolgozása")
    parser.add_argument("--c3", action="store_true", help="Ábrajegyzék → figure_catalog keywords")
    parser.add_argument("--c4", action="store_true", help="Kérdésbank táblázat → N_Kerdesek.md")
    parser.add_argument("--all", dest="all_", action="store_true", help="Mind a három")
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()
    if not week_dir.exists():
        sys.exit(f"HIBA: {week_dir} nem található")

    run_all = args.all_
    if run_all or args.c1:
        process_c1(week_dir)
    if run_all or args.c3:
        process_c3(week_dir)
    if run_all or args.c4:
        process_c4(week_dir)
    if not (run_all or args.c1 or args.c3 or args.c4):
        parser.print_help()


if __name__ == "__main__":
    main()
