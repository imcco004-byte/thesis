#!/usr/bin/env python3
"""Convert PDFs to Markdown with PyMuPDF4LLM."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pymupdf4llm


DEFAULT_SOURCE = Path("Paper_reference")
DEFAULT_OUTPUT_DIR = Path("Paper_reference_markdown")


def _iter_pdfs(source: Path, pattern: str) -> list[Path]:
    if source.is_file():
        if source.suffix.lower() != ".pdf":
            raise ValueError(f"expected a .pdf file, got {source}")
        return [source]
    if not source.is_dir():
        raise ValueError(f"source does not exist: {source}")
    return sorted(path for path in source.glob(pattern) if path.is_file())


def _convert_pdf(
    pdf_path: Path,
    output_dir: Path,
    *,
    overwrite: bool,
    include_headers: bool,
    include_footers: bool,
    force_ocr: bool,
    use_ocr: bool,
) -> tuple[Path, bool]:
    output_path = output_dir / f"{pdf_path.stem}.md"
    if output_path.exists() and not overwrite:
        return output_path, False

    markdown = pymupdf4llm.to_markdown(
        str(pdf_path),
        header=include_headers,
        footer=include_footers,
        force_ocr=force_ocr,
        use_ocr=use_ocr,
    )
    output_path.write_text(markdown, encoding="utf-8")
    return output_path, True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert one PDF or a directory of PDFs to Markdown.",
    )
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=DEFAULT_SOURCE,
        help="PDF file or directory of PDFs (default: Paper_reference)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated Markdown files (default: Paper_reference_markdown)",
    )
    parser.add_argument(
        "-g",
        "--glob",
        default="*.pdf",
        help="Glob to use when source is a directory (default: *.pdf)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing Markdown outputs.",
    )
    parser.add_argument(
        "--keep-headers",
        action="store_true",
        help="Keep detected page headers in the output.",
    )
    parser.add_argument(
        "--keep-footers",
        action="store_true",
        help="Keep detected page footers in the output.",
    )
    ocr_group = parser.add_mutually_exclusive_group()
    ocr_group.add_argument(
        "--force-ocr",
        action="store_true",
        help="Force OCR even when native text exists.",
    )
    ocr_group.add_argument(
        "--no-ocr",
        action="store_true",
        help="Disable OCR entirely.",
    )
    args = parser.parse_args()

    try:
        pdf_paths = _iter_pdfs(args.source, args.glob)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    if not pdf_paths:
        print("Error: no PDF files matched the requested source.", file=sys.stderr)
        raise SystemExit(1)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    converted = 0
    skipped = 0
    for pdf_path in pdf_paths:
        output_path, wrote_file = _convert_pdf(
            pdf_path,
            args.output_dir,
            overwrite=args.overwrite,
            include_headers=args.keep_headers,
            include_footers=args.keep_footers,
            force_ocr=args.force_ocr,
            use_ocr=not args.no_ocr,
        )
        if wrote_file:
            converted += 1
            print(f"converted: {pdf_path} -> {output_path}")
        else:
            skipped += 1
            print(f"skipped: {output_path} already exists")

    print(
        f"done: {converted} converted, {skipped} skipped, {len(pdf_paths)} total"
    )


if __name__ == "__main__":
    main()