import re

import pymupdf


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract and normalize text from a PDF file."""
    doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()

    raw_text = "\n".join(pages)
    if not raw_text.strip():
        raise ValueError("Could not extract text from the PDF. The file may be scanned or image-based.")

    # Normalize whitespace
    text = re.sub(r"[ \t]+", " ", raw_text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
