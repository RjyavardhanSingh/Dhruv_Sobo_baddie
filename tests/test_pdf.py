from pathlib import Path

import pytest

from ingestion.pdf import extract_pdf
from models import MaterialKind

# Resolve PDF path relative to this file, not CWD
PDF_PATH = Path(__file__).parent.parent / "data" / "test_biology.pdf"


def test_extract_pdf_basic():
    document = extract_pdf(PDF_PATH)

    assert document.name == "test_biology.pdf"
    assert document.kind is MaterialKind.PDF
    assert document.page_count == 3
    assert len(document.pages) == 3
    assert all(page.text for page in document.pages)


def test_extract_pdf_page_numbers():
    document = extract_pdf(PDF_PATH)

    for i, page in enumerate(document.pages, start=1):
        assert page.page_number == i


def test_extract_pdf_content():
    document = extract_pdf(PDF_PATH)

    # Page 1 contains intro
    assert "Introduction to Biology" in document.pages[0].text
    assert "Cells are the basic structural" in document.pages[0].text

    # Page 2 contains cell
    assert "The Cell" in document.pages[1].text

    # Page 3 contains photosynthesis
    assert "Photosynthesis" in document.pages[2].text

    # full_text property joins pages
    assert "Biology is the scientific study" in document.full_text
    assert document.word_count > 100


def test_extract_pdf_accepts_string_path():
    document = extract_pdf(str(PDF_PATH))
    assert document.page_count == 3


def test_extract_pdf_file_not_found():
    with pytest.raises(FileNotFoundError, match="PDF not found"):
        extract_pdf(Path("/tmp/nonexistent.pdf"))


def test_extract_pdf_not_a_pdf():
    with pytest.raises(ValueError, match="Expected a PDF file"):
        extract_pdf(Path(__file__))  # .py is not .pdf
