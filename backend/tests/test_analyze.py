import io
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

from app.main import app
from app.models.report_schema import DossierReport

client = TestClient(app)

SAMPLE_REPORT = DossierReport(
    report_meta={
        "company_name": "TestCo",
        "job_title": "Engineer",
        "generated_at": "2026-03-22T00:00:00Z",
        "version": "1.0",
    },
    role_summary="A test role summary.",
    hiring_priorities=["Priority 1", "Priority 2"],
    candidate_strengths=["Strength 1"],
    candidate_concerns=[
        {"concern": "Gap 1", "severity": "medium", "mitigation": "Mitigate it"}
    ],
    likely_interview_questions=[
        {"question": "Tell me about X?", "why_they_might_ask": "To assess X"}
    ],
    reverse_interview_questions=[
        {
            "audience": "Hiring Manager",
            "question": "How is success measured?",
            "why_it_matters": "Clarity on expectations",
        }
    ],
    positioning_strategy=["Lead with X"],
    red_flags_or_unknowns=["Vague scope"],
    prep_checklist=["Research the team"],
)


def _make_pdf_bytes():
    """Create a minimal valid PDF for testing."""
    import pymupdf

    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), "John Doe\nSoftware Engineer\n5 years experience")
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def test_analyze_missing_fields():
    """Test that missing required fields return 422."""
    response = client.post("/api/v1/analyze", data={})
    assert response.status_code == 422


def test_analyze_empty_company_name():
    pdf_bytes = _make_pdf_bytes()
    response = client.post(
        "/api/v1/analyze",
        data={
            "company_name": "  ",
            "job_title": "Engineer",
            "job_description": "Build things",
        },
        files={"resume_file": ("resume.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
    )
    assert response.status_code == 400


def test_analyze_wrong_file_type():
    response = client.post(
        "/api/v1/analyze",
        data={
            "company_name": "TestCo",
            "job_title": "Engineer",
            "job_description": "Build things",
        },
        files={"resume_file": ("resume.txt", io.BytesIO(b"hello"), "text/plain")},
    )
    assert response.status_code == 415


@patch("app.api.v1.routes.analyze.generate_dossier")
def test_analyze_success(mock_gen):
    """Test successful analysis with mocked AI."""
    mock_gen.return_value = SAMPLE_REPORT
    pdf_bytes = _make_pdf_bytes()

    response = client.post(
        "/api/v1/analyze",
        data={
            "company_name": "TestCo",
            "job_title": "Engineer",
            "job_description": "Build distributed systems",
        },
        files={"resume_file": ("resume.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "report" in data
    assert data["report"]["report_meta"]["company_name"] == "TestCo"
    assert len(data["report"]["hiring_priorities"]) > 0
