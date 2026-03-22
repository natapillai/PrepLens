import pytest
from pydantic import ValidationError

from app.models.report_schema import PrepLensReportV2
from tests.sample_v2 import SAMPLE_REPORT_V2


def test_v2_schema_validates():
    """Test that the sample V2 report validates successfully."""
    report = PrepLensReportV2.model_validate(SAMPLE_REPORT_V2)
    assert report.schema_version == "2.0"
    assert report.input_summary.company_name == "TestCo"
    assert report.pursuit_recommendation.overall_fit_score == 7
    assert len(report.hiring_priorities) == 2
    assert len(report.likely_interview_questions) == 2
    assert len(report.prep_checklist) == 3


def test_v2_schema_rejects_invalid():
    """Test that invalid data raises ValidationError."""
    with pytest.raises(ValidationError):
        PrepLensReportV2.model_validate({"invalid": True})


def test_v2_fit_score_range():
    """Test that fit score validation enforces 0-10 range."""
    data = dict(SAMPLE_REPORT_V2)
    data["pursuit_recommendation"] = dict(data["pursuit_recommendation"])
    data["pursuit_recommendation"]["overall_fit_score"] = 15
    with pytest.raises(ValidationError):
        PrepLensReportV2.model_validate(data)


def test_v2_importance_score_range():
    """Test that importance score validation enforces 1-5 range."""
    data = dict(SAMPLE_REPORT_V2)
    data["hiring_priorities"] = [
        {"priority": "Test", "why_it_matters": "Test", "importance_score": 10}
    ]
    with pytest.raises(ValidationError):
        PrepLensReportV2.model_validate(data)


def test_v2_roundtrip():
    """Test that model_dump produces valid JSON and can be re-validated."""
    report = PrepLensReportV2.model_validate(SAMPLE_REPORT_V2)
    dumped = report.model_dump()
    re_validated = PrepLensReportV2.model_validate(dumped)
    assert re_validated.schema_version == report.schema_version
    assert re_validated.pursuit_recommendation.overall_fit_score == report.pursuit_recommendation.overall_fit_score
