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
try:
    from _encoding_fix import fix_stdout as _fix_stdout
    _fix_stdout()
except ImportError:
    pass


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
    """Build a ## Hivatkozásjegyzék section from seed numeric keys (numbered list)."""
    lines = ["## Hivatkozásjegyzék", ""]
    for k in sorted((k for k in seed if k.isdigit()), key=int):
        v = seed[k]
        author = v.get("author") or v.get("authors") or "?"
        title  = v.get("title", "?")
        year   = v.get("year", "?")
        fname  = v.get("filename") or v.get("file")
        url    = v.get("url")
        loc = f"[{fname}]({url})" if (fname and url) else \
              (fname or (url and f"<{url}>") or "?")
        lines.append(f"{k}. {author}. *{title}* ({year}). {loc}")
        lines.append("")  # blank line between entries for readability
    return lines


# ---------------------------------------------------------------------------
# Section title extractor (D6: assembler does NOT number -- heading_numberer
# is the sole source of section numbering)
# ---------------------------------------------------------------------------

def extract_section_title(answer_text: str) -> tuple:
    """
    Extract the first ## or ### heading from the NLM answer as the section title.

    Priority: ## heading preferred; ### accepted if no ## found.
    If the heading is the very first non-empty line, strip it from the body
    to avoid duplication (the heading becomes the ## wrapper, not also content).
    Returns (title_or_None, body_text).

    Note: NLM CLI typically generates ### as its first heading (not ##).
    Both are promoted to ## level in the output.
    """
    lines = answer_text.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        m = re.match(r'^#{2,3}\s+(.+)$', stripped)
        if m:
            # Strip any leading dotted number the NLM may have added (e.g. "1. Topic")
            raw_title = re.sub(r'^[\d.]+\s+', '', m.group(1).strip())
            if i <= 1:
                # First non-empty line IS a heading -- use as wrapper, strip from body
                remaining = '\n'.join(lines[i + 1:]).lstrip('\n')
                return raw_title, remaining
            else:
                # Heading appears mid-text -- use as title but keep in body (no duplication)
                return raw_title, answer_text
        else:
            # First non-empty line is prose, not a heading
            break
    return None, answer_text


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
    title   = args.title   if args.title   else meta.get("title", f"{week}. Het")
    today   = date.today().isoformat()

    # Fallback: try to read title from nlm_mindmap_export.md H1 if not resolved
    if title == f"{week}. Het":
        mindmap_path = week_dir / "3_raw_outputs" / "nlm_mindmap_export.md"
        if mindmap_path.exists():
            for line in mindmap_path.read_text(encoding="utf-8").splitlines():
                m = re.match(r'^#\s+(.+)$', line.strip())
                if m:
                    title = m.group(1).strip()
                    break

    uuid_to_global = build_uuid_to_global(seed)

    # Load dfs_node_list.json for L1-based sectioning (written by 04_nlm_dfs_queries.py)
    # Maps query index (str) -> {name, level, parent}
    node_list: dict = {}
    node_list_path = raw_dir / "dfs_node_list.json"
    if node_list_path.exists():
        node_list = json.loads(node_list_path.read_bytes().decode("utf-8-sig"))
        print(f"  dfs_node_list.json betöltve: {len(node_list)} bejegyzés", file=sys.stderr)
    else:
        print(f"  WARN  dfs_node_list.json nem található -- L1-szekcionálás kihagyva.", file=sys.stderr)

    # Load requested queries
    query_indices = args.queries  # list of int
    answers = {}
    for qi in query_indices:
        fname = raw_dir / f"nlm_q{qi}_raw.txt"
        if not fname.exists():
            print(f"  WARN  {fname.name} nem talalhato -- kihagyva.", file=sys.stderr)
            continue
        answer, cits = load_nlm(fname)
        # Build local -> global map for this query
        local_map = {}
        for local_str, src_uuid in cits.items():
            g = uuid_to_global.get(src_uuid)
            if g:
                local_map[int(local_str)] = g
        # Deduplicate consecutive identical citations: [2], [2] -> [2]
        mapped_answer = replace_local_citations(answer, local_map)
        mapped_answer = re.sub(r'\[(\d+)\](?:,\s*\[\1\])+', r'[\1]', mapped_answer)
        answers[qi] = (mapped_answer, local_map)
        n_cit = len(cits)
        print(f"  Q{qi}: {len(answer)} char, {n_cit} citations")

    # Determine output order
    q_order = args.q_order  # list of int; may differ from query_indices for reordering

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

    # Intro (Q1) -- unnumbered Bevezetes section (heading_numberer leaves it unnumbered)
    if 1 in answers and 1 in q_order:
        text, _ = answers[1]
        body.append("<!-- Q:1 -->")
        body.append("## Bevezetes")
        body.append("")
        body.append(text)
        body.append("")

    # Content sections (Q2+):
    # L1-szintű DFS node-oknál MINDIG szekciócímet szúrunk a mindmap node nevéből (RC-2 fix).
    # L2+ node-oknál: az NLM válasz első ## vagy ### headingéből kíséreljük meg kinyerni a címet.
    # heading_numberer.py is the sole source of section numbering (D6).
    for qi in q_order:
        if qi == 1:
            continue  # already handled
        if qi not in answers:
            continue
        text, _ = answers[qi]

        # Check if this query is an L1 node
        node_info = node_list.get(str(qi), {})
        node_level = node_info.get("level", -1)
        node_name  = node_info.get("name", "")

        is_msc = node_info.get("is_msc", False)
        body.append(f"<!-- Q:{qi} -->")
        if is_msc:
            body.append("<!-- MSc -->")
        if node_level in (1, 2) and node_name:
            # L1 és L2 nodes always get a ## section with the mindmap node name.
            # Strip any leading ## from the NLM answer to avoid duplication
            # (J1 Prompt B now makes NLM start with ##, so we must remove it here).
            _, text_body = extract_section_title(text)
            msc_label = "[MSc] " if is_msc else ""
            body.append(f"## {msc_label}{node_name}")
            body.append("")
            body.append(text_body)
        else:
            # L3+ nodes: try to extract title from NLM answer heading
            section_title, text_body = extract_section_title(text)
            if section_title:
                msc_label = "[MSc] " if is_msc else ""
                body.append(f"## {msc_label}{section_title}")
            # If no ## extracted: answer's own headings become the section structure
            body.append("")
            body.append(text_body)
        if is_msc:
            body.append("<!-- /MSc -->")
        body.append("")

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
    print(f"Írva: {out_path}  ({len(text)} karakter)", file=sys.stderr)


if __name__ == "__main__":
    main()