"""
03-1_qfig_parser.py -- Parse Qfig NLM output and update figure_catalog.json

Reads the nlm_qfig_raw.txt (structured text output from NLM Vision query),
extracts FORRÁS / SZÁM / ALÁÍRÁS / LEÍRÁS / TÉMAKÖR fields per figure/table,
and writes the caption + keywords back into figure_catalog.json.

Matching strategy:
  - Groups catalog entries by source filename.
  - Groups Qfig entries by source filename.
  - Within each source, matches positionally (order = document/page order).
  - If counts differ, matches by min(len) and logs unmatched entries.

figure_catalog.json format: {key: entry_dict} (MinerU dict output).

Usage:
    python scripts/03-1_qfig_parser.py --week-dir <path/to/N_het> [options]

    --week-dir     Path to the weekly folder. Required.
    --qfig-file    Path to nlm_qfig_raw.txt (default: 3_raw_outputs/nlm_qfig_raw.txt).
                   Accepts plain text OR JSON-wrapped NLM CLI output.
    --catalog      Path to figure_catalog.json (default: 3_raw_outputs/figure_catalog.json).
    --dry-run      Print matched pairs to stdout, do not write catalog.
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Parse Qfig output text
# ---------------------------------------------------------------------------

# Each entry block is expected to have lines like:
#   FORRÁS: filename.pdf
#   SZÁM: Figure 3
#   ALÁÍRÁS: caption text
#   LEÍRÁS: description sentence.
#   TÉMAKÖR: keyword1, keyword2

FIELD_RE = re.compile(
    r'^(FORR[AÁ]S|SZ[AÁ]M|AL[AÁ][IÍ]R[AÁ]S|LE[IÍ]R[AÁ]S|T[EÉ]MAK[OÖ]R)\s*:\s*(.*)$',
    re.IGNORECASE
)

FIELD_MAP = {
    'forras': 'source', 'forrás': 'source',
    'szam':   'num',    'szám':   'num',
    'alairas':  'caption', 'aláírás':  'caption',
    'leiras':   'desc',    'leírás':   'desc',
    'temakör':  'keywords', 'témakör': 'keywords',
}


def _canonical(key):
    k = key.lower().strip()
    for variant, canon in FIELD_MAP.items():
        if variant in k:
            return canon
    return k


def parse_qfig_text(text):
    """Parse free-text Qfig output into a list of entry dicts."""
    entries = []
    current = {}

    for line in text.splitlines():
        line = line.strip()
        m = FIELD_RE.match(line)
        if m:
            canon = _canonical(m.group(1))
            value = m.group(2).strip()
            if canon == 'source' and current:
                entries.append(current)
                current = {}
            current[canon] = value
        elif not line and current:
            entries.append(current)
            current = {}

    if current:
        entries.append(current)

    return [e for e in entries if e.get('source')]


def load_qfig(path):
    """Load Qfig file -- plain text OR JSON-wrapped NLM CLI output."""
    raw = path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    try:
        obj = json.loads(raw)
        val = obj.get("value", obj)
        text = val.get("answer", raw)
    except json.JSONDecodeError:
        text = raw
    return parse_qfig_text(text)


# ---------------------------------------------------------------------------
# Match Qfig entries to catalog
# ---------------------------------------------------------------------------

def normalize_source(name):
    """Normalize source filename for comparison (lowercase, strip path)."""
    return Path(name).name.lower()


def match_and_update(catalog_entries, catalog_keys, qfig_entries, dry_run):
    """
    Match Qfig entries to catalog entries by source, positionally.
    Updates catalog_entries in-place. Returns number of matched entries.
    """
    from collections import defaultdict

    cat_by_source = defaultdict(list)
    for i, entry in enumerate(catalog_entries):
        src = normalize_source(entry.get("source", ""))
        cat_by_source[src].append(i)

    qfig_by_source = defaultdict(list)
    for entry in qfig_entries:
        src = normalize_source(entry.get("source", ""))
        qfig_by_source[src].append(entry)

    total_matched = 0

    for src in qfig_by_source:
        cat_indices = cat_by_source.get(src, [])
        qfig_group  = qfig_by_source[src]

        if not cat_indices:
            print(
                f"  WARN  nincs katalógus-bejegyzés: {src} "
                f"({len(qfig_group)} Qfig entry kihagyva)",
                file=sys.stderr
            )
            continue

        n = min(len(cat_indices), len(qfig_group))
        if len(cat_indices) != len(qfig_group):
            print(
                f"  WARN  {src}: katalógus={len(cat_indices)}, "
                f"Qfig={len(qfig_group)} -- pozicionálisan párosítva ({n} db)",
                file=sys.stderr
            )

        for j in range(n):
            cat_idx    = cat_indices[j]
            qfig_entry = qfig_group[j]

            caption  = qfig_entry.get("caption", "").strip()
            desc     = qfig_entry.get("desc", "").strip()
            kw_raw   = qfig_entry.get("keywords", "")
            keywords = [k.strip() for k in re.split(r"[,;]", kw_raw) if k.strip()]

            final_caption = caption if caption else desc

            if dry_run:
                key = catalog_keys[cat_idx] if catalog_keys else str(cat_idx)
                print(
                    f"  [{key}] {src} p{catalog_entries[cat_idx].get('page','?')} "
                    f"-> caption={final_caption!r} kw={keywords}"
                )
            else:
                catalog_entries[cat_idx]["caption"]  = final_caption
                catalog_entries[cat_idx]["keywords"] = keywords
                catalog_entries[cat_idx]["vlm_done"] = True

            total_matched += 1

    return total_matched


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Qfig NLM output -> figure_catalog.json updater"
    )
    parser.add_argument("--week-dir", required=True, type=Path,
                        help="Heti mappa (tartalmazza 3_raw_outputs/)")
    parser.add_argument("--qfig-file", default=None, type=Path,
                        help="nlm_qfig_raw.txt (default: 3_raw_outputs/nlm_qfig_raw.txt)")
    parser.add_argument("--catalog", default=None, type=Path,
                        help="figure_catalog.json (default: 3_raw_outputs/figure_catalog.json)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Párosítás kiírása, katalógus nem frissül")
    args = parser.parse_args()

    week_dir     = args.week_dir.resolve()
    qfig_path    = (args.qfig_file or week_dir / "3_raw_outputs" / "nlm_qfig_raw.txt").resolve()
    catalog_path = (args.catalog   or week_dir / "3_raw_outputs" / "figure_catalog.json").resolve()

    if not qfig_path.exists():
        sys.exit(f"Nem található: {qfig_path}")
    if not catalog_path.exists():
        sys.exit(f"Nem található: {catalog_path}")

    qfig_entries = load_qfig(qfig_path)
    print(f"Qfig entries parsed: {len(qfig_entries)}")

    raw_catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    if isinstance(raw_catalog, dict):
        catalog_keys    = list(raw_catalog.keys())
        catalog_entries = list(raw_catalog.values())
        is_dict = True
    else:
        catalog_keys    = None
        catalog_entries = raw_catalog
        is_dict = False
    print(f"Catalog entries: {len(catalog_entries)}")

    n_matched = match_and_update(catalog_entries, catalog_keys, qfig_entries, args.dry_run)
    print(f"Matched: {n_matched}")

    if not args.dry_run:
        if is_dict:
            updated = {catalog_keys[i]: catalog_entries[i] for i in range(len(catalog_entries))}
        else:
            updated = catalog_entries
        catalog_path.write_text(
            json.dumps(updated, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"OK Katalógus frissítve: {catalog_path}")


if __name__ == "__main__":
    main()
