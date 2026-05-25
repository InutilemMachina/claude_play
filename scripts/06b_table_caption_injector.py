"""
06b_table_caption_injector.py -- Inject captions ABOVE Markdown tables.

Academic convention: caption goes ABOVE the table.
Format inserted:
    *N. táblázat -- [source caption or auto-generated text]*

The script:
  1. Scans N_Jegyzet.md for GFM tables (lines starting with |).
  2. Checks if the line immediately above is already a caption
     (italic line matching the pattern "*N. táblázat*").
  3. If not, inserts an auto-numbered caption above the table.
  4. Writes the result back in-place (backs up original as .bak).

Existing captions (from figure_catalog or manual) are preserved unchanged.
Only tables WITHOUT a caption get one injected.

Usage:
    python scripts/06b_table_caption_injector.py <N_Jegyzet.md> [options]

    --prefix     Caption prefix word (default: "táblázat")
    --dry-run    Print result to stdout, do not modify file.
    --no-backup  Skip .bak file creation.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Table detection
# ---------------------------------------------------------------------------

def is_table_line(line):
    """True if the line is part of a GFM table (starts with |)."""
    return line.lstrip().startswith('|')


def is_separator_row(line):
    """True if the line is a GFM table separator row (|----|)."""
    return bool(re.match(r'^\s*\|[-: |]+\|\s*$', line))


def is_caption_line(line, prefix):
    """
    True if the line looks like an existing table caption.
    Matches: *N. táblázat ...* or **N. táblázat ...**
    """
    pat = rf'^\s*\*{{1,2}}\d+\.\s+{re.escape(prefix)}.*\*{{1,2}}\s*$'
    return bool(re.match(pat, line, re.IGNORECASE))


def is_blank(line):
    return line.strip() == ''


# ---------------------------------------------------------------------------
# Core injection
# ---------------------------------------------------------------------------

def inject_captions(text, prefix='táblázat'):
    """
    Scan text for tables without captions and inject numbered captions above.
    Returns (new_text, n_injected).
    """
    lines = text.splitlines(keepends=True)
    result = []
    table_num = 0
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detect start of a table block (first | line that is NOT a separator)
        if is_table_line(line) and not is_separator_row(line):
            # Check what's above: skip blank lines to find nearest non-blank
            prev_non_blank = None
            for j in range(len(result) - 1, -1, -1):
                if not is_blank(result[j]):
                    prev_non_blank = result[j]
                    break

            # Only inject if previous non-blank is NOT already a caption
            if prev_non_blank is None or not is_caption_line(prev_non_blank, prefix):
                table_num += 1
                caption = f"*{table_num}. {prefix} -- (automatikus felirat)*\n"
                # Insert blank line before caption if needed
                if result and not is_blank(result[-1]):
                    result.append('\n')
                result.append(caption)

            # Consume the entire table block
            while i < len(lines) and (is_table_line(lines[i]) or is_separator_row(lines[i])):
                result.append(lines[i])
                i += 1
            continue

        result.append(line)
        i += 1

    return ''.join(result), table_num


def count_existing_captions(text, prefix):
    """Count caption lines already present (to set starting table_num correctly)."""
    count = 0
    pat = rf'^\s*\*{{1,2}}\d+\.\s+{re.escape(prefix)}.*\*{{1,2}}\s*$'
    for line in text.splitlines():
        if re.match(pat, line, re.IGNORECASE):
            count += 1
    return count


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Inject captions above Markdown tables (academic style)"
    )
    parser.add_argument("input", type=Path, help="Input Markdown fájl")
    parser.add_argument("--prefix", default="táblázat",
                        help="Caption prefix (default: 'táblázat')")
    parser.add_argument("--dry-run", action="store_true",
                        help="Eredmény stdout-ra, fájl érintetlen")
    parser.add_argument("--no-backup", action="store_true",
                        help=".bak fájl nem készül")
    args = parser.parse_args()

    path = args.input.resolve()
    if not path.exists():
        sys.exit(f"Nem található: {path}")

    text = path.read_text(encoding="utf-8")
    new_text, n_injected = inject_captions(text, args.prefix)

    if args.dry_run:
        print(new_text)
        print(f"\n--- {n_injected} caption injektálva (dry-run) ---", file=sys.stderr)
        return

    if n_injected == 0:
        print(f"OK Nincs injektálandó caption -- fájl érintetlen: {path.name}")
        return

    if not args.no_backup:
        bak = path.with_suffix(path.suffix + '.bak')
        shutil.copy2(path, bak)

    path.write_text(new_text, encoding="utf-8")
    print(f"OK {n_injected} caption injektálva: {path.name}")


if __name__ == "__main__":
    main()
