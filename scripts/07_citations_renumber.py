"""
07_citations_renumber.py -- Post-assembly citation cleanup for Jegyzet.md

What this script does (new pipeline, 2026-05-29):
  1. Convert plain [N] -> <sup>[N]</sup> in body text
  2. Remove inline "Felhasznált/Hivatkozott forrás(ok):" blocks (NLM artifacts)
  3. Deduplicate consecutive identical citations [N], [N] -> [N]

Pre-condition: 05_assemble.py already mapped local->global citation numbers
using citations_seed.json. This script only does formatting cleanup.

Usage:
    python scripts/07_citations_renumber.py --week-dir test_outputs/mini/1_het
    python scripts/07_citations_renumber.py --week-dir test_outputs/mini/1_het --dry-run
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

from _citations_util import load_seed


def convert_plain_citations(text: str) -> tuple[str, int]:
    """Convert [N] and [N, M] plain brackets -> <sup>[N]</sup> etc.
    Skips citations already wrapped in <sup>...</sup>.
    """
    count = 0

    def repl(m):
        nonlocal count
        # Already wrapped? leave as-is (handled by negative lookbehind below)
        count += 1
        return f"<sup>{m.group(0)}</sup>"

    # Match [N] or [N, M, ...] NOT already inside <sup>
    # Negative lookbehind for <sup> and negative lookahead for </sup>
    pattern = r'(?<!<sup>)(\[\d+(?:,\s*\d+)*\])(?!</sup>)'
    new_text = re.sub(pattern, repl, text)
    return new_text, count


def remove_inline_source_blocks(text: str) -> tuple[str, int]:
    """Remove NLM-generated inline source blocks.
    Patterns removed:
      - Lines starting with 'Felhasznált források:' or 'Hivatkozott források:' etc.
      - Following bullet lines that are part of that block (lines starting with * or -)
    """
    count = 0
    lines = text.splitlines()
    result = []
    skip_bullets = False

    SOURCE_BLOCK = re.compile(
        r'^\s*(Felhaszn[aá]lt|Hivatkozott|Felhasznalt|Hivatkozott)\s+forr[aá]s(ok)?[:\.]?\s*$',
        re.IGNORECASE
    )

    for line in lines:
        if SOURCE_BLOCK.match(line):
            count += 1
            skip_bullets = True
            continue  # skip the header line
        if skip_bullets:
            # Skip following bullet/star lines (inline source list)
            if re.match(r'^\s*[*\-]\s+', line) or re.match(r'^\s*\d+\.\s+', line):
                count += 1
                continue
            else:
                skip_bullets = False

        result.append(line)

    return '\n'.join(result), count


def dedup_citations(text: str) -> tuple[str, int]:
    """Remove consecutive duplicate citations: [N], [N] -> [N]."""
    count = 0

    def repl(m):
        nonlocal count
        count += 1
        return m.group(1)  # keep first occurrence only

    # Match [N] followed by one or more ,[N] (same N)
    # e.g. [2], [2] -> [2]
    new_text = re.sub(r'(<sup>\[(\d+)\]</sup>)(?:,\s*<sup>\[\2\]</sup>)+', r'\1', text)
    if new_text != text:
        # Count how many were removed
        new_text2 = re.sub(
            r'(<sup>\[(\d+)\]</sup>)(?:,\s*<sup>\[\2\]</sup>)+',
            lambda m: m.group(1),
            text
        )
        count = text.count('<sup>') - new_text.count('<sup>')
    return new_text, count


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Citation cleanup for assembled Jegyzet.md")
    parser.add_argument("--week-dir", required=True, type=Path,
                        help="Heti mappa (pl. test_outputs/mini/1_het)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Csak statisztikát ír, nem módosít")
    parser.add_argument("--no-sup", action="store_true",
                        help="Ne konvertálja [N]-t <sup>[N]</sup>-re")
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()
    seed_path = week_dir / "1_raw_inputs" / "citations_seed.json"
    wip_dir = week_dir / "4_wip_outputs"

    if not seed_path.exists():
        sys.exit(f"HIBA: {seed_path} nem található")

    seed = load_seed(seed_path)
    week_num = seed.get("_meta", {}).get("week", 1)
    jegyzet_path = wip_dir / f"{week_num}_Jegyzet.md"

    if not jegyzet_path.exists():
        sys.exit(f"HIBA: {jegyzet_path} nem található")

    text = jegyzet_path.read_text(encoding="utf-8")

    # Step 1: Remove inline source blocks
    text, n_blocks = remove_inline_source_blocks(text)
    print(f"  Forrásblokk eltávolítva: {n_blocks} sor")

    # Step 2: Deduplicate consecutive plain [N],[N]
    text_dedup = re.sub(r'\[(\d+)\](?:,\s*\[\1\])+', r'[\1]', text)
    n_dedup = text.count('[') - text_dedup.count('[') if text != text_dedup else 0
    text = text_dedup
    print(f"  Dupla citáció dedup: {n_dedup} eltávolítva")

    # Step 3: Convert [N] -> <sup>[N]</sup>
    if not args.no_sup:
        text, n_sup = convert_plain_citations(text)
        print(f"  [N] -> <sup>[N]</sup>: {n_sup} konvertálva")
    else:
        n_sup = 0

    # Step 4: Deduplicate <sup>[N]</sup>,<sup>[N]</sup>
    text, n_sup_dedup = dedup_citations(text)
    print(f"  <sup> dupla dedup: {n_sup_dedup} eltávolítva")

    print(f"  Összesen: {n_blocks + n_dedup + n_sup + n_sup_dedup} változás")

    if args.dry_run:
        print("[DRY RUN] -- fájl nem módosítva")
        return

    bak = str(jegyzet_path) + ".bak"
    shutil.copy2(str(jegyzet_path), bak)
    jegyzet_path.write_text(text, encoding="utf-8")
    print(f"OK: {jegyzet_path} felülírva (backup: {bak})")


if __name__ == "__main__":
    main()
