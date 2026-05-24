"""
nlm_query.py -- NLM CLI wrapper with proper UTF-8 handling

Feladat: `nlm query notebook` és `nlm mindmap create` futtatása Python
         subprocess-on keresztül, hogy a PowerShell pipe-encoding-hiba elkerülhető.

Futtatás:
    python scripts/nlm_query.py query <notebook_id> "<kerdes>" <output.txt> [--conv <conv_id>]
    python scripts/nlm_query.py mindmap <notebook_id> <output.txt> [--title "Cim"]

Pelda:
    python scripts/nlm_query.py query 6d6525ba-... "Mi a Matrix Profile?" clean_sources/nlm_q1_raw.txt
"""

import argparse
import subprocess
import sys
from pathlib import Path

NLM_EXE = r"C:\Users\lasz\AppData\Roaming\uv\tools\notebooklm-mcp-cli\Scripts\nlm.exe"


def run_nlm(args_list: list[str]) -> tuple[int, str, str]:
    """Futtat egy nlm parancsot, visszaadja (returncode, stdout, stderr)."""
    result = subprocess.run(
        [NLM_EXE] + args_list,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode, result.stdout, result.stderr


def cmd_query(nb_id: str, question: str, output: Path,
              conv_id: str | None, use_json: bool) -> int:
    args = ["query", "notebook", nb_id, question]
    if conv_id:
        args += ["--conversation-id", conv_id]
    if use_json:
        args += ["--json"]

    rc, stdout, stderr = run_nlm(args)
    if rc != 0:
        print(f"HIBA (rc={rc}):\n{stderr}", file=sys.stderr)
        return rc

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(stdout, encoding="utf-8")
    print(f"OK -> {output}")
    return 0


def cmd_mindmap(nb_id: str, output: Path, title: str) -> int:
    args = ["mindmap", "create", nb_id, "--title", title, "--confirm", "--json"]
    rc, stdout, stderr = run_nlm(args)

    # Ha --json nem tamogatott, probalkozunk nelkule
    if rc != 0 and "--json" in stderr:
        args = ["mindmap", "create", nb_id, "--title", title, "--confirm"]
        rc, stdout, stderr = run_nlm(args)

    if rc != 0:
        print(f"HIBA (rc={rc}):\n{stderr}", file=sys.stderr)
        return rc

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(stdout, encoding="utf-8")
    print(f"OK -> {output}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="NLM CLI UTF-8 wrapper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("query", help="nlm query notebook")
    q.add_argument("nb_id")
    q.add_argument("question")
    q.add_argument("output", type=Path)
    q.add_argument("--conv", default=None)
    q.add_argument("--no-json", action="store_true")

    m = sub.add_parser("mindmap", help="nlm mindmap create")
    m.add_argument("nb_id")
    m.add_argument("output", type=Path)
    m.add_argument("--title", default="Mind Map")

    args = parser.parse_args()

    if args.cmd == "query":
        sys.exit(cmd_query(args.nb_id, args.question, args.output,
                           args.conv, not args.no_json))
    elif args.cmd == "mindmap":
        sys.exit(cmd_mindmap(args.nb_id, args.output, args.title))


if __name__ == "__main__":
    main()
