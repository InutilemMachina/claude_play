"""
05_assemble.py -- NLM Q1-Q4 outputs assembler

Reads nlm_q*.txt files from 3_raw_outputs/, resolves local citation numbers
to global IDs via citations_seed.json, and writes a draft N_Jegyzet.md.

Does NOT insert figures -- that is handled downstream by 09_figure_mapper.py
and 10_notes_collector.py.

Usage:
    python scripts/05_assemble.py --week-dir <path/to/N_het> [options]

    --week-dir   Path to the weekly folder (contains 1_raw_inputs/, 3_raw_outputs/,
                 4_wip_outputs/). Required.
    --queries    Space-separated query indices to assemble (default: 1 2 3 4).
    --q-order    Order in which queries appear in the output (default: 1 2 3 4).
    --title      Document title (default: read from citations_seed.json _meta.title).
    --week       Week number integer (default: read from citations_seed.json _meta.week).
    --subject    Subject name (default: read from citations_seed.json _meta.subject).
    --level      BSc or MSc (default: BSc).
    --output     Output file path (default: 4_wip_outputs/N_Jegyzet.md where N=week).
    --dry-run    Print to stdout instead of writing file.

Example:
    python scripts/05_assemble.py --week-dir test_outputs/Termografia_teszt_v3/1_het
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------------
# Load helpers
# ---------------------------------------------------------------------------

def load_nlm(path: Path) -> tuple[str, dict]:
    """Read a PowerShell Out-File JSON (UTF-8-sig, CRLF) and return (answer, citations)."""
    raw = path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    obj = json.loads(raw)
    val = obj.get("value", obj)
    answer   = val.get("answer", "")
    citations = val.get("citations", {})  # {local_int_str: uuid}
    return answer, citations


def load_seed(seed_path: Path) -> dict:
    """Load citations_seed.json, return the dict (including _meta entries)."""
    return json.loads(seed_path.read_bytes().decode("utf-8-sig"))


def build_uuid_to_global(seed: dict) -> dict:
    """Map nlm_uuid -> global citation id (int) from seed."""
    result = {}
    for k, v in seed.items():
        if k.startswith("_"):
            continue
        if isinstance(v, dict) and "nlm_uuid" in v:
            result[v["nlm_uuid"]] = int(k)
    return result


def replace_local_citations(text: str, local_map: dict) -> str:
    """Replace [1], [2, 3] etc. with global IDs using local_map {local_int: global_int}."""
    if not local_map:
        return text

    def repl(m):
        nums = [int(x.strip()) for x in m.group(1).split(",")]
        mapped = sorted(set(local_map.get(n, n) for n in nums))
        return "[" + ", ".join(str(x) for x in mapped) + "]"

    return re.sub(r"\[(\d+(?:,\s*\d+)*)\]", repl, text)


# ---------------------------------------------------------------------------
# Build reference list from seed
# ---------------------------------------------------------------------------

def build_reference_section(seed: dict) -> list[str]:
    """Build a ## Hivatkozásjegyzék section from seed numeric keys."""
    lines = ["## Hivatkozásjegyzék", ""]
    for k in sorted((k for k in seed if k.isdigit()), key=int):
        v = seed[k]
        author = v.get("author") or v.get("authors") or "?"
        title  = v.get("title", "?")
        year   = v.get("year", "?")
        fname  = v.get("filename") or v.get("file", "?")
        lines.append(
            f'[{k}] {author}. "{title}," {year}. Fájl: `{fname}`'
        )
    return lines


# ---------------------------------------------------------------------------
# Section title generator
# ---------------------------------------------------------------------------

def default_section_title(idx: int, q_idx: int) -> str:
    """Fallback section title when none provided."""
    return f"## {idx}. {idx}. szekció (Q{q_idx})"


# ---------------------------------------------------------------------------
# Main assembly
# ---------------------------------------------------------------------------

def assemble(week_dir: Path, args) -> str:
    """Assemble draft Jegyzet.md text and return as string."""
    raw_dir   = week_dir / "3_raw_outputs"
    seed_path = week_dir / "1_raw_inputs" / "citations_seed.json"

    if not seed_path.exists():
        sys.exit(f"citations_seed.json not found: {seed_path}")

    seed = load_seed(seed_path)
    meta = seed.get("_meta", {})

    # Resolve metadata
    week    = args.week    if args.week    else meta.get("week", 1)
    subject = args.subject if args.subject else meta.get("subject", "Tantargy")
    level   = args.level
    title   = args.title   if args.title   else meta.get("title", f"{week}. Hét")
    today   = date.today().isoformat()

    uuid_to_global = build_uuid_to_global(seed)

    # Load requested queries
    query_indices = args.queries  # list of int
    answers = {}
    for qi in query_indices:
        fname = raw_dir / f"nlm_q{qi}_raw.txt"
        if not fname.exists():
            print(f"  ⚠️  {fname.name} nem található -- kihagyva.", file=sys.stderr)
            continue
        answer, cits = load_nlm(fname)
        # Build local -> global map for this query
        local_map = {}
        for local_str, src_uuid in cits.items():
            g = uuid_to_global.get(src_uuid)
            if g:
                local_map[int(local_str)] = g
        answers[qi] = (replace_local_citations(answer, local_map), local_map)
        n_cit = len(cits)
        print(f"  Q{qi}: {len(answer)} char, {n_cit} citations")

    # Determine output order
    q_order = args.q_order  # list of int; may differ from query_indices for reordering

    # Build section titles: consecutive 1-based for the assembled output
    # (section numbers based on position in q_order, not Q-index)
    section_counter = 1
    section_titles = {}
    for qi in q_order:
        if qi == 1:
            # Q1 = intro, no numbered section -- keep as unnumbered preamble
            section_titles[qi] = None  # handled specially
        else:
            section_titles[qi] = f"## {section_counter}. {section_counter}. szekció (Q{qi})"
            section_counter += 1

    # YAML frontmatter
    frontmatter = (
        "---\n"
        f"title: {title}\n"
        f"subject: {subject}\n"
        f"week: {week}\n"
        f"level: {level}\n"
        f"updated: {today}\n"
        "---"
    )

    body = [frontmatter, "", f"# {title}", ""]

    # Intro (Q1) -- ## parent added so ### headings inside don't skip a level
    if 1 in answers and 1 in q_order:
        text, _ = answers[1]
        body.append("<!-- Q:1 -->")
        body.append("## 0. Bevezetés")
        body.append("")
        body.append(text)
        body.append("")

    # Content sections (Q2+)
    sec_num = 1
    for qi in q_order:
        if qi == 1:
            continue  # already handled
        if qi not in answers:
            continue
        text, _ = answers[qi]
        body.append(f"<!-- Q:{qi} -->")
        body.append(f"## {sec_num}. {sec_num}. szekció (Q{qi})")
        body.append("")
        body.append(text)
        body.append("")
        sec_num += 1

    # Reference list
    body.extend(build_reference_section(seed))

    return "\n".join(body)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="NLM Q1-Q4 → draft Jegyzet.md assembler")
    parser.add_argument("--week-dir", required=True, type=Path,
                        help="Heti mappa (tartalmazza 1_raw_inputs/, 3_raw_outputs/, 4_wip_outputs/)")
    parser.add_argument("--queries", nargs="+", type=int, default=[1, 2, 3, 4],
                        help="Beolvasandó query indexek (default: 1 2 3 4)")
    parser.add_argument("--q-order", nargs="+", type=int, default=None,
                        help="Kimenetbeli sorrend (default: --queries sorrendben)")
    parser.add_argument("--title",   default=None, help="Dokumentumcím (default: seed _meta)")
    parser.add_argument("--week",    default=None, type=int, help="Hét száma (default: seed _meta)")
    parser.add_argument("--subject", default=None, help="Tantárgy neve (default: seed _meta)")
    parser.add_argument("--level",   default="BSc", choices=["BSc", "MSc"],
                        help="BSc vagy MSc (default: BSc)")
    parser.add_argument("--output",  default=None, type=Path,
                        help="Kimeneti fájl (default: 4_wip_outputs/N_Jegyzet.md)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Kiírás stdout-ra fájl helyett")
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()
    if not week_dir.exists():
        sys.exit(f"Nem található: {week_dir}")

    if args.q_order is None:
        args.q_order = args.queries

    text = assemble(week_dir, args)

    if args.dry_run:
        print(text)
        return

    # Determine output path
    if args.output:
        out_path = args.output.resolve()
    else:
        # Read week number from seed for filename
        seed_path = week_dir / "1_raw_inputs" / "citations_seed.json"
        seed = json.loads(seed_path.read_bytes().decode("utf-8-sig"))
        week_num = args.week or seed.get("_meta", {}).get("week", 1)
        out_path = week_dir / "4_wip_outputs" / f"{week_num}_Jegyzet.md"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")