"""Turn raw uploads into normalized source documents."""

from ingestion.registry import (
    UnsupportedFormatError,
    extract_path,
    extract_text,
    supported_extensions,
)

__all__ = [
    "UnsupportedFormatError",
    "extract_path",
    "extract_text",
    "supported_extensions",
]
