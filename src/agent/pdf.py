from pathlib import Path

import pymupdf
from pydantic import BaseModel


class PDFPage(BaseModel):
    page_number: int
    text: str


class PDFDocument(BaseModel):
    file_path: str
    page_count: int
    pages: list[PDFPage]

    @property
    def full_text(self) -> str:
        return "\n\n".join(page.text for page in self.pages if page.text.strip())


def extract_pdf(path: str | Path) -> PDFDocument:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file, got: {path.suffix}")

    pages: list[PDFPage] = []

    with pymupdf.open(path) as document:
        for index, page in enumerate(document):
            text = page.get_text("text").strip()
            pages.append(PDFPage(page_number=index + 1, text=text))

        page_count = len(document)

    return PDFDocument(
        file_path=path.name,
        page_count=page_count,
        pages=pages,
    )
