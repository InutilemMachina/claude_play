import argparse
import subprocess
import sys
from pathlib import Path

# Files to skip (by filename, without folder path)
SKIP_FILES = {
    "D6 kieg - gravdahl1999-Book--Compressor Surge and Rotating Stall.pdf",
    "D6 kieg - gravdahl1999-Chapter 1--Compressor Surge and Rotating Stall.pdf"
}

# Supported file extensions (mineru handles these)
SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".docx", ".pptx", ".xlsx"}

DEFAULT_OUTPUT = "./mineru_tests"

# PDFs with more pages than this threshold trigger a confirmation prompt
LONG_PDF_PAGE_THRESHOLD = 50


def get_pdf_page_count(file_path: str) -> int | None:
    """Return the page count of a PDF, or None if it cannot be determined.

    Requires pypdf. If the package is missing, returns None silently.
    """
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        return len(reader.pages)
    except ImportError:
        return None
    except Exception:
        return None


def confirm_long_pdf(file_path: str, page_count: int, yes: bool) -> bool:
    """Print a warning for long PDFs and return True if processing should proceed.

    If yes=True (--yes flag), skips the interactive prompt and proceeds automatically.
    """
    print(f"  [WARNING] {Path(file_path).name} has {page_count} pages "
          f"(threshold: {LONG_PDF_PAGE_THRESHOLD}). MinerU may take 10-30+ minutes.")
    if yes:
        print("  [--yes] Proceeding automatically.")
        return True
    answer = input("  Process anyway? [y/N] ").strip().lower()
    return answer == "y"


def parse_file(input_path: str, output_dir: str = DEFAULT_OUTPUT, yes: bool = False) -> None:
    """Run MinerU on a single file and save results to output_dir.

    For PDF files exceeding LONG_PDF_PAGE_THRESHOLD pages, asks for confirmation
    unless yes=True.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Long-PDF check (PDF only)
    if Path(input_path).suffix.lower() == ".pdf":
        page_count = get_pdf_page_count(input_path)
        if page_count is not None and page_count > LONG_PDF_PAGE_THRESHOLD:
            if not confirm_long_pdf(input_path, page_count, yes):
                print(f"  [SKIP] {Path(input_path).name} (user cancelled)")
                return

    subprocess.run(
        ["conda", "run", "-n", "mineru", "mineru",
         "-p", input_path,
         "-o", output_dir,
         "-b", "pipeline",
         "-l", "en"],
        check=True
    )


def already_processed(file_path: str, output_dir: str) -> bool:
    """Return True if MinerU output folder for this file already exists and is non-empty."""
    stem = Path(file_path).stem
    out_folder = Path(output_dir) / stem
    return out_folder.is_dir() and any(out_folder.iterdir())


def process_folder(folder: str, output_dir: str = DEFAULT_OUTPUT, yes: bool = False) -> None:
    """Run MinerU on every supported file in a folder, skipping already-processed ones."""
    files = sorted(Path(folder).iterdir())
    supported = [f for f in files if f.suffix.lower() in SUPPORTED_EXTENSIONS]

    print(f"Found {len(supported)} supported file(s) in '{folder}'")
    print(f"Output:  {output_dir}")

    for f in supported:
        if f.name in SKIP_FILES:
            print(f"  [SKIP] {f.name}")
            continue
        if already_processed(str(f), output_dir):
            print(f"  [SKIP] {f.name} (already processed)")
            continue
        print(f"  [Processing] {f.name} ...")
        try:
            parse_file(str(f), output_dir, yes=yes)
            print(f"  [Done] {f.name}")
        except Exception as e:
            print(f"  [Error] {f.name}: {e}")


# Run from the command line:
#   single file:    python mineru_pdf.py path/to/file.pdf
#   whole folder:   python mineru_pdf.py path/to/folder/
#   custom output:  python mineru_pdf.py path/to/folder/ --output path/to/kepek/
#   skip prompts:   python mineru_pdf.py path/to/folder/ --yes
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run MinerU on a PDF file or a folder of PDFs."
    )
    parser.add_argument("input", help="PDF file or folder containing PDFs")
    parser.add_argument(
        "--output", "-o",
        default=DEFAULT_OUTPUT,
        help=f"Output directory (default: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help=f"Skip confirmation prompt for PDFs over {LONG_PDF_PAGE_THRESHOLD} pages"
    )
    args = parser.parse_args()

    target = Path(args.input)
    if not target.exists():
        sys.exit(f"[Error] Path not found: {target}")

    if target.is_dir():
        process_folder(str(target), args.output, yes=args.yes)
    else:
        parse_file(str(target), args.output, yes=args.yes)
