"""
generate_index.py -- Insert ToC and figures into N_Jegyzet.md (10_notes_collector)

Inserts a ## Tárgymutató block after the main # title heading,
and places figures from figure_catalog.json at the correct paragraph positions.

GFM anchor rules applied:
  - Lowercase
  - Remove: # ( ) . , ! ? : *
  - Spaces -> dashes
  - Hungarian accents preserved (é á ő ű etc.)
  - Duplicate headings get -1 -2 suffix

Usage:
    python scripts/generate_index.py --week-dir <path/to/N_het> [options]

    --week-dir      Path to weekly folder. Required.
    --week          Week number (default: read from citations_seed.json _meta.week).
    --no-figures    Skip figure insertion.
    --min-matches   Minimum match_score for figure insertion (default: 1).
    --dry-run       Print result to stdout, do not overwrite file.
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Anchor generation (GFM)
# ---------------------------------------------------------------------------

_ANCHOR_STRIP = re.compile(r'[#().,:!?*]')


def heading_to_anchor(text: str) -> str:
    """Convert a heading text to a GFM anchor slug."""
    text = _ANCHOR_STRIP.sub('', text)
    text = text.lower()
    text = re.sub(r'[ \t]+', '-', text.strip())
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


_ACCENT_MAP = str.maketrans('áéíóöőúüűÁÉÍÓÖŐÚÜŰ', 'aeiooouuuAEIOOOUUU')

# Headings excluded from ToC (accent-normalized, lowercase, no punctuation)
_EXCLUDE_HEADINGS = {
    'targymutat\xf3',  # tárgymutató (original)
    'targymutat o',
    'targymutat',
    'hivatkozasjegyzek',
    'hivatkozasjegyz\xe9k',
    'forrasjegyzek',
}
# simpler: just match normalized prefix
_EXCLUDE_PREFIXES = ('targymutat', 'hivatkozas', 'forrasjegyzek')


def build_toc(lines: list[str]) -> list[str]:
    """Build ToC lines from markdown heading lines.

    Excludes: # (level-1 title), ## Tárgymutató, ## Hivatkozásjegyzék.
    """
    anchor_counts: dict[str, int] = {}
    toc: list[str] = []

    for line in lines:
        m = re.match(r'^(#{2,4})\s+(.*)', line)
        if not m:
            continue
        level = len(m.group(1))  # 2, 3, or 4
        raw = m.group(2).strip()
        anchor_base = heading_to_anchor(raw)
        norm = re.sub(r'[^a-z]', '', raw.lower().translate(_ACCENT_MAP))
        if any(norm.startswith(p) for p in _EXCLUDE_PREFIXES):
            continue

        count = anchor_counts.get(anchor_base, 0)
        anchor = anchor_base if count == 0 else f'{anchor_base}-{count}'
        anchor_counts[anchor_base] = count + 1

        indent = '  ' * (level - 2)
        toc.append(f'{indent}- [{raw}](#{anchor})')

    return toc


# ---------------------------------------------------------------------------
# Figure insertion
# ---------------------------------------------------------------------------

def insert_figures(paragraphs: list[str], catalog_path: Path, min_matches: int) -> list[str]:
    """Insert figure blocks into paragraphs based on catalog inserted_after_paragraph."""
    if not catalog_path.exists():
        return paragraphs

    raw = json.loads(catalog_path.read_bytes().decode('utf-8-sig'))
    catalog = raw if isinstance(raw, dict) else {}

    # Gather (index, score, block) tuples
    inserts: dict[int, list[tuple[int, str]]] = {}
    for entry in catalog.values():
        idx = entry.get('inserted_after_paragraph')
        if idx is None:
            continue
        score = entry.get('match_score', 0)
        if score < min_matches:
            continue
        caption = entry.get('caption', '')
        path    = entry.get('path', '')
        if not path:
            continue
        block = f'\n![{caption}]({path})\n*{caption}*\n'
        inserts.setdefault(idx, []).append((score, block))

    if not inserts:
        return paragraphs

    result = list(paragraphs)
    for idx in sorted(inserts.keys(), reverse=True):
        if idx >= len(result):
            continue
        # Sort by score descending (highest score inserted first = appears closest after paragraph)
        for _, block in sorted(inserts[idx], key=lambda x: -x[0]):
            result[idx] = result[idx] + block

    return result


# ---------------------------------------------------------------------------
# ToC insertion
# ---------------------------------------------------------------------------

EXCLUDED_SECTIONS = {'tárgymutató', 'hivatkozásjegyzék', 'forrásjegyzék'}


def insert_toc(text: str, toc_lines: list[str]) -> str:
    """Insert ## Tárgymutató block after the first # heading line."""
    lines = text.splitlines()
    insert_after = -1
    for i, line in enumerate(lines):
        if re.match(r'^#\s', line):
            insert_after = i
            break

    if insert_after == -1:
        return text  # no title found, unchanged

    # Remove existing ## Tárgymutató block if present
    cleaned = []
    skip = False
    for i, line in enumerate(lines):
        if re.match(r'^##\s+Tárgymutató', line, re.IGNORECASE):
            skip = True
        elif skip and re.match(r'^#', line):
            skip = False
        if not skip:
            cleaned.append(line)
    lines = cleaned

    # Find insertion point again after cleaning
    insert_after = -1
    for i, line in enumerate(lines):
        if re.match(r'^#\s', line):
            insert_after = i
            break

    toc_block = ['', '## Tárgymutató', ''] + toc_lines + ['']
    result = lines[:insert_after + 1] + toc_block + lines[insert_after + 1:]
    return '\n'.join(result)


# ---------------------------------------------------------------------------
# Paragraph splitter (for figure insertion)
# ---------------------------------------------------------------------------

def split_paragraphs(text: str) -> list[str]:
    """Split text into paragraphs (double-newline separated)."""
    return re.split(r'\n\n', text)


def join_paragraphs(paragraphs: list[str]) -> str:
    return '\n\n'.join(paragraphs)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def resolve_week(week_dir: Path, week_arg) -> int:
    if week_arg:
        return int(week_arg)
    seed = week_dir / '1_raw_inputs' / 'citations_seed.json'
    if seed.exists():
        data = json.loads(seed.read_bytes().decode('utf-8-sig'))
        return data.get('_meta', {}).get('week', 1)
    return 1


def main():
    parser = argparse.ArgumentParser(description='ToC + figure inserter for N_Jegyzet.md')
    parser.add_argument('--week-dir', required=True, type=Path)
    parser.add_argument('--week', default=None, type=int)
    parser.add_argument('--no-figures', action='store_true',
                        help='Képbeillesztés kihagyása')
    parser.add_argument('--min-matches', type=int, default=1,
                        help='Minimum match_score a képekhez (default: 1)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Stdout-ra ír, fájlt nem ír felül')
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()
    if not week_dir.exists():
        sys.exit(f'Nem található: {week_dir}')

    week = resolve_week(week_dir, args.week)
    wip_dir     = week_dir / '4_wip_outputs'
    catalog_path = week_dir / '3_raw_outputs' / 'figure_catalog.json'
    notes_path  = wip_dir / f'{week}_Jegyzet.md'

    if not notes_path.exists():
        sys.exit(f'Nem található: {notes_path}')

    text = notes_path.read_bytes().decode('utf-8-sig').replace('\r\n', '\n')

    # Build ToC from heading lines
    toc_lines = build_toc(text.splitlines())
    print(f'  ToC: {len(toc_lines)} bejegyzés')

    # Insert ToC
    text = insert_toc(text, toc_lines)

    # Insert figures
    if not args.no_figures:
        paragraphs = split_paragraphs(text)
        paragraphs = insert_figures(paragraphs, catalog_path, args.min_matches)
        text = join_paragraphs(paragraphs)
        print(f'  Képek: figure_catalog feldolgozva')

    if args.dry_run:
        print(text)
        return

    notes_path.write_text(text, encoding='utf-8')
    print(f'  OK  {notes_path.name} frissítve')


if __name__ == '__main__':
    main()
