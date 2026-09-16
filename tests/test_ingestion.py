import pytest

from ingestion import UnsupportedFormatError, extract_path, supported_extensions
from ingestion.markdown import extract_markdown, split_sections
from ingestion.text import extract_text, extract_text_file
from models import MaterialKind


def test_supported_extensions():
    assert supported_extensions() == [".markdown", ".md", ".pdf", ".txt"]


def test_extract_path_unknown_format(tmp_path):
    bad = tmp_path / "notes.docx"
    bad.write_text("hello")

    with pytest.raises(UnsupportedFormatError, match="Unsupported format"):
        extract_path(bad)


def test_extract_text_single_page():
    document = extract_text("Cells are the basic unit of life.")

    assert document.kind is MaterialKind.TEXT
    assert document.page_count == 1
    assert document.full_text == "Cells are the basic unit of life."


def test_extract_text_file(tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("Photosynthesis converts light into energy.")

    document = extract_text_file(path)

    assert document.name == "notes.txt"
    assert document.page_count == 1


def test_extract_text_file_missing():
    with pytest.raises(FileNotFoundError):
        extract_text_file("/tmp/does-not-exist.txt")


def test_split_sections_by_heading():
    content = "# Intro\n\nHello\n\n## Details\n\nMore text"

    sections = split_sections(content)

    assert len(sections) == 2
    assert sections[0].startswith("# Intro")
    assert sections[1].startswith("## Details")


def test_split_sections_keeps_preamble():
    content = "Preamble line\n\n# Heading\n\nBody"

    sections = split_sections(content)

    assert sections[0] == "Preamble line"
    assert sections[1].startswith("# Heading")


def test_split_sections_without_headings():
    assert split_sections("just some text") == ["just some text"]


def test_extract_markdown_sections():
    document = extract_markdown("# A\n\none\n\n# B\n\ntwo")

    assert document.kind is MaterialKind.MARKDOWN
    assert document.page_count == 2
    assert document.pages[0].page_number == 1
    assert "one" in document.pages[0].text
