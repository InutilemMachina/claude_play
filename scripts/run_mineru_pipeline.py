"""
run_mineru_pipeline.py -- MinerU pipeline vizualis folyamatkovetesssel

Feladat: raw_sources/*.pdf -> clean_sources/kepek/ + figure_catalog.json
         Minden notebook (het-mappa) es fajl szamlaloval, MinerU progress-barral.
         Nagy fajloknal a felhasznalo donti el, feldolgozza-e.

Futtatas (tantargy gyokerebol):
    python ../../scripts/run_mineru_pipeline.py [--root <tantargy_mappa>] [--warn-mb 20]

Peldak:
    # Claude_play gyokerebol:
    python scripts/run_mineru_pipeline.py --root haromhetes_teszt
    # Tantargy mappan belulrol:
    cd haromhetes_teszt && python ../scripts/run_mineru_pipeline.py
"""

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

try:
    from rich.columns import Columns
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import (BarColumn, Progress, SpinnerColumn,
                               TaskProgressColumn, TextColumn,
                               TimeElapsedColumn)
    from rich.rule import Rule
    from rich.table import Table
    from rich.text import Text
    RICH = True
except ImportError:
    RICH = False

# ── Konfiguracio ──────────────────────────────────────────────────────────────
WARN_MB_DEFAULT = 20       # e felett figyelmeztetes + kerdes
CONDA_ENV       = "mineru" # conda kornyezet neve
MAGIC_PDF_CMD   = ["conda", "run", "-n", CONDA_ENV, "--no-capture-output",
                   "magic-pdf", "-p", "{pdf}", "-o", "{out}", "-m", "auto"]

# ── Helper-ek ─────────────────────────────────────────────────────────────────
console = Console() if RICH else None


def human_mb(path: Path) -> float:
    return path.stat().st_size / 1_048_576


def count_pdf_pages(pdf_path: Path) -> int:
    """Gyors oldalszamlales pypdf-fel (fallback: 0)."""
    try:
        import pypdf
        return len(pypdf.PdfReader(str(pdf_path)).pages)
    except Exception:
        return 0


def discover_notebooks(root: Path) -> list[tuple[str, list[Path]]]:
    """
    Visszaadja a het-mappak listajat (notebook_nev, pdf_lista) rendezett sorban.
    Keresi: root/N_*/raw_sources/*.pdf
    """
    notebooks = []
    for week_dir in sorted(root.iterdir()):
        raw = week_dir / "raw_sources"
        if not raw.is_dir():
            continue
        pdfs = sorted(raw.glob("*.pdf"))
        if pdfs:
            notebooks.append((week_dir.name, pdfs))
    return notebooks


def ask_user(prompt: str) -> str:
    """Interaktiv billentyuleutes (i/k/q)."""
    if RICH:
        console.print(prompt, end="")
    else:
        print(prompt, end="", flush=True)
    return input().strip().lower()


def should_process(pdf: Path, warn_mb: float) -> bool:
    """
    Ha a fajl nagyobb warn_mb MB-nel, kerdi a felhasznalot.
    Visszateres: True = feldolgozas, False = kihagyas.
    """
    mb = human_mb(pdf)
    if mb < warn_mb:
        return True

    size_str = f"{mb:.1f} MB"
    if RICH:
        console.print(
            f"      [yellow]⚠️  Nagy fajl:[/yellow] [bold]{pdf.name}[/bold]"
            f" [dim]({size_str})[/dim]"
        )
        answer = ask_user(
            "      Feldolgozzuk? "
            "\\[[green]i[/green]]gen / "
            "\\[[red]k[/red]]ihagyas / "
            "\\[[bold]q[/bold]]uit : "
        )
    else:
        print(f"      ⚠️  Nagy fajl: {pdf.name} ({size_str})")
        answer = ask_user("      Feldolgozzuk? [i]gen / [k]ihagyas / [q]uit : ")

    if answer in ("q", "quit", "exit"):
        if RICH:
            console.print("[bold red]Megszakitva.[/bold red]")
        else:
            print("Megszakitva.")
        sys.exit(0)

    return answer in ("i", "igen", "y", "yes", "")


def run_mineru(pdf: Path, out_dir: Path, pages: int) -> bool:
    """
    Futtatja a magic-pdf-et, valosi idejU progress-barral.
    Visszateres: True = siker, False = hiba.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        c.replace("{pdf}", str(pdf)).replace("{out}", str(out_dir))
        for c in MAGIC_PDF_CMD
    ]

    # ── Rich progress bar ──────────────────────────────────────────────────
    if RICH:
        with Progress(
            SpinnerColumn(),
            TextColumn("      "),
            BarColumn(bar_width=28),
            TaskProgressColumn(),
            TextColumn("[dim]{task.fields[detail]}[/dim]"),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        ) as prog:
            task = prog.add_task(
                "MinerU",
                total=max(pages, 1),
                detail=f"0/{pages} oldal" if pages else "fut...",
            )

            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True, bufsize=1,
                errors="replace",
            )

            for line in proc.stdout:
                # tqdm / magic-pdf progress: "XX%|...| N/M [...]"
                m = re.search(r"(\d+)%\|.*?(\d+)/(\d+)", line)
                if m:
                    pct   = int(m.group(1))
                    done  = int(m.group(2))
                    total = int(m.group(3))
                    prog.update(
                        task,
                        completed=done,
                        total=max(total, 1),
                        detail=f"{done}/{total} oldal",
                    )
                    continue

                # magic-pdf soros log: "page_id: N" vagy "INFO - page N"
                m2 = re.search(r"page[_\s-]*(?:id[:\s]+)?(\d+)", line, re.I)
                if m2 and pages:
                    done = int(m2.group(1)) + 1
                    pct  = min(int(done / pages * 100), 100)
                    prog.update(
                        task,
                        completed=done,
                        detail=f"{done}/{pages} oldal",
                    )

            proc.wait()
            if proc.returncode == 0:
                prog.update(task, completed=max(pages, 1), detail="kesz")

    # ── Fallback: egyszerű szoveg ─────────────────────────────────────────
    else:
        print(f"      [MinerU] {pdf.name} ...", end="", flush=True)
        proc = subprocess.run(cmd, capture_output=True, text=True)
        print(" KESZ" if proc.returncode == 0 else " HIBA")

    return proc.returncode == 0


# ── Fo fuggveny ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="MinerU pipeline vizualis futtatasa")
    parser.add_argument(
        "--root", default=".",
        help="Tantargy gyokermappaja (alapertek: aktualis konyvtar)"
    )
    parser.add_argument(
        "--warn-mb", type=float, default=WARN_MB_DEFAULT,
        help=f"Fajlmeret MB-ben, ami felett kerdez (alapertek: {WARN_MB_DEFAULT})"
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        sys.exit(f"HIBA: mappa nem talalhato: {root}")

    notebooks = discover_notebooks(root)
    if not notebooks:
        sys.exit(f"HIBA: nincs raw_sources/*.pdf a {root} alatt.")

    nb_total = len(notebooks)

    if RICH:
        console.print(Rule(f"[bold]MinerU Pipeline[/bold] -- {root.name}"))
        console.print(
            f"[dim]Notebookok: {nb_total} | "
            f"Figyelmeztetesi hatar: {args.warn_mb:.0f} MB[/dim]\n"
        )
    else:
        print(f"=== MinerU Pipeline: {root.name} ({nb_total} notebook) ===\n")

    results = []  # (notebook, fajl, statusz)

    for nb_idx, (nb_name, pdfs) in enumerate(notebooks, 1):
        week_dir  = root / nb_name
        clean_dir = week_dir / "clean_sources" / "kepek"
        pdf_total = len(pdfs)

        if RICH:
            console.print(
                f"[bold cyan][{nb_idx}/{nb_total}][/bold cyan] "
                f"Notebook: [bold]{nb_name}[/bold] "
                f"[dim]({pdf_total} PDF)[/dim]"
            )
        else:
            print(f"[{nb_idx}/{nb_total}] Notebook: {nb_name} ({pdf_total} PDF)")

        for f_idx, pdf in enumerate(pdfs, 1):
            mb     = human_mb(pdf)
            pages  = count_pdf_pages(pdf)
            mb_str = f"{mb:.1f} MB"
            pg_str = f"{pages}p" if pages else "?"

            if RICH:
                console.print(
                    f"  [bold white][{f_idx}/{pdf_total}][/bold white] "
                    f"{pdf.name} [dim]({mb_str}, {pg_str})[/dim]"
                )
            else:
                print(f"  [{f_idx}/{pdf_total}] {pdf.name} ({mb_str}, {pg_str})")

            # Nagy fajl kerdes
            if not should_process(pdf, args.warn_mb):
                if RICH:
                    console.print("      [yellow]→ KIHAGYVA[/yellow]")
                else:
                    print("      → KIHAGYVA")
                results.append((nb_name, pdf.name, "KIHAGYVA"))
                continue

            # MinerU futtatasa
            ok = run_mineru(pdf, clean_dir / pdf.stem, pages)

            if ok:
                if RICH:
                    console.print(f"      [green]✓ {pdf.name}[/green]")
                else:
                    print(f"      ✓ {pdf.name}")
                results.append((nb_name, pdf.name, "OK"))
            else:
                if RICH:
                    console.print(f"      [red]✗ HIBA: {pdf.name}[/red]")
                else:
                    print(f"      ✗ HIBA: {pdf.name}")
                results.append((nb_name, pdf.name, "HIBA"))

        if RICH:
            console.print()

    # ── Osszefoglalo ──────────────────────────────────────────────────────────
    ok_n   = sum(1 for _, _, s in results if s == "OK")
    skip_n = sum(1 for _, _, s in results if s == "KIHAGYVA")
    err_n  = sum(1 for _, _, s in results if s == "HIBA")

    if RICH:
        table = Table(title="Osszefoglalo", show_header=True, header_style="bold")
        table.add_column("Notebook")
        table.add_column("Fajl")
        table.add_column("Statusz")
        for nb, f, s in results:
            color = {"OK": "green", "KIHAGYVA": "yellow", "HIBA": "red"}[s]
            table.add_row(nb, f, Text(s, style=color))
        console.print(table)
        console.print(
            f"\n[green]✓ {ok_n} OK[/green]  "
            f"[yellow]{skip_n} kihagyva[/yellow]  "
            f"[red]{err_n} hiba[/red]"
        )
    else:
        print("\n--- Osszefoglalo ---")
        for nb, f, s in results:
            print(f"  {s:10s}  {nb}/{f}")
        print(f"\nOK: {ok_n}  Kihagyva: {skip_n}  Hiba: {err_n}")

    # Visszateresi kod: 0 ha nincs hiba, 1 ha van
    sys.exit(1 if err_n else 0)


if __name__ == "__main__":
    main()
