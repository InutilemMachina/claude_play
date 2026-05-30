"""
04_nlm_dfs_queries.py -- Mindmap-based DFS NLM query runner

Parses nlm_mindmap_export.md and generates one NLM query per node
using the pipeline.md §3 template (DFS traversal).

Usage:
    python scripts/04_nlm_dfs_queries.py --week-dir test_outputs/DFT_teszt/1_het

Output:
    3_raw_outputs/nlm_qN_raw.txt   (one per mindmap node, 1-indexed)
    3_raw_outputs/dfs_query_log.txt

Template:
    Root:  "Beszeljen az ezekben a forrasokban targyalt [root] temakorrol."
    Child: "Beszeljen az ezekben a forrasokban targyalt, a(z) [parent]
            tagabb kontextusaba tartozo [node] temakorrol."
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from _citations_util import build_citations_json, load_seed as _load_seed

# NLM CLI path resolution (priority: env var > .claude/config.json > default)
_DEFAULT_NLM_PATH = r"C:\Users\lasz\AppData\Roaming\uv\tools\notebooklm-mcp-cli\Scripts\nlm.exe"

def _resolve_nlm_path() -> str:
    """Resolve nlm.exe path: NLM_PATH env var > .claude/config.json > default."""
    if env := os.environ.get("NLM_PATH"):
        return env
    # Look for .claude/config.json in project root (parent of scripts/)
    cfg = Path(__file__).parent.parent / ".claude" / "config.json"
    if cfg.exists():
        try:
            data = json.loads(cfg.read_bytes().decode("utf-8-sig"))
            if p := data.get("nlm_path"):
                return p
        except Exception:
            pass
    return _DEFAULT_NLM_PATH

NLM_PATH = _resolve_nlm_path()

# ---------------------------------------------------------------------------
# Mindmap parser
# ---------------------------------------------------------------------------

def strip_meta(name: str) -> str:
    """Remove ', N gyermek' suffix and vision-bypass '(?)' markers from node names."""
    import re
    name = re.sub(r",\s*\d+\s+gyermek", "", name)
    name = re.sub(r"\s*\(\?\)", "", name)
    return name.strip()


def parse_mindmap(path: Path) -> list[tuple[str, str | None]]:
    """
    Returns list of (node_name, parent_name) in DFS order.
    parent_name is None for the root.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    nodes: list[tuple[str, str | None]] = []
    # Stack: list of (indent_level, node_name)
    stack: list[tuple[int, str]] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Determine indent level and node type
        if line.startswith("# "):
            level = 0
            name = strip_meta(line[2:].strip())
        elif line.startswith("## "):
            level = 1
            name = strip_meta(line[3:].strip())
        elif stripped.startswith("- "):
            # Count leading spaces to determine indent
            spaces = len(line) - len(line.lstrip(" "))
            # Each 2 spaces = 1 level; base dash level starts at 2
            level = 2 + spaces // 2
            name = strip_meta(stripped[2:].strip())
        else:
            continue

        # Find parent: last stack entry with level < current
        while stack and stack[-1][0] >= level:
            stack.pop()

        parent = stack[-1][1] if stack else None
        nodes.append((name, parent))
        stack.append((level, name))

    return nodes


# ---------------------------------------------------------------------------
# Qfig query (ingyenes VLM alternatíva -- RC-4 fix)
# ---------------------------------------------------------------------------

QFIG_PROMPT = (
    "Sorold fel az osszes abrat, diagramot, grafikont es tablazatot a forrasokban! "
    "Minden elemhez add meg: (1) a forras nevet kiterjeszessel, (2) az abra szamat ha van, "
    "(3) a captionjet ha van, (4) 3-5 angol kulcsszot vesszevel elvalasztva, amelyek "
    "leirjak a vizualis tartalmat. Formatum minden elemhez:\n"
    "FORRAS: <fajlnev.pdf>\n"
    "SZAM: <abra szama vagy 'nincs'>\n"
    "CAPTION: <caption szovege vagy 'nincs'>\n"
    "KEYWORDS: <kulcsszavak>\n"
    "---"
)


def run_qfig_query(nb_id: str, out_path: Path) -> bool:
    """Run a single Qfig query and write output to out_path."""
    import subprocess
    cmd = [NLM_PATH, "query", "notebook", nb_id, QFIG_PROMPT, "--json"]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=300
        )
        output = result.stdout.strip()
        if output:
            out_path.write_text(output, encoding="utf-8")
            print(f"  Qfig: {out_path.name} ({len(output)} chars, rc={result.returncode})")
            return result.returncode == 0
        else:
            print(f"  Qfig: EMPTY output, rc={result.returncode}", file=sys.stderr)
            if result.stderr:
                print(f"  stderr: {result.stderr[:200]}", file=sys.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("  Qfig: TIMEOUT", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  Qfig: ERROR: {e}", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# Query builder
# ---------------------------------------------------------------------------

def build_query(node: str, parent: str | None) -> str:
    # Keep original -- nlm handles UTF-8 on Windows if invoked directly
    if parent is None:
        # J3: Root node = pure intro, not a full overview (avoids massive repetition)
        return (
            f"Irjon rovid, 2-3 bekezdesbol allo, osszefuggo bevezeto szoveget a(z) {node} "
            f"teruleterol BSc hallgatoknak. Csak az alapelvet es a teruletet hatarozza meg -- "
            f"a reszleteket (torvenyek, kameraepites, alkalmazasok) NE targyalja, "
            f"azok kesobb kiemelten kerulnek kifejtesre."
        )
    else:
        return (
            f"Beszeljen az ezekben a forrasokban targyalt, "
            f"a(z) {parent} tagabb kontextusaba tartozo {node} temakorrol."
        )


# ---------------------------------------------------------------------------
# NLM caller
# ---------------------------------------------------------------------------

RESOURCE_EXHAUSTED_MARKER = "RESOURCE_EXHAUSTED"
MIN_VALID_BYTES = 500  # outputs shorter than this are considered invalid


def is_resource_exhausted(output: str) -> bool:
    """Detect Google RESOURCE_EXHAUSTED quota error in JSON response."""
    return RESOURCE_EXHAUSTED_MARKER in output


def nlm_query(nb_id: str, query: str, out_path: Path, log_fh) -> bool:
    cmd = [NLM_PATH, "query", "notebook", nb_id, query, "--json"]
    log_fh.write(f"CMD: {' '.join(cmd[:5])}...\n")
    log_fh.flush()

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=300
        )
        output = result.stdout.strip()
        if output:
            if is_resource_exhausted(output):
                log_fh.write(f"  -> QUOTA_ERROR (RESOURCE_EXHAUSTED) -- skipping write\n")
                return False
            out_path.write_text(output, encoding="utf-8")
            log_fh.write(f"  -> {out_path.name}: {len(output)} chars, rc={result.returncode}\n")
            return result.returncode == 0
        else:
            log_fh.write(f"  -> EMPTY output, rc={result.returncode}\n")
            if result.stderr:
                log_fh.write(f"  stderr: {result.stderr[:200]}\n")
            return False
    except subprocess.TimeoutExpired:
        print(f"  [TIMEOUT] {out_path.name} -- 300s lejárt, kihagyva")
        log_fh.write(f"  -> TIMEOUT (300s) -- skipping\n")
        return False
    except subprocess.TimeoutExpired:
        log_fh.write(f"  -> TIMEOUT\n")
        return False
    except Exception as e:
        log_fh.write(f"  -> ERROR: {e}\n")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--week-dir", required=True)
    parser.add_argument("--max-level", type=int, default=99,
                        help="Max mindmap depth to query (0=root only, 99=all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print queries without calling NLM")
    parser.add_argument("--resume", action="store_true",
                        help=f"Skip existing output files larger than {MIN_VALID_BYTES} bytes")
    parser.add_argument("--sleep", type=float, default=2.0,
                        help="Seconds to sleep between queries (default: 2)")
    parser.add_argument("--qfig", action="store_true",
                        help="Run Qfig figure query (writes nlm_qfig_raw.txt); skips DFS")
    args = parser.parse_args()

    week_dir = Path(args.week_dir).resolve()
    raw_out  = week_dir / "3_raw_outputs"
    raw_out.mkdir(exist_ok=True)

    # Load notebook ID from citations_seed.json
    seed_path = week_dir / "1_raw_inputs" / "citations_seed.json"
    seed = _load_seed(seed_path)
    nb_id = seed.get("_notebook", {}).get("id")
    if not nb_id:
        sys.exit("HIBA: _notebook.id hiányzik a citations_seed.json-ből")

    # --qfig mode: run figure query only, skip DFS
    if args.qfig:
        qfig_path = raw_out / "nlm_qfig_raw.txt"
        print(f"Qfig query -> {qfig_path.name}")
        ok = run_qfig_query(nb_id, qfig_path)
        sys.exit(0 if ok else 1)

    # Parse mindmap
    mindmap_path = raw_out / "nlm_mindmap_export.md"
    if not mindmap_path.exists():
        sys.exit(f"HIBA: nem található: {mindmap_path}")

    nodes = parse_mindmap(mindmap_path)
    print(f"Mindmap: {len(nodes)} csomópont | Notebook: {nb_id}")

    # Filter by max level (approximate: count parent chain length)
    # Build parent->level map
    level_map: dict[str, int] = {}
    for name, parent in nodes:
        if parent is None:
            level_map[name] = 0
        else:
            level_map[name] = level_map.get(parent, 0) + 1

    filtered = [(n, p) for n, p in nodes if level_map.get(n, 0) <= args.max_level]
    print(f"Futtatandó (max-level={args.max_level}): {len(filtered)} query")

    # Write dfs_node_list.json for 05_assemble.py (L1 sectioning)
    node_list = {}
    for i, (node, parent) in enumerate(filtered, 1):
        node_list[str(i)] = {
            "name": node,
            "level": level_map.get(node, 0),
            "parent": parent,
        }
    node_list_path = raw_out / "dfs_node_list.json"
    node_list_path.write_text(json.dumps(node_list, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"dfs_node_list.json írva: {len(node_list)} bejegyzés")

    if args.dry_run:
        for i, (node, parent) in enumerate(filtered, 1):
            q = build_query(node, parent)
            print(f"Q{i:02d} [L{level_map.get(node,0)}] {node}")
            print(f"     -> {q[:100]}")
        return

    log_path = raw_out / "dfs_query_log.txt"
    ok_count = 0
    with open(log_path, "w", encoding="utf-8") as log_fh:
        log_fh.write(f"DFS NLM queries -- {len(filtered)} csomópont\n\n")
        for i, (node, parent) in enumerate(filtered, 1):
            q = build_query(node, parent)
            out_file = raw_out / f"nlm_q{i}_raw.txt"
            ts = time.strftime("%H:%M:%S")
            msg = f"[{ts}] Q{i}/{len(filtered)} L{level_map.get(node,0)} -- {node}"
            print(msg)
            log_fh.write(f"{msg}\n  Query: {q}\n")
            # --resume: skip if file already exists and is valid
            if args.resume and out_file.exists() and out_file.stat().st_size >= MIN_VALID_BYTES:
                print(f"  [SKIP] {out_file.name} already valid ({out_file.stat().st_size} B)")
                log_fh.write(f"  [SKIP] {out_file.name} already valid\n")
                ok_count += 1
                continue

            ok = nlm_query(nb_id, q, out_file, log_fh)
            if ok:
                ok_count += 1
            time.sleep(args.sleep)

    print(f"\nKész: {ok_count}/{len(filtered)} sikeres. Log: {log_path}")

    # Build citations.json from seed + discovered UUIDs in raw outputs
    citations = build_citations_json(seed, raw_out)
    citations_path = raw_out / "citations.json"
    citations_path.write_text(json.dumps(citations, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"citations.json irva: {len(citations)} forras -> {citations_path.name}")


if __name__ == "__main__":
    main()
