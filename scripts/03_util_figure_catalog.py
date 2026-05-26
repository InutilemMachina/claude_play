#!/usr/bin/env python3
"""
Build figure_catalog.json from MinerU *_content_list.json files.

Usage:
    python 03_03_util_figure_catalog.py <2_clean_inputs_dir> [options]

Options:
    --output / -o   Output path for figure_catalog.json
    --vlm           Enable VLM captioning via Claude vision API (claude-sonnet-4-6).
                    Requires ANTHROPIC_API_KEY env variable.

Examples:
    # Build catalog only (no VLM)
    python 03_03_util_figure_catalog.py test_outputs/Termografia/1_het/2_clean_inputs/

    # Build + VLM captioning in one step
    python 03_03_util_figure_catalog.py test_outputs/Termografia/1_het/2_clean_inputs/ --vlm

    # VLM on existing catalog (re-run to fill empty keywords)
    python 03_03_util_figure_catalog.py test_outputs/Termografia/1_het/2_clean_inputs/ --vlm --output existing.json

Output schema per entry:
    key  : "{source_stem}-{type}-{n}-p{page}"
    value: {
        "source":   "yeh2016_paper.pdf",
        "page":     3,                          # 1-based
        "type":     "image",                    # image | table | chart
        "caption":  "...",                      # VLM caption if --vlm, else MinerU caption
        "path":     "2_clean_inputs/yeh2016_paper/auto/images/abc123.jpg",
        "keywords": ["infrared", "thermal"],    # VLM keywords if --vlm, else []
        "vlm_done": true                        # set to true after VLM run
    }
"""

import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path

INCLUDE_TYPES = {"image", "table", "chart"}

# ---- VLM captioning ----

VLM_MODEL = "claude-sonnet-4-6"
VLM_MAX_TOKENS = 512

VLM_PROMPT = """\
Tekintsd meg a képet és válaszolj a következő formátumban (semmi mást ne írj):
CAPTION: <1-2 mondatos magyar leírás a kép műszaki/tudományos tartalmáról>
KEYWORDS: <3-5 angol kulcsszó vesszővel elválasztva, pl. thermal camera, emissivity, Stefan-Boltzmann>

A kulcsszavak legyenek: fizikai jelenségek, mért mennyiségek, eszközök, módszerek nevei.
"""


def vlm_caption_and_keywords(
    image_path: Path,
    client,
) -> tuple[str, list[str]]:
    """
    Send image to Claude vision API.
    Returns (caption_str, keywords_list).
    Falls back to ("", []) on any error.
    """
    if not image_path.exists():
        print(f"    [VLM] Image not found, skip: {image_path}")
        return "", []

    suffix = image_path.suffix.lower()
    media_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                 ".png": "image/png", ".webp": "image/webp"}
    media_type = media_map.get(suffix, "image/jpeg")

    image_data = base64.standard_b64encode(image_path.read_bytes()).decode("utf-8")

    try:
        response = client.messages.create(
            model=VLM_MODEL,
            max_tokens=VLM_MAX_TOKENS,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image",
                         "source": {"type": "base64",
                                    "media_type": media_type,
                                    "data": image_data}},
                        {"type": "text", "text": VLM_PROMPT},
                    ],
                }
            ],
        )
    except Exception as e:
        print(f"    [VLM] API error: {e}")
        return "", []

    raw = response.content[0].text.strip()

    # Parse CAPTION and KEYWORDS lines
    caption = ""
    keywords: list[str] = []

    for line in raw.splitlines():
        if line.startswith("CAPTION:"):
            caption = line[len("CAPTION:"):].strip()
        elif line.startswith("KEYWORDS:"):
            kw_str = line[len("KEYWORDS:"):].strip()
            keywords = [k.strip() for k in kw_str.split(",") if k.strip()]

    return caption, keywords


def run_vlm_on_catalog(
    catalog: dict,
    2_clean_inputs_dir: Path,
    client,
) -> int:
    """
    Iterate catalog entries where vlm_done is not True.
    Call VLM for each image; update caption (if empty) and keywords in-place.
    Returns count of entries processed.
    """
    processed = 0
    week_dir = 2_clean_inputs_dir.parent  # e.g. 1_het/

    for key, entry in catalog.items():
        if entry.get("vlm_done"):
            continue

        img_path = week_dir / entry["path"]
        print(f"  [VLM] {key} -> {img_path.name}")

        caption, keywords = vlm_caption_and_keywords(img_path, client)

        if caption and not entry.get("caption"):
            entry["caption"] = caption
        if keywords:
            entry["keywords"] = keywords
        entry["vlm_done"] = True
        processed += 1

    return processed


def build_catalog(kepek_dir: Path) -> dict:
    """Traverse kepek_dir for *_content_list.json files and build a unified catalog."""
    catalog: dict = {}

    cl_files = sorted(kepek_dir.rglob("*_content_list.json"))
    if not cl_files:
        print(f"[Warning] No *_content_list.json files found under: {kepek_dir}")
        return catalog

    for cl_file in cl_files:
        # MinerU output: kepek/SOURCE/auto/SOURCE_content_list.json
        # cl_file.parent is the auto/ dir; .parent.parent is the SOURCE dir
        auto_dir    = cl_file.parent
        source_dir  = auto_dir.parent
        source_stem = source_dir.name              # e.g. "yeh2016_paper"
        source_pdf  = source_stem + ".pdf"

        try:
            items = json.loads(cl_file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  [Error] Cannot read {cl_file}: {e}")
            continue

        type_counters: dict[str, int] = {}
        added = 0

        for item in items:
            ctype = item.get("type")
            if ctype not in INCLUDE_TYPES:
                continue

            img_rel = item.get("img_path", "")
            if not img_rel:
                continue

            page = item.get("page_idx", 0) + 1      # convert to 1-based

            type_counters[ctype] = type_counters.get(ctype, 0) + 1
            n = type_counters[ctype]
            # Keep original filename (MinerU uses content-hash names)
            orig_name = Path(img_rel).name   # e.g. "abc123.jpg"

            # Relative path from the subject week folder root
            # MinerU writes to 2_clean_inputs/SOURCE/auto/images/
            rel_path = f"2_clean_inputs/{source_stem}/auto/images/{orig_name}"

            # Caption: prefer dedicated caption fields, fall back to inline text
            caption_list = (
                item.get("image_caption")
                or item.get("table_caption")
                or item.get("chart_caption")
                or []
            )
            if caption_list:
                caption = caption_list[0].strip()[:200]
            else:
                caption = item.get("text", "").strip()[:200]

            key = f"{source_stem}-{ctype}-{n}-p{page}"
            catalog[key] = {
                "source":   source_pdf,
                "page":     page,
                "type":     ctype,
                "caption":  caption,
                "path":     rel_path,
                "keywords": [],      # populated later by 05b_figure_mapper
            }
            added += 1

        print(f"  {source_stem}: {added} entries")

    return catalog


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build figure_catalog.json from MinerU content_list files."
    )
    parser.add_argument(
        "kepek_dir",
        help="2_clean_inputs/ directory (contains per-source subfolders with auto/)"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output path for figure_catalog.json (default: <kepek_dir>/../figure_catalog.json)"
    )
    parser.add_argument(
        "--vlm",
        action="store_true",
        help="Enable VLM captioning via Claude vision API (requires ANTHROPIC_API_KEY)"
    )
    args = parser.parse_args()

    kepek_dir = Path(args.kepek_dir)
    if not kepek_dir.is_dir():
        sys.exit(f"[Error] Directory not found: {kepek_dir}")

    # Default output: <week_dir>/3_raw_outputs/figure_catalog.json
    out_path = Path(args.output) if args.output else kepek_dir.parent / "3_raw_outputs" / "figure_catalog.json"

    # --- Step 1: Build catalog from MinerU content_list files ---
    if out_path.exists():
        print(f"Loading existing catalog: {out_path}")
        catalog = json.loads(out_path.read_text(encoding="utf-8"))
        print(f"  {len(catalog)} entries loaded.")
    else:
        print(f"Building figure catalog from: {kepek_dir}")
        catalog = build_catalog(kepek_dir)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(catalog, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"Wrote {len(catalog)} entries -> {out_path}")

    # --- Step 2 (optional): VLM captioning ---
    if args.vlm:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            sys.exit("[Error] --vlm requires ANTHROPIC_API_KEY environment variable.")

        try:
            import anthropic
        except ImportError:
            sys.exit("[Error] anthropic package not installed. Run: pip install anthropic")

        client = anthropic.Anthropic(api_key=api_key)
        pending = sum(1 for e in catalog.values() if not e.get("vlm_done"))
        print(f"\n[VLM] {pending} entries to process (vlm_done=False)...")

        processed = run_vlm_on_catalog(catalog, kepek_dir, client)

        # Save after every batch (overwrite in-place)
        out_path.write_text(
            json.dumps(catalog, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"\n[VLM] Done: {processed} entries processed -> {out_path}")


if __name__ == "__main__":
    main()
