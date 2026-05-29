"""
06_excerpt_block_maker.py -- Szabály-alapú (extractive) összefoglaló blokkok.

Beszúr a 4_wip_outputs/N_Jegyzet.md-be:
  - 💡 Lényeg blokkot minden ### alszakasz VÉGÉRE (az alszakasz első érdemi
    prózai mondatának kivonataként)
  - 🗺️ Fejezet összegzés blokkot minden ## fejezet VÉGÉRE (a benne lévő
    ### alszakaszok címeiből összeállítva)

Mód:
  --mode extractive  (default) -- szabály-alapú, API nélkül; az első prózai
                     mondatot emeli ki. Nincs LLM, nincs kvóta.
  (jövőbeli: --mode abstractive -- Claude API, ha elérhető)

Idempotens: meglévő 💡/🗺️ blokkot nem duplikál.
A <!-- Q:N --> markereket, képeket, táblákat, blockquote-okat kihagyja.

Usage:
    python scripts/06_excerpt_block_maker.py --week-dir <path/to/N_het>
    python scripts/06_excerpt_block_maker.py --week-dir <path> --dry-run
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

try:
    from _encoding_fix import fix_stdout as _fix_stdout
    _fix_stdout()
except ImportError:
    pass


LENYEG_MARKER = "**💡 Lényeg:**"
OSSZEGZES_MARKER = "**🗺️ Fejezet összegzés"


# ---------------------------------------------------------------------------
# Sentence extraction
# ---------------------------------------------------------------------------

def is_prose_line(line: str) -> bool:
    """Return True if the line is body prose (not heading/list/table/image/etc.)."""
    s = line.strip()
    if not s:
        return False
    prefixes = ('#', '*', '-', '|', '>', '!', '<!--', '<sup', '$$', '```', '---')
    if s.startswith(prefixes):
        return False
    return True


def first_sentence(paragraph: str, max_chars: int = 240) -> str:
    """
    Extract the first sentence from a prose paragraph.
    Keeps <sup>[N]</sup> citations. Splits on '. ' boundary (not decimals).
    """
    # Protect decimals/abbreviations is overkill; split on '. ' followed by uppercase
    # or end. Simpler: find first '.' that is followed by space + capital, or EOL.
    text = paragraph.strip()
    # Remove trailing citation-only for boundary detection, but keep in output
    m = re.search(r'\.\s+(?=[A-ZÁÉÍÓÖŐÚÜŰ])', text)
    if m:
        sentence = text[: m.start() + 1]
    else:
        sentence = text
    sentence = sentence.strip()
    if len(sentence) > max_chars:
        # Truncate at last word boundary before max_chars
        cut = sentence[:max_chars].rsplit(' ', 1)[0]
        sentence = cut + " […]"
    return sentence


# ---------------------------------------------------------------------------
# Document parsing
# ---------------------------------------------------------------------------

def load_md(path: Path) -> str:
    return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def is_section_boundary(line: str) -> bool:
    """Heading or Q-marker = boundary that closes the current ### subsection body."""
    s = line.strip()
    return (s.startswith('## ') or s.startswith('### ')
            or s.startswith('# ') or s.startswith('<!--'))


def extract_first_prose(body_lines: list[str]) -> str | None:
    """Find the first prose paragraph in a block and return its first sentence."""
    for line in body_lines:
        if is_prose_line(line):
            return first_sentence(line)
    return None


# ---------------------------------------------------------------------------
# Core: insert blocks
# ---------------------------------------------------------------------------

def process(text: str) -> tuple[str, int, int]:
    """
    Returns (new_text, n_lenyeg, n_osszegzes).
    Walks the document, tracking ## chapters and ### subsections.
    """
    lines = text.splitlines()
    out: list[str] = []
    n_lenyeg = 0
    n_osszegzes = 0

    # State
    i = 0
    cur_chapter_title = None        # current ## title (stripped of number)
    chapter_sub_titles: list[str] = []  # ### titles within current chapter

    def flush_chapter_summary():
        """Append a 🗺️ summary for the chapter just ended (if it had subsections)."""
        nonlocal n_osszegzes
        if cur_chapter_title and chapter_sub_titles:
            # Avoid duplicate: check if last non-empty out lines already have summary
            tail = "\n".join(out[-6:])
            if OSSZEGZES_MARKER not in tail:
                if out and out[-1].strip() != "":
                    out.append("")
                subs = ", ".join(chapter_sub_titles)
                out.append(f"> {OSSZEGZES_MARKER} -- {cur_chapter_title}**")
                out.append(">")
                out.append(f"> Ez a fejezet a következő témákat tárgyalta: {subs}.")
                out.append("")
                n_osszegzes += 1

    while i < len(lines):
        line = lines[i]
        s = line.strip()

        # New ## chapter heading
        m_h2 = re.match(r'^##\s+(.+)$', s)
        m_h3 = re.match(r'^###\s+(.+)$', s)

        if m_h2 and not m_h3:
            # Close previous chapter with summary
            flush_chapter_summary()
            # Reset chapter state
            raw = m_h2.group(1).strip()
            # Skip ToC / references / intro chapters from summary logic
            clean = re.sub(r'^[\d.]+\s*', '', raw)
            low = clean.lower()
            if any(k in low for k in ('tartalomjegyz', 'hivatkoz', 'bevezet')):
                cur_chapter_title = None
                chapter_sub_titles = []
            else:
                cur_chapter_title = clean
                chapter_sub_titles = []
            out.append(line)
            i += 1
            continue

        if m_h3:
            # Record subsection title for chapter summary
            sub_title = re.sub(r'^[\d.]+\s*', '', m_h3.group(1).strip())
            chapter_sub_titles.append(sub_title)
            out.append(line)
            i += 1
            # Gather subsection body until next boundary
            body_start = len(out)
            body_lines = []
            while i < len(lines) and not is_section_boundary(lines[i]):
                body_lines.append(lines[i])
                out.append(lines[i])
                i += 1
            # Insert 💡 Lényeg at end of subsection body (if not already present)
            body_text = "\n".join(body_lines)
            if LENYEG_MARKER not in body_text:
                excerpt = extract_first_prose(body_lines)
                if excerpt:
                    # Trim trailing blank lines from out, then add block
                    while out and out[-1].strip() == "":
                        out.pop()
                    out.append("")
                    out.append(f"> {LENYEG_MARKER} {excerpt}")
                    out.append("")
                    n_lenyeg += 1
            continue

        out.append(line)
        i += 1

    # Flush summary for the last chapter
    flush_chapter_summary()

    return "\n".join(out), n_lenyeg, n_osszegzes


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def find_jegyzet(week_dir: Path) -> Path | None:
    wip = week_dir / "4_wip_outputs"
    cands = sorted(wip.glob("*_Jegyzet.md"))
    return cands[0] if cands else None


def main():
    parser = argparse.ArgumentParser(description="Szabály-alapú excerpt blokkok a Jegyzetbe")
    parser.add_argument("--week-dir", required=True, type=Path)
    parser.add_argument("--mode", choices=["extractive"], default="extractive",
                        help="extractive = szabály-alapú (default, API nélkül)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-backup", action="store_true")
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()
    jegyzet = find_jegyzet(week_dir)
    if not jegyzet or not jegyzet.exists():
        sys.exit(f"HIBA: nem található *_Jegyzet.md itt: {week_dir / '4_wip_outputs'}")

    text = load_md(jegyzet)
    new_text, n_l, n_o = process(text)
    print(f"  💡 Lényeg blokkok: {n_l}")
    print(f"  🗺️ Fejezet összegzések: {n_o}")

    if args.dry_run:
        print("[DRY RUN] -- fájl nem módosítva")
        return

    if not args.no_backup:
        shutil.copy2(str(jegyzet), str(jegyzet) + ".bak")
    jegyzet.write_text(new_text, encoding="utf-8")
    print(f"OK: {jegyzet} felülírva ({n_l + n_o} blokk)")


if __name__ == "__main__":
    main()
