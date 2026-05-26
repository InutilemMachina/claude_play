"""
04_nlm_dfs_queries.py -- Mindmap-based DFS NLM query runner

Parses nlm_mindmap_export.md and generates one NLM query per node
using the pipeline.md §3 template (DFS traversal).

Usage:
    python scripts/04_nlm_dfs_queries.py --week-dir test_outputs/DFT_teszt/1_het

Output:
    3_raw_outputs/nlm_qNN_raw.txt  (one per mindmap node, zero-padded)
    3_raw_outputs/dfs_query_log.txt

Template:
    Root:  "Beszeljen az ezekben a forrasokban targyalt [root] temakorrol."
    Child: "Beszeljen az ezekben a forrasokban targyalt, a(z) [parent]
            tagabb kontextusaba tartozo [node] temakorrol."
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

NLM_PATH = r"C:\Users\lasz\AppData\Roaming\uv\tools\notebooklm-mcp-cli\Scripts\nlm.exe"

# ---------------------------------------------------------------------------
# Mindmap parser
# ---------------------------------------------------------------------------

def strip_meta(name: str) -> str:
    """Remove ', N gyermek' suffix from node names."""
    import re
    return re.sub(r",\s*\d+\s+gyermek", "", name).strip()


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
# Query builder
# ---------------------------------------------------------------------------

def build_query(node: str, parent: str | None) -> str:
    # ASCII version to avoid PowerShell encoding issues
    node_a   = node.encode("ascii", "ignore").decode()   # fallback
    # Keep original -- nlm handles UTF-8 on Windows if invoked directly
    if parent is None:
        return f"Beszeljen az ezekben a forrasokban targyalt {node} temakorrol."
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
    args = parser.parse_args()

    week_dir = Path(args.week_dir).resolve()
    raw_out  = week_dir / "3_raw_outputs"
    raw_out.mkdir(exist_ok=True)

    # Load notebook ID from citations_seed.json
    seed_path = week_dir / "1_raw_inputs" / "citations_seed.json"
    seed = json.loads(seed_path.read_bytes().decode("utf-8-sig"))
    nb_id = seed.get("_notebook", {}).get("id")
    if not nb_id:
        sys.exit("HIBA: _notebook.id hiányzik a citations_seed.json-ből")

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
            out_file = raw_out / f"nlm_q{i:02d}_raw.txt"
            ts = time.strftime("%H:%M:%S")
            msg = f"[{ts}] Q{i:02d}/{len(filtered)} L{level_map.get(node,0)} -- {node}"
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


if __name__ == "__main__":
    main()
