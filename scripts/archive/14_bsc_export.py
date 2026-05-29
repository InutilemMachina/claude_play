"""
bsc_export.py -- BSc filter: strips MSc-only content from weekly outputs.

Usage:
    python scripts/bsc_export.py --het N --tantargy <tantargy_mappa>

Removes:
  - Markdown: <!-- MSc --> ... <!-- /MSc --> blocks
  - Mermaid: nodes with [MSc] prefix
  - Question bank: SZINT:4 and SZINT:5 questions
  - Marp: slides between <!-- MSc --> and <!-- /MSc -->

Output: <tantargy_mappa>/<N>_het/bsc/ directory with *_BSc.* files.
"""

import argparse
import os
import re
import shutil
from pathlib import Path


# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------

def strip_msc_blocks(text: str) -> str:
    """Remove <!-- MSc --> ... <!-- /MSc --> blocks (including Marp slide blocks)."""
    # Also handles Marp slide separator case: ---\n<!-- MSc -->\n...\n<!-- /MSc -->
    # Remove block with surrounding blank lines
    text = re.sub(
        r'\n*<!-- MSc -->\n.*?<!-- /MSc -->\n*',
        '\n',
        text,
        flags=re.DOTALL
    )
    return text


def strip_msc_mermaid_nodes(text: str) -> str:
    """Remove Mermaid nodes that contain [MSc] in their label."""
    # Matches lines like:    A --> A2[[MSc] MSc alfogalom]
    # or                     ROOT --> F[[MSc] MP Sorozat]
    lines = text.split('\n')
    out = []
    for line in lines:
        # Skip lines where node text contains [MSc]
        if re.search(r'\[+\[?MSc\]', line):
            continue
        # Also skip edge lines pointing to an MSc node id
        # (harder to detect without full graph parse -- skip for now)
        out.append(line)
    return '\n'.join(out)


def strip_msc_questions(text: str) -> str:
    """Remove SZINT:4 and SZINT:5 questions from question bank."""
    # Questions are separated by blank lines, start with **K[N]** SZINT:[2-5]
    blocks = re.split(r'(?=\*\*K\d+\*\*\s+SZINT:)', text)
    out = []
    for block in blocks:
        m = re.match(r'\*\*K\d+\*\*\s+SZINT:([2-5])', block)
        if m:
            level = int(m.group(1))
            if level >= 4:
                continue  # skip MSc questions
        out.append(block)
    return ''.join(out)


def renumber_questions(text: str) -> str:
    """Renumber K[N] after MSc questions removed."""
    counter = [0]
    def repl(m):
        counter[0] += 1
        return f'**K{counter[0]}**'
    return re.sub(r'\*\*K\d+\*\*', repl, text)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_file(src: Path, dst: Path, file_type: str):
    """Read src, apply BSc filters, write to dst."""
    with open(src, encoding='utf-8') as f:
        text = f.read()

    if file_type in ('notes', 'prezentacio', 'mindmap'):
        text = strip_msc_blocks(text)
        if file_type == 'mindmap':
            text = strip_msc_mermaid_nodes(text)

    if file_type == 'kerdesek':
        text = strip_msc_blocks(text)
        text = strip_msc_questions(text)
        text = renumber_questions(text)

    # Update title to indicate BSc version
    text = re.sub(
        r'^(# .+?)$',
        lambda m: m.group(1) + ' -- BSc',
        text,
        count=1,
        flags=re.MULTILINE
    )

    # Update YAML statusz
    text = re.sub(r'(statusz:\s*)\w+', r'\1DRAFT-BSc', text)

    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(text)

    orig_msc = text.count('<!-- MSc')
    print(f"  ✅ {dst.name}  ({len(text)} kar, {orig_msc} MSc blokk maradt: {orig_msc == 0})")


def main():
    parser = argparse.ArgumentParser(description='BSc export: strip MSc content')
    parser.add_argument('--het', required=True, help='Hét száma (pl. 1)')
    parser.add_argument('--tantargy', required=True, help='Tantárgy mappa elérési útja')
    args = parser.parse_args()

    n = args.het
    base = Path(args.tantargy) / f'{n}_het'
    bsc_dir = base / 'bsc'

    if not base.exists():
        print(f"Nem található: {base}")
        return

    file_map = {
        f'{n}_Jegyzet.md':      ('notes',       f'{n}_Jegyzet_BSc.md'),
        f'{n}_Mindmap.md':      ('mindmap',     f'{n}_Mindmap_BSc.md'),
        f'{n}_Prezentacio.md':  ('prezentacio', f'{n}_Prezentacio_BSc.md'),
        f'{n}_Kerdesek.md':     ('kerdesek',    f'{n}_Kerdesek_BSc.md'),
    }

    print(f"BSc export: {base} → {bsc_dir}")
    for src_name, (ftype, dst_name) in file_map.items():
        src = base / src_name
        if not src.exists():
            print(f"  ⚠️  Hiányzik: {src_name}")
            continue
        dst = bsc_dir / dst_name
        process_file(src, dst, ftype)

    print(f"\n✅ BSc export kész: {bsc_dir}")


if __name__ == '__main__':
    main()
