#!/usr/bin/env python3
"""
Build figure_catalog.json from MinerU *_content_list.json files.

Usage:
    python build_figure_catalog.py <kepek_dir> [--output figure_catalog.json]

Example:
    python build_figure_catalog.py 1_het/forrasok/kepek/
    python build_figure_catalog.py 1_het/forrasok/kepek/ --output 1_het/forrasok/figure_catalog.json

Output schema per entry:
    key  : "{source_stem}-{type}-{n}-p{page}"
    value: {
        "source":   "yeh2016_paper.pdf",
        "page":     3,                          # 1-based
        "type":     "image",                    # image | table | chart
        "caption":  "...",                      # first 200 chars from content_list
        "path":     "forrasok/kepek/yeh2016_paper/images/image_1_p3.jpg",
        "keywords": []                          # filled by 05b_figure_mapper
    }
"""

import argparse
import json
import sys
from pathlib import Path

INCLUDE_TYPES = {"image", "table", "chart"}


def build_catalog(kepek_dir: Path) -> dict:
    """Traverse kepek_dir for *_content_list.json files and build a unified catalog."""
    catalog: dict = {}

    cl_files = sorted(kepek_dir.rglob("*_content_list.json"))
    if not cl_files:
        print(f"[Warning] No *_content_list.json files found under: {kepek_dir}")
        return catalog

    for cl_file in cl_files:
        # MinerU output: kepek/SOURCE/auto/SOURCE_content_list.json
        # cl_file.parent is the auto/ dir; .parent.parent is the SOURCE dir
        auto_dir    = cl_file.parent
        source_dir  = auto_dir.parent
        source_stem = source_dir.name              # e.g. "yeh2016_paper"
        source_pdf  = source_stem + ".pdf"

        try:
            items = json.loads(cl_file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  [Error] Cannot read {cl_file}: {e}")
            continue

        type_counters: dict[str, int] = {}
        added = 0

        for item in items:
            ctype = item.get("type")
            if ctype not in INCLUDE_TYPES:
                continue

            img_rel = item.get("img_path", "")
            if not img_rel:
                continue

            page = item.get("page_idx", 0) + 1      # convert to 1-based

            type_counters[ctype] = type_counters.get(ctype, 0) + 1
            n = type_counters[ctype]
            new_name = f"{ctype}_{n}_p{page}{Path(img_rel).suffix}"

            # Relative path from the subject week folder root
            # MinerU writes to kepek/SOURCE/auto/images/
            rel_path = f"forrasok/kepek/{source_stem}/auto/images/{new_name}"

            # Caption: prefer dedicated caption fields, fall back to inline text
            caption_list = (
                item.get("image_caption")
                or item.get("table_caption")
                or item.get("chart_caption")
                or []
            )
            if caption_list:
                caption = caption_list[0].strip()[:200]
            else:
                caption = item.get("text", "").strip()[:200]

            key = f"{source_stem}-{ctype}-{n}-p{page}"
            catalog[key] = {
                "source":   source_pdf,
                "page":     page,
                "type":     ctype,
                "caption":  caption,
                "path":     rel_path,
                "keywords": [],      # populated later by 05b_figure_mapper
            }
            added += 1

        print(f"  {source_stem}: {added} entries")

    return catalog


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build figure_catalog.json from MinerU content_list files."
    )
    parser.add_argument(
        "kepek_dir",
        help="Directory produced by mineru_pdf.py (contains per-source subfolders)"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output path for figure_catalog.json (default: <kepek_dir>/../figure_catalog.json)"
    )
    args = parser.parse_args()

    kepek_dir = Path(args.kepek_dir)
    if not kepek_dir.is_dir():
        sys.exit(f"[Error] Directory not found: {kepek_dir}")

    # Default output: one level above kepek_dir (i.e. forrasok/figure_catalog.json)
    out_path = Path(args.output) if args.output else kepek_dir.parent / "figure_catalog.json"

    print(f"Building figure catalog from: {kepek_dir}")
    catalog = build_catalog(kepek_dir)

    out_path.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\nWrote {len(catalog)} entries -> {out_path}")


if __name__ == "__main__":
    main()
