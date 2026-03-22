from fastapi.testclient import TestClient

from app.main import app
from tests.sample_v2 import SAMPLE_REPORT_V2

client = TestClient(app)


def test_export_docx():
    response = client.post("/api/v1/export/docx", json={"report": SAMPLE_REPORT_V2})
    assert response.status_code == 200
    assert "wordprocessingml" in response.headers["content-type"]
    assert len(response.content) > 1000


def test_export_pdf():
    response = client.post("/api/v1/export/pdf", json={"report": SAMPLE_REPORT_V2})
    assert response.status_code == 200
    assert "pdf" in response.headers["content-type"]
    assert response.content[:5] == b"%PDF-"


def test_export_invalid_schema():
    response = client.post("/api/v1/export/pdf", json={"report": {"invalid": True}})
    assert response.status_code == 422
