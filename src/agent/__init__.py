"""Self Learning Platform agent package."""

from agent.pdf import PDFDocument, PDFPage, extract_pdf

__all__ = ["PDFDocument", "PDFPage", "extract_pdf", "main"]


def main() -> None:
    print("Hello from agent!")
