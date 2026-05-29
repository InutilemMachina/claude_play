"""
10_notes_collector.py -- Table of Contents generator + figure inserter for N_Jegyzet.md

Two tasks in one pass:
  1. FIGURE INSERTION: reads figure_catalog.json (with inserted_after_paragraph set
     by 09_figure_mapper.py), inserts ![caption](path) blocks at the right positions.
     Skips entries where duplicate=True or inserted_after_paragraph is None.
  2. TOC GENERATION: scans headings and builds a Markdown ToC, inserts it after the
     YAML frontmatter (before the document title heading).

Figures are inserted with caption BELOW (standard image convention):
    ![caption](path)
    *N. ábra -- caption text* <sup>[[source]](#ref-source)</sup>

Tables already have captions ABOVE (injected by 06_table_caption_injector.py).

Usage:
    python scripts/10_notes_collector.py --week-dir <path/to/N_het> [options]

    --week-dir   Path to the weekly folder. Required.
    --notes      Path to N_Jegyzet.md (default: 4_wip_outputs/<week>_Jegyzet.md,
                 auto-detected from week number in YAML frontmatter).
    --catalog    Path to figure_catalog.json (default: 3_raw_outputs/figure_catalog.json).
    --no-figures Skip figure insertion (ToC only).
    --no-toc     Skip ToC generation (figures only).
    --dry-run    Print result to stdout, do not write file.
    --no-backup  Skip .bak creation.
"""

import argparse
import json
import re
import shutil
import sys as _sys
try:
    from _encoding_fix import fix_stdout as _fix_stdout
    _fix_stdout()
except ImportError:
    pass
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_yaml_week(text):
    """Read 'week: N' from YAML frontmatter. Returns int or None."""
    m = re.search(r'^week:\s*(\d+)', text, re.MULTILINE)
    return int(m.group(1)) if m else None


def find_notes_file(week_dir, text_hint=None):
    """Auto-detect N_Jegyzet.md in 4_wip_outputs/."""
    wip = week_dir / "4_wip_outputs"
    if text_hint:
        week = extract_yaml_week(text_hint)
        if week:
            candidate = wip / f"{week}_Jegyzet.md"
            if candidate.exists():
                return candidate
    # Fallback: first *_Jegyzet.md found
    candidates = sorted(wip.glob("*_Jegyzet.md"))
    return candidates[0] if candidates else None


# ---------------------------------------------------------------------------
# 1. Figure insertion
# ---------------------------------------------------------------------------

def extract_paragraphs_with_positions(text):
    """
    Return list of (start_line_idx, end_line_idx) for each matchable paragraph.
    A paragraph is a contiguous block of non-empty, non-heading, non-image lines.
    Matches the definition used in 09_figure_mapper.py.
    """
    lines = text.splitlines()
    paragraphs = []  # (start, end) line indices (inclusive)
    i = 0
    para_start = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        is_content = (
            stripped
            and not stripped.startswith('#')
            and not stripped.startswith('![')
            and not stripped.startswith('<!--')
            and not stripped.startswith('>')
            and not stripped.startswith('|')
        )
        if is_content:
            if para_start is None:
                para_start = i
        else:
            if para_start is not None:
                paragraphs.append((para_start, i - 1))
                para_start = None

    if para_start is not None:
        paragraphs.append((para_start, len(lines) - 1))

    return paragraphs


def build_figure_block(entry, fig_num, week_dir):
    """
    Build the Markdown block to insert for one figure.
    Path is made relative to the Markdown file's folder (4_wip_outputs/).
    """
    path_str = entry.get("path", "")
    caption  = entry.get("caption", "").strip()
    if not caption:
        caption = f"ábra {fig_num}"

    # Make path relative from 4_wip_outputs/ -> needs ../ prefix since
    # catalog paths are relative to week_dir (e.g. 2_clean_inputs/src/auto/images/...)
    rel_path = "../" + path_str  # 4_wip_outputs/ is one level below week_dir

    lines = [
        "",
        f"![{caption}]({rel_path})",
        f"*{fig_num}. ábra -- {caption}*",
        "",
    ]
    return "\n".join(lines)


def insert_figures(text, catalog, week_dir):
    """
    Insert figure blocks after the appropriate paragraphs.
    Returns new text.
    """
    lines = text.splitlines(keepends=False)
    para_positions = extract_paragraphs_with_positions(text)

    # Collect insertions: {after_line_idx: [figure_block_str, ...]}
    from collections import defaultdict
    insertions = defaultdict(list)

    fig_num = 0
    for entry in catalog.values() if isinstance(catalog, dict) else catalog:
        if entry.get("duplicate"):
            continue
        para_idx = entry.get("inserted_after_paragraph")
        if para_idx is None:
            continue
        if para_idx >= len(para_positions):
            continue

        fig_num += 1
        _, end_line = para_positions[para_idx]
        block = build_figure_block(entry, fig_num, week_dir)
        insertions[end_line].append(block)

    if not insertions:
        return text, 0

    # Rebuild with insertions
    result = []
    for i, line in enumerate(lines):
        result.append(line)
        if i in insertions:
            for block in insertions[i]:
                result.extend(block.splitlines())

    return "\n".join(result), fig_num


# ---------------------------------------------------------------------------
# 2. ToC generation
# ---------------------------------------------------------------------------

def heading_to_anchor(text):
    """GitHub-style anchor: lowercase, spaces->hyphen, strip special chars."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'\s+', '-', text.strip())
    return text


def build_toc(text):
    """
    Build a Markdown ToC from headings (skipping the document title = first #).
    Returns ToC string.
    """
    lines = text.splitlines()
    in_yaml = False
    yaml_done = False
    in_code = False
    title_seen = False
    toc_lines = ["## Tartalomjegyzék", ""]

    for line in lines:
        s = line.rstrip()
        if not yaml_done and s == '---':
            if not in_yaml and not title_seen:
                in_yaml = True; continue
            elif in_yaml:
                in_yaml = False; yaml_done = True; continue
        if in_yaml: continue
        if s.startswith('```') or s.startswith('~~~'):
            in_code = not in_code; continue
        if in_code: continue

        m = re.match(r'^(#{1,6})\s+(.+?)$', s)
        if not m: continue
        depth = len(m.group(1))
        heading_text = m.group(2).strip()

        # Skip document title
        if not title_seen and depth == 1:
            title_seen = True
            continue

        # Skip ToC heading itself (avoid self-referencing)
        if re.match(r'tartalomjegyzék', heading_text, re.IGNORECASE):
            continue

        anchor = heading_to_anchor(re.sub(r'^[\d.]+\s+', '', heading_text))
        indent = "  " * (depth - 2) if depth > 1 else ""
        toc_lines.append(f"{indent}- [{heading_text}](#{anchor})")

    toc_lines.append("")
    return "\n".join(toc_lines)


def insert_toc(text, toc):
    """
    Insert ToC after YAML frontmatter and document title heading.
    Position: after the first # heading line.
    """
    lines = text.splitlines(keepends=False)
    in_yaml = False
    yaml_done = False
    title_inserted = False
    result = []

    for line in lines:
        result.append(line)
        s = line.rstrip()
        if not yaml_done:
            if s == '---':
                if not in_yaml:
                    in_yaml = True
                else:
                    in_yaml = False; yaml_done = True
            continue
        if in_yaml: continue

        # After first # heading = document title
        if not title_inserted and re.match(r'^# ', s):
            result.append("")
            result.extend(toc.splitlines())
            title_inserted = True

    return "\n".join(result)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="ToC generator + figure inserter for N_Jegyzet.md"
    )
    parser.add_argument("--week-dir", required=True, type=Path,
                        help="Heti mappa (tartalmazza 4_wip_outputs/, 3_raw_outputs/)")
    parser.add_argument("--notes", default=None, type=Path,
                        help="N_Jegyzet.md elérési útja (auto-detect ha nem adott)")
    parser.add_argument("--catalog", default=None, type=Path,
                        help="figure_catalog.json (default: 3_raw_outputs/figure_catalog.json)")
    parser.add_argument("--no-figures", action="store_true", help="Ábrák beillesztése kihagyva")
    parser.add_argument("--no-toc",     action="store_true", help="ToC generálás kihagyva")
    parser.add_argument("--dry-run",    action="store_true", help="stdout, fájl érintetlen")
    parser.add_argument("--no-backup",  action="store_true", help=".bak nem készül")
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()

    # Locate Markdown file
    if args.notes:
        notes_path = args.notes.resolve()
    else:
        notes_path = find_notes_file(week_dir)
        if notes_path is None:
            sys.exit(f"Nem található *_Jegyzet.md a 4_wip_outputs/ mappában: {week_dir}")

    if not notes_path.exists():
        sys.exit(f"Nem található: {notes_path}")

    text = notes_path.read_text(encoding="utf-8")
    print(f"Betöltve: {notes_path.name} ({len(text.splitlines())} sor)")

    # Figure insertion
    n_figs = 0
    if not args.no_figures:
        catalog_path = (
            args.catalog or week_dir / "3_raw_outputs" / "figure_catalog.json"
        ).resolve()
        if not catalog_path.exists():
            print(f"  WARN  figure_catalog.json nem található -- ábrák kihagyva: {catalog_path}",
                  file=sys.stderr)
        else:
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            text, n_figs = insert_figures(text, catalog, week_dir)
            print(f"Ábra beillesztve: {n_figs}")

    # ToC generation
    if not args.no_toc:
        toc = build_toc(text)
        text = insert_toc(text, toc)
        toc_entries = toc.count('\n- ') + toc.count('\n  - ')
        print(f"ToC generálva: {toc_entries} bejegyzés")

    if args.dry_run:
        print(text)
        return

    if not args.no_backup:
        bak = notes_path.with_suffix(notes_path.suffix + ".bak")
        shutil.copy2(notes_path, bak)

    notes_path.write_text(text, encoding="utf-8")
    print(f"OK Mentve: {notes_path}")


if __name__ == "__main__":
    main()
