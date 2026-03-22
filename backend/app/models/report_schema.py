from pydantic import BaseModel


class ReportMeta(BaseModel):
    company_name: str
    job_title: str
    generated_at: str
    version: str = "1.0"


class InterviewQuestion(BaseModel):
    question: str
    why_they_might_ask: str


class ReverseQuestion(BaseModel):
    audience: str  # "Recruiter" | "Hiring Manager" | "Engineer"
    question: str
    why_it_matters: str


class CandidateConcern(BaseModel):
    concern: str
    severity: str  # "low" | "medium" | "high"
    mitigation: str


class DossierReport(BaseModel):
    report_meta: ReportMeta
    role_summary: str
    hiring_priorities: list[str]
    candidate_strengths: list[str]
    candidate_concerns: list[CandidateConcern]
    likely_interview_questions: list[InterviewQuestion]
    reverse_interview_questions: list[ReverseQuestion]
    positioning_strategy: list[str]
    red_flags_or_unknowns: list[str]
    prep_checklist: list[str]


class AnalyzeResponse(BaseModel):
    report: DossierReport


class ExportRequest(BaseModel):
    report: DossierReport


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
