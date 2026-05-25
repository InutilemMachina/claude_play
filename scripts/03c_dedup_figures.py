"""
03c_dedup_figures.py -- Hash-based figure deduplication for figure_catalog.json

MinerU saves figures with their SHA-256 hash as filename. If two pages in the
same (or different) source reference the same image, the path contains the same
hash -- this script marks the later occurrences as duplicate=True.

Only the FIRST occurrence of each hash is kept (duplicate=False).
Downstream tools (09_figure_mapper, 10_notes_collector) skip duplicate=True entries.

figure_catalog.json format: {key: entry_dict} (MinerU dict output).

Usage:
    python scripts/03c_dedup_figures.py --week-dir <path/to/N_het> [options]

    --week-dir   Path to the weekly folder. Required.
    --catalog    Path to figure_catalog.json (default: raw_outputs/figure_catalog.json).
    --dry-run    Print duplicate entries, do not write catalog.
    --reset      Clear all duplicate flags before processing (re-run from scratch).
"""

import argparse
import json
import re
import sys
from pathlib import Path


def extract_hash(path_str):
    """
    Extract the image hash from a MinerU path.
    MinerU filenames are SHA-256 hex strings (64 chars) as stem.
    Example: clean_inputs/src/auto/images/705c8f...bc96b.jpg -> '705c8f...bc96b'
    """
    stem = Path(path_str).stem
    if re.fullmatch(r'[0-9a-fA-F]{64}', stem):
        return stem.lower()
    m = re.search(r'[0-9a-fA-F]{32,}', stem)
    return m.group(0).lower() if m else None


def dedup(catalog_entries, catalog_keys, dry_run, reset):
    """
    Mark duplicates in-place. Returns (n_unique, n_duplicate).
    catalog_entries: list of entry dicts (may be mutated).
    catalog_keys: list of str keys (parallel to catalog_entries), or None for list format.
    """
    if reset:
        for entry in catalog_entries:
            entry.pop("duplicate", None)

    seen = {}  # hash -> first index
    n_dup = 0

    for i, entry in enumerate(catalog_entries):
        path_str = entry.get("path", "")
        h = extract_hash(path_str)

        if h is None:
            entry.setdefault("duplicate", False)
            continue

        if h in seen:
            first_idx = seen[h]
            first = catalog_entries[first_idx]
            key_i = catalog_keys[i] if catalog_keys else str(i)
            key_f = catalog_keys[first_idx] if catalog_keys else str(first_idx)
            if dry_run:
                print(
                    f"  DUP [{key_i}] {entry.get('source','?')} "
                    f"p{entry.get('page','?')} == "
                    f"[{key_f}] {first.get('source','?')} "
                    f"p{first.get('page','?')}  hash={h[:16]}..."
                )
            else:
                entry["duplicate"] = True
            n_dup += 1
        else:
            seen[h] = i
            entry.setdefault("duplicate", False)

    n_unique = len(catalog_entries) - n_dup
    return n_unique, n_dup


def main():
    parser = argparse.ArgumentParser(
        description="Hash-based figure deduplication for figure_catalog.json"
    )
    parser.add_argument("--week-dir", required=True, type=Path,
                        help="Heti mappa (tartalmazza raw_outputs/)")
    parser.add_argument("--catalog", default=None, type=Path,
                        help="figure_catalog.json (default: raw_outputs/figure_catalog.json)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Duplikátumok listázása, katalógus nem frissül")
    parser.add_argument("--reset", action="store_true",
                        help="Meglévő duplicate flag-ek törlése feldolgozás előtt")
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()
    catalog_path = (
        args.catalog or week_dir / "raw_outputs" / "figure_catalog.json"
    ).resolve()

    if not catalog_path.exists():
        sys.exit(f"Nem található: {catalog_path}")

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

    n_unique, n_dup = dedup(catalog_entries, catalog_keys, args.dry_run, args.reset)
    print(f"Egyedi: {n_unique}  |  Duplikátum: {n_dup}")

    if not args.dry_run:
        if is_dict:
            updated = {
                catalog_keys[i]: catalog_entries[i]
                for i in range(len(catalog_entries))
            }
        else:
            updated = catalog_entries
        catalog_path.write_text(
            json.dumps(updated, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"OK Katalógus frissítve: {catalog_path}")


if __name__ == "__main__":
    main()
