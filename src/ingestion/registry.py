"""Dispatch uploads to the right extractor by format."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from ingestion import markdown, pdf, text
from models import MaterialKind, SourceDocument

Loader = Callable[[Path], SourceDocument]

_LOADERS: dict[str, Loader] = {
    ".pdf": pdf.extract_pdf,
    ".txt": text.extract_text_file,
    ".md": markdown.extract_markdown_file,
    ".markdown": markdown.extract_markdown_file,
}


class UnsupportedFormatError(ValueError):
    """Raised when no extractor is registered for an upload type."""


def supported_extensions() -> list[str]:
    """Return the file extensions we can currently ingest."""
    return sorted(_LOADERS)


def extract_path(path: str | Path) -> SourceDocument:
    """Extract a source document from a file, choosing the loader by suffix."""
    path = Path(path)
    loader = _LOADERS.get(path.suffix.lower())
    if loader is None:
        supported = ", ".join(supported_extensions())
        raise UnsupportedFormatError(
            f"Unsupported format {path.suffix!r} for {path.name}. Supported: {supported}"
        )
    return loader(path)


def extract_text(
    content: str,
    *,
    name: str,
    kind: MaterialKind = MaterialKind.TEXT,
) -> SourceDocument:
    """Extract a source document from pasted text or Markdown."""
    if kind is MaterialKind.MARKDOWN:
        return markdown.extract_markdown(content, name=name)
    return text.extract_text(content, name=name)
