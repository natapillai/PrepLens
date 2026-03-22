import pytest
import pymupdf

from app.services.resume_parser import extract_text_from_pdf


def _make_pdf(text: str) -> bytes:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def test_extract_text_success():
    pdf_bytes = _make_pdf("John Doe\nSoftware Engineer")
    text = extract_text_from_pdf(pdf_bytes)
    assert "John Doe" in text
    assert "Software Engineer" in text


def test_extract_empty_pdf():
    # Create a PDF with no text content
    doc = pymupdf.open()
    doc.new_page()
    pdf_bytes = doc.tobytes()
    doc.close()

    with pytest.raises(ValueError, match="Could not extract text"):
        extract_text_from_pdf(pdf_bytes)


def test_extract_normalizes_whitespace():
    pdf_bytes = _make_pdf("Hello    World\n\n\n\n\nTest")
    text = extract_text_from_pdf(pdf_bytes)
    assert "Hello World" in text
    # Should not have more than 2 consecutive newlines
    assert "\n\n\n" not in text
