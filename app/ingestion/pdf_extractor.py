"""Extracts raw text from an uploaded PDF."""

from pypdf import PdfReader


def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text_parts = []
    for page in reader.pages:
        text_parts.append(page.extract_text())
    return "\n".join(text_parts)


if __name__ == "__main__":
    text = extract_text("data/sample.pdf")
    print(f"Extracted {len(text)} characters")
    print(text[:500])
