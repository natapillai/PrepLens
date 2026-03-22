from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

SAMPLE_REPORT_JSON = {
    "report": {
        "report_meta": {
            "company_name": "TestCo",
            "job_title": "Engineer",
            "generated_at": "2026-03-22T00:00:00Z",
            "version": "1.0",
        },
        "role_summary": "A test role.",
        "hiring_priorities": ["Priority 1"],
        "candidate_strengths": ["Strength 1"],
        "candidate_concerns": [
            {"concern": "Gap", "severity": "low", "mitigation": "Fix"}
        ],
        "likely_interview_questions": [
            {"question": "Q?", "why_they_might_ask": "Because"}
        ],
        "reverse_interview_questions": [
            {"audience": "Recruiter", "question": "RQ?", "why_it_matters": "Signal"}
        ],
        "positioning_strategy": ["Strategy"],
        "red_flags_or_unknowns": ["Flag"],
        "prep_checklist": ["Check"],
    }
}


def test_export_docx():
    response = client.post("/api/v1/export/docx", json=SAMPLE_REPORT_JSON)
    assert response.status_code == 200
    assert "wordprocessingml" in response.headers["content-type"]
    assert len(response.content) > 1000


def test_export_pdf():
    response = client.post("/api/v1/export/pdf", json=SAMPLE_REPORT_JSON)
    assert response.status_code == 200
    assert "pdf" in response.headers["content-type"]
    assert response.content[:5] == b"%PDF-"


def test_export_invalid_schema():
    response = client.post("/api/v1/export/pdf", json={"report": {"invalid": True}})
    assert response.status_code == 422
