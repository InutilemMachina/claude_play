"""
03_all.py -- Egységes belépési pont a 03. pipeline lépéshez.

Sorban futtatja:
    1. 03_util_source_extractor.py --week-dir  (nem-PDF forrásextrakció)
    2. 03_run_mineru_pipeline.py --root         (MinerU PDF feldolgozás)

Felváltja a kétlépéses kézi hívást.

Usage:
    python scripts/03_all.py --week-dir <path/to/N_het> [--backend pipeline] [--yes]

A tantárgy gyökere automatikusan kiszámítódik: week_dir.parent.parent
(pl. test_outputs/mini3/1_het → test_outputs/mini3)
"""

import argparse
import subprocess
import sys
from pathlib import Path

try:
    from _encoding_fix import fix_stdout as _fix_stdout
    _fix_stdout()
except ImportError:
    pass

SCRIPTS_DIR = Path(__file__).resolve().parent


def run(cmd: list, label: str) -> int:
    print(f"\n{'='*60}")
    print(f"[03_all] {label}")
    print(f"{'='*60}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"[03_all] HIBA: {label} visszatérési kód: {result.returncode}")
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="03 pipeline lépés: forrásextrakció + MinerU"
    )
    parser.add_argument(
        "--week-dir", required=True,
        help="Heti mappa (pl. test_outputs/mini3/1_het)"
    )
    parser.add_argument(
        "--types", nargs="+", default=None,
        help="Forrástípusok az extractornak (pl. pptx html docx)"
    )
    parser.add_argument(
        "--backend", default="pipeline",
        choices=["pipeline", "vlm-transformers", "vlm-sglang"],
        help="MinerU backend (alapérték: pipeline)"
    )
    parser.add_argument(
        "--yes", action="store_true",
        help="Nagy fájloknál ne kérdezzen"
    )
    parser.add_argument(
        "--warn-mb", type=float, default=None,
        help="Fájlméret MB-ben, ami felett kérdez"
    )
    args = parser.parse_args()

    week_dir = Path(args.week_dir).resolve()
    if not week_dir.exists():
        sys.exit(f"[03_all] HIBA: week-dir nem található: {week_dir}")

    # subject root: week_dir / .. / .. (pl. test_outputs/mini3)
    subject_root = week_dir.parent.parent

    # --- Lépés 1: forrásextrakció (nem-PDF) ---
    extractor_cmd = [sys.executable, str(SCRIPTS_DIR / "03_util_source_extractor.py"),
                     "--week-dir", str(week_dir)]
    if args.types:
        extractor_cmd += ["--types"] + args.types
    rc1 = run(extractor_cmd, "03_util_source_extractor (nem-PDF extrakció)")

    # --- Lépés 2: MinerU (PDF) ---
    mineru_cmd = [sys.executable, str(SCRIPTS_DIR / "03_run_mineru_pipeline.py"),
                  "--root", str(subject_root),
                  "--backend", args.backend]
    if args.yes:
        mineru_cmd.append("--yes")
    if args.warn_mb is not None:
        mineru_cmd += ["--warn-mb", str(args.warn_mb)]
    rc2 = run(mineru_cmd, "03_run_mineru_pipeline (MinerU PDF feldolgozás)")

    if rc1 != 0 or rc2 != 0:
        sys.exit(f"[03_all] Egy vagy több lépés hibával zárult (extractor: {rc1}, mineru: {rc2})")
    print("\n[03_all] Kész.")


if __name__ == "__main__":
    main()
