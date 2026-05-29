"""
14_util_pandoc_export.py -- Camera-ready DOCX export Pandoc-kal.

A 4_wip_outputs/N_Jegyzet.md (vagy 5_clean_outputs/N_Jegyzet_bsc.md) Markdown
fájlt Word DOCX-be konvertálja a templates/due_jegyzet_template.docx
reference-dokumentum stílusaival.

Előfeltétel: pandoc telepítve (https://pandoc.org/installing.html).
  Windows: winget install --id JohnMacFarlane.Pandoc
Ha a pandoc nincs telepítve, a script világos hibaüzenetet ad és kilép (exit 2).

Usage:
    python scripts/14_util_pandoc_export.py --week-dir <path/to/N_het>
    python scripts/14_util_pandoc_export.py --week-dir <path> --bsc   # a _bsc verziót
    python scripts/14_util_pandoc_export.py --week-dir <path> --no-template
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def resolve_pandoc(project_root: Path) -> str | None:
    """Find pandoc: PATH > .claude/config.json > winget install glob."""
    import os
    p = shutil.which("pandoc")
    if p:
        return p
    # .claude/config.json
    cfg = project_root / ".claude" / "config.json"
    if cfg.exists():
        try:
            data = json.loads(cfg.read_bytes().decode("utf-8-sig"))
            cand = data.get("pandoc_path")
            if cand and Path(cand).exists():
                return cand
        except Exception:
            pass
    # winget default install location (PATH not refreshed in current shell)
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages"
    if base.is_dir():
        for exe in base.glob("JohnMacFarlane.Pandoc*/pandoc*/pandoc.exe"):
            return str(exe)
    return None


def resolve_week(week_dir: Path, week_arg) -> int:
    if week_arg:
        return int(week_arg)
    seed = week_dir / "1_raw_inputs" / "citations_seed.json"
    if seed.exists():
        data = json.loads(seed.read_bytes().decode("utf-8-sig"))
        return data.get("_meta", {}).get("week", 1)
    return 1


def find_template(project_root: Path) -> Path | None:
    """Locate the Jegyzet reference docx in templates/."""
    cands = [
        project_root / "templates" / "due_jegyzet_template.docx",
        project_root / "templates" / "du_jegyzet_template.docx",
    ]
    for c in cands:
        if c.exists():
            return c
    # Fallback: any *jegyzet*.docx
    tdir = project_root / "templates"
    if tdir.is_dir():
        for f in tdir.glob("*jegyzet*.docx"):
            return f
    return None


def main():
    parser = argparse.ArgumentParser(description="Camera-ready DOCX export Pandoc-kal")
    parser.add_argument("--week-dir", required=True, type=Path)
    parser.add_argument("--week", default=None, type=int)
    parser.add_argument("--bsc", action="store_true",
                        help="A 5_clean_outputs/N_Jegyzet_bsc.md-t konvertálja")
    parser.add_argument("--no-template", action="store_true",
                        help="Reference template nélkül (Pandoc alapstílus)")
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()
    # Project root = ascend until we find templates/ (or use cwd)
    project_root = Path(__file__).resolve().parent.parent

    # 1. Pandoc availability check (PATH > config.json > winget glob)
    pandoc = resolve_pandoc(project_root)
    if not pandoc:
        print("[HIBA] pandoc nincs telepítve.", file=sys.stderr)
        print("  Telepítés (Windows): winget install --id JohnMacFarlane.Pandoc", file=sys.stderr)
        print("  Vagy: https://pandoc.org/installing.html", file=sys.stderr)
        print("  (Telepítés után új shell vagy PATH-frissítés szükséges; a script", file=sys.stderr)
        print("   a winget install mappáját is megnézi automatikusan.)", file=sys.stderr)
        sys.exit(2)

    week = resolve_week(week_dir, args.week)

    # 2. Locate input Markdown
    if args.bsc:
        src = week_dir / "5_clean_outputs" / f"{week}_Jegyzet_bsc.md"
    else:
        src = week_dir / "4_wip_outputs" / f"{week}_Jegyzet.md"
    if not src.exists():
        sys.exit(f"[HIBA] nem található: {src}")

    # 3. Output
    clean_dir = week_dir / "5_clean_outputs"
    clean_dir.mkdir(parents=True, exist_ok=True)
    suffix = "_bsc" if args.bsc else ""
    out = clean_dir / f"{week}_Jegyzet{suffix}.docx"

    # 4. Build pandoc command
    cmd = [pandoc, str(src), "-o", str(out),
           "--from", "gfm+tex_math_dollars",  # GFM + $...$ LaTeX math
           "--standalone"]

    template = None if args.no_template else find_template(project_root)
    if template:
        cmd += ["--reference-doc", str(template)]
        print(f"  Reference template: {template.name}")
    else:
        if not args.no_template:
            print("  WARN  nincs jegyzet template a templates/-ben -- alapstílus")

    # 5. Run
    print(f"  Konvertálás: {src.name} -> {out.name}")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        print(f"[HIBA] pandoc rc={result.returncode}", file=sys.stderr)
        if result.stderr:
            print(result.stderr[:500], file=sys.stderr)
        sys.exit(1)

    size_kb = out.stat().st_size // 1024 if out.exists() else 0
    print(f"OK: {out} ({size_kb} KB)")


if __name__ == "__main__":
    main()
