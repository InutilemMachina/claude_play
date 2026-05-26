#!/usr/bin/env python3
"""
MinerU post-processing: rename output images by content type and sequence number.

Naming convention: {content_type}_{n}_p{page}.{ext}
  e.g.  image_1_p3.jpg, table_2_p5.jpg, equation_1_p2.jpg

Counter is per content_type, no leading zeros.
Page number is 1-based (page_idx + 1), matching the PDF reader page number.

Usage:
    python 03_util_mineru_rename.py <output_root> [--dry-run]
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

RENAME_TYPES = {"image", "table", "chart", "equation", "seal"}


def find_content_lists(root: Path) -> list[tuple[Path, Path]]:
    return [(p, p.parent) for p in sorted(root.rglob("*_content_list.json"))]


RenameEntry = tuple[str, str]  # (new_name, caption)


def build_rename_map(items: list, img_dir: Path) -> dict[str, RenameEntry]:
    """Return {old_filename: (new_filename, caption)} for all renameable items."""
    counters: dict[str, int] = {}
    rename_map: dict[str, RenameEntry] = {}
    used_names: set[str] = set()

    for item in items:
        content_type = item.get("type")
        if content_type not in RENAME_TYPES:
            continue

        img_path_rel = item.get("img_path")
        if not img_path_rel:
            continue

        old_name = Path(img_path_rel).name
        if not (img_dir / old_name).exists():
            continue

        ext = Path(old_name).suffix
        page = item.get("page_idx", 0) + 1  # 1-based: matches PDF reader page number
        counters[content_type] = counters.get(content_type, 0) + 1
        n = counters[content_type]

        base = f"{content_type}_{n}_p{page}"
        new_name = f"{base}{ext}"

        # collision guard (edge case: two items of same type on same page with same ext)
        collision = 2
        while new_name in used_names:
            new_name = f"{base}_{collision}{ext}"
            collision += 1

        used_names.add(new_name)

        caption_list = (
            item.get("image_caption")
            or item.get("table_caption")
            or item.get("chart_caption")
            or []
        )
        caption = caption_list[0].strip() if caption_list else ""

        rename_map[old_name] = (new_name, caption)

    return rename_map


def update_markdown(md_path: Path, rename_map: dict[str, RenameEntry], dry_run: bool) -> bool:
    if not md_path.exists():
        return False

    text = md_path.read_text(encoding="utf-8")
    updated = text

    for old, (new, caption) in rename_map.items():
        # Replace filename and inject caption into alt-text if present and alt-text is empty
        def make_replacement(m: re.Match) -> str:
            existing_alt = m.group(1)
            alt = existing_alt if existing_alt else caption
            return f"![{alt}](images/{new})"

        updated = re.sub(
            r"!\[([^\]]*)\]\(images/" + re.escape(old) + r"\)",
            make_replacement,
            updated,
        )

    if updated == text:
        return False

    if not dry_run:
        md_path.write_text(updated, encoding="utf-8")
    return True


def process_document(cl_path: Path, auto_dir: Path, dry_run: bool) -> None:
    img_dir = auto_dir / "images"
    if not img_dir.is_dir():
        print(f"  [SKIP] images/ not found: {auto_dir}")
        return

    with cl_path.open(encoding="utf-8") as f:
        items = json.load(f)

    rename_map = build_rename_map(items, img_dir)
    if not rename_map:
        print(f"  [SKIP] nothing to rename in {cl_path.name}")
        return

    stem = cl_path.name.replace("_content_list.json", "")
    md_path = auto_dir / f"{stem}.md"

    prefix = "[DRY] " if dry_run else ""
    print(f"\n  {auto_dir.name}")

    for old, (new, caption) in rename_map.items():
        cap_hint = f"  [{caption[:50]}]" if caption else ""
        print(f"    {prefix}{old[:40]:40s}  ->  {new}{cap_hint}")
        if not dry_run:
            shutil.move(str(img_dir / old), str(img_dir / new))

    md_changed = update_markdown(md_path, rename_map, dry_run)
    if md_changed:
        print(f"    {prefix}markdown updated: {md_path.name}")
    elif md_path.exists():
        print(f"    [INFO] no image refs found in markdown: {md_path.name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rename MinerU output images to content_type_N_pPage.ext"
    )
    parser.add_argument("output_root", help="Root output directory (processed recursively)")
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without renaming files"
    )
    args = parser.parse_args()

    root = Path(args.output_root)
    if not root.is_dir():
        sys.exit(f"Not a directory: {root}")

    docs = find_content_lists(root)
    if not docs:
        sys.exit("No _content_list.json files found under the given directory.")

    mode = "DRY RUN — no files will be changed" if args.dry_run else "renaming files"
    print(f"MinerU rename [{mode}]")
    print(f"Root: {root}")
    print(f"Documents found: {len(docs)}")

    for cl_path, auto_dir in docs:
        process_document(cl_path, auto_dir, args.dry_run)

    print("\nDone.")


if __name__ == "__main__":
    main()


# Example usage:
#   python 03_util_mineru_rename.py ./mineru_tests/ --dry-run
