from pathlib import Path

from agent.pdf import extract_pdf


pdf_path = Path("data/test_biology.pdf")

document = extract_pdf(pdf_path)

print("=" * 80)
print("EXTRACTED PDF")
print("=" * 80)

print(f"File: {document.file_path}")
print(f"Pages: {document.page_count}")

for page in document.pages:
    print(f"\n{'=' * 80}")
    print(f"PAGE {page.page_number}")
    print(f"{'=' * 80}")
    print(page.text[:2000])