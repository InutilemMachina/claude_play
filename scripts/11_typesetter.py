"""
11_typesetter.py -- Two-phase Markdown typesetter for NLM pipeline.

Phase 1: Bullet-to-prose conversion via Claude API (claude-sonnet-4-6).
Phase 2: Whitespace/formatting linting (rules A, C, D, E, F from skill).

Usage:
    python 11_typesetter.py <path_to_N_Jegyzet.md>

Requirements:
    pip install anthropic
    ANTHROPIC_API_KEY environment variable must be set.
"""

import re
import sys
import os
import anthropic
from pathlib import Path


# ---- Configuration ----

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096

# Minimum number of bullet lines in a block to trigger API conversion.
# Single-line "lists" (e.g. standalone "* Note:") are left as-is.
MIN_BULLET_LINES = 2


# ---- File I/O ----

def load_md(path: Path) -> str:
    """Read Markdown, handling BOM and CRLF (PowerShell Out-File artifacts)."""
    return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def save_md(path: Path, text: str):
    """Write Markdown as UTF-8 without BOM."""
    path.write_text(text, encoding="utf-8")


# ---- Block parser ----

def is_bullet_line(line: str) -> bool:
    """Return True if line is a bullet or numbered list item (any indent level)."""
    stripped = line.lstrip()
    return (
        re.match(r"^\*\s+", stripped) is not None or
        re.match(r"^-\s+", stripped) is not None or
        re.match(r"^\d+\.\s+", stripped) is not None
    )


def is_preserved_line(line: str) -> bool:
    """Lines that must never be sent to the API or modified by linting."""
    stripped = line.strip()
    return (
        stripped.startswith("#") or      # Markdown headers
        stripped.startswith("![") or     # Image references
        stripped.startswith("<!--") or   # HTML comments (Q:N markers)
        stripped.startswith(">") or      # Blockquotes
        stripped.startswith("---") or    # HR / YAML delimiter
        stripped == ""                   # Empty lines
    )


def split_into_blocks(text: str):
    """
    Split text into blocks of (type, lines).
    Types: 'preserve' | 'bullets' | 'prose'

    YAML front matter (--- ... ---) is always a single 'preserve' block.
    """
    lines = text.split("\n")
    blocks = []
    i = 0

    # Extract YAML front matter as one preserve block
    if lines and lines[0].strip() == "---":
        j = 1
        while j < len(lines) and lines[j].strip() != "---":
            j += 1
        blocks.append(("preserve", lines[: j + 1]))
        i = j + 1

    current_type = None
    current_lines = []

    while i < len(lines):
        line = lines[i]

        if is_preserved_line(line):
            ltype = "preserve"
        elif is_bullet_line(line):
            ltype = "bullets"
        else:
            ltype = "prose"

        if ltype == current_type:
            current_lines.append(line)
        else:
            if current_type is not None:
                blocks.append((current_type, current_lines))
            current_type = ltype
            current_lines = [line]
        i += 1

    if current_lines:
        blocks.append((current_type, current_lines))

    return blocks


# ---- Phase 1: Prose conversion ----

PROSE_PROMPT = """\
A következő szöveg egy magyar nyelvű műszaki/tudományos tananyag egy szekciójából való bullet-point lista.
Alakítsd összefüggő, folyamatos magyar prózává egyetlen bekezdésbe vagy logikusan tagolt bekezdésekbe.

Kötelező szabályok:
1. A tartalom VÁLTOZATLAN marad -- csak a formátumot alakítjuk prózává.
2. Megőrizendő elemek: <sup>...</sup> hivatkozások, LaTeX képletek ($...$),
   **félkövér** és *dőlt* formázás, számok és egységek.
3. Magyar tudományos/oktató regiszter, tömör mondatok.
4. Ne adj hozzá új tartalmat, ne hagyj el semmit.
5. Visszaadandó: CSAK a konvertált próza szöveg -- semmi magyarázat, komment.

Bullet lista:
{bullet_text}"""


def convert_bullets_to_prose(bullet_text: str, client: anthropic.Anthropic) -> str:
    """Call Claude API to convert a bullet block to flowing prose."""
    prompt = PROSE_PROMPT.format(bullet_text=bullet_text)
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def phase1_prose_conversion(text: str, client: anthropic.Anthropic) -> str:
    """
    Walk through all blocks; convert 'bullets' blocks (>= MIN_BULLET_LINES) to prose.
    Preserve everything else exactly.
    """
    blocks = split_into_blocks(text)
    result_parts = []
    converted = 0
    skipped = 0

    for btype, lines in blocks:
        block_text = "\n".join(lines)

        if btype == "bullets" and len(lines) >= MIN_BULLET_LINES:
            print(
                f"  [Phase 1] Converting bullet block "
                f"({len(lines)} lines, {len(block_text)} chars)..."
            )
            prose = convert_bullets_to_prose(block_text, client)
            result_parts.append(prose)
            converted += 1
        else:
            if btype == "bullets":
                skipped += 1  # too short; left as-is
            result_parts.append(block_text)

    print(
        f"[Phase 1] Done: {converted} block(s) converted, "
        f"{skipped} short block(s) left as-is."
    )
    return "\n".join(result_parts)


# ---- Phase 2: Linting ----

def rule_a_sup_paragraph_break(text: str) -> tuple[str, int]:
    """
    Rule A: Insert blank line after </sup>. before new sentence starting with
    a capital (Hungarian) letter.
    """
    pattern = re.compile(r"(</sup>\.)([ \t]*)([A-ZÁÉÍÓÖŐÚÜŰ])")
    count = len(pattern.findall(text))
    text = pattern.sub(r"\1\n\n\3", text)
    return text, count


def rule_c_image_spacing(text: str) -> tuple[str, int]:
    """Rule C: Ensure a blank line before every ![ image reference."""
    pattern = re.compile(r"([^\n])\n(!\[)")
    count = len(pattern.findall(text))
    text = pattern.sub(r"\1\n\n\2", text)
    return text, count


def rule_d_blockquote_spacing(text: str) -> tuple[str, int]:
    """Rule D: Ensure a blank line before every > blockquote line."""
    pattern = re.compile(r"([^\n>])\n(> )")
    count = len(pattern.findall(text))
    text = pattern.sub(r"\1\n\n\2", text)
    return text, count


def rule_e_hr_dedup(text: str) -> tuple[str, int]:
    """Rule E: Collapse consecutive --- separators into one."""
    pattern = re.compile(r"---\n+---")
    count = len(pattern.findall(text))
    text = pattern.sub("---", text)
    return text, count


def rule_f_latex_check(text: str) -> list[str]:
    """
    Rule F: Check for unpaired LaTeX delimiters.
    Returns a list of warning strings (empty = OK).
    Does NOT modify text.
    """
    warnings = []
    # Inline $: match $ not preceded or followed by another $
    singles = re.findall(r"(?<!\$)\$(?!\$)", text)
    if len(singles) % 2 != 0:
        warnings.append(f"Unpaired inline $ (count={len(singles)})")
    # Display $$
    doubles = re.findall(r"\$\$", text)
    if len(doubles) % 2 != 0:
        warnings.append(f"Unpaired display $$ (count={len(doubles)})")
    return warnings


def phase2_linting(text: str) -> str:
    """Apply rules A, C, D, E, F. Rule G (heading numbering) uses a separate util."""
    print("[Phase 2] Linting...")

    text, n_a = rule_a_sup_paragraph_break(text)
    print(f"  Rule A (sup paragraph breaks): {n_a} fix(es)")

    text, n_c = rule_c_image_spacing(text)
    print(f"  Rule C (image blank lines):    {n_c} fix(es)")

    text, n_d = rule_d_blockquote_spacing(text)
    print(f"  Rule D (blockquote spacing):   {n_d} fix(es)")

    text, n_e = rule_e_hr_dedup(text)
    print(f"  Rule E (HR dedup):             {n_e} fix(es)")

    warnings_f = rule_f_latex_check(text)
    if warnings_f:
        print("  Rule F (LaTeX) WARNINGS:")
        for w in warnings_f:
            print(f"    - {w}")
    else:
        print("  Rule F (LaTeX):                OK")

    print("[Phase 2] Done.")
    return text


# ---- Main ----

def main():
    if len(sys.argv) < 2:
        print("Usage: python 11_typesetter.py <path_to_N_Jegyzet.md>")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"ERROR: File not found: {md_path}")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)

    print(f"[11_typesetter] Input: {md_path}")
    text = load_md(md_path)
    original_len = len(text)

    # Phase 1: Prose conversion (Claude API)
    client = anthropic.Anthropic(api_key=api_key)
    text = phase1_prose_conversion(text, client)

    # Phase 2: Whitespace linting
    text = phase2_linting(text)

    # Write back in-place
    save_md(md_path, text)
    print(
        f"[11_typesetter] Written back: {md_path} "
        f"({original_len} -> {len(text)} chars)"
    )
    print("[11_typesetter] NOTE: Run util_heading_numberer.py for Rule G (heading numbering).")


if __name__ == "__main__":
    main()
