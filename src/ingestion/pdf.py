"""Extract normalized text from PDF uploads."""

from __future__ import annotations

from pathlib import Path

import pymupdf

from models import MaterialKind, SourceDocument, SourcePage, build_source_document


def extract_pdf(path: str | Path) -> SourceDocument:
    """Read a PDF file and return one page per PDF page."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file, got: {path.suffix}")

    pages: list[SourcePage] = []

    with pymupdf.open(path) as document:
        for index, page in enumerate(document):
            text = page.get_text("text").strip()
            pages.append(SourcePage(page_number=index + 1, text=text))

    return build_source_document(name=path.name, kind=MaterialKind.PDF, pages=pages)
