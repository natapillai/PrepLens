from __future__ import annotations

from pydantic import BaseModel, Field


# --- Shared enums as Literal types ---


# --- Nested models ---


class InputSummary(BaseModel):
    company_name: str
    job_title: str
    job_posting_url: str | None = None
    resume_filename: str | None = None
    candidate_notes_present: bool = False
    job_description_present: bool = True
    job_description_length: int = 0


class ExecutiveSummary(BaseModel):
    headline: str
    summary: str
    top_takeaways: list[str]


class PursuitRecommendation(BaseModel):
    overall_fit_score: float = Field(ge=0, le=10)
    confidence_score: float = Field(ge=0, le=10)
    recommendation: str  # pursue | pursue_selectively | low_priority | insufficient_information
    reasoning: list[str]
    ideal_candidate_profile: str
    candidate_outlook: str


class CompanySnapshot(BaseModel):
    company_overview: str
    business_model: str | None = None
    product_focus: str | None = None
    engineering_signals: list[str] = []
    company_stage: str = "unknown"  # startup | growth | enterprise | public | unknown
    risk_level: str = "unknown"  # low | medium | high | unknown
    notable_unknowns: list[str] = []


class RoleSnapshot(BaseModel):
    role_summary: str
    seniority_signal: str = "unknown"  # junior | mid | senior | staff | unknown
    core_domain: list[str] = []
    primary_stack_signals: list[str] = []
    success_profile: str = ""


class HiringPriority(BaseModel):
    priority: str
    why_it_matters: str
    importance_score: int = Field(ge=1, le=5)


class FitSignal(BaseModel):
    signal: str
    evidence: str
    strength_score: int = Field(ge=1, le=10)


class WeakSignal(BaseModel):
    signal: str
    why_it_matters: str
    gap_severity: str  # low | medium | high


class FitAnalysis(BaseModel):
    strong_fit_signals: list[FitSignal] = []
    partial_fit_signals: list[FitSignal] = []
    missing_or_weak_signals: list[WeakSignal] = []


class ConcernItem(BaseModel):
    concern: str
    why_they_may_care: str
    severity: str  # low | medium | high
    mitigation_strategy: str
    best_proof_to_use: str
    sample_response: str


class ResumePriorityEdit(BaseModel):
    type: str  # bullet_rewrite | keyword_addition | reorder_section | project_highlight | summary_adjustment
    target: str
    recommendation: str
    why: str


class BulletToEmphasize(BaseModel):
    experience_area: str
    why: str


class ResumeTailoring(BaseModel):
    resume_verdict: str  # good_to_apply | tailor_before_applying | needs_significant_rewrite
    priority_edits: list[ResumePriorityEdit] = []
    missing_keywords: list[str] = []
    bullets_to_emphasize: list[BulletToEmphasize] = []
    positioning_angle: str = ""


class ApplicationStrategy(BaseModel):
    apply_now: bool = True
    referral_recommended: bool = False
    best_outreach_target: str = "none"  # recruiter | hiring_manager | engineer | alumni | none
    outreach_angle: str = ""
    suggested_connection_note: str = ""
    suggested_email_angle: str = ""


class RecruiterQuestion(BaseModel):
    question: str
    intent: str
    suggested_answer_points: list[str] = []


class RecruiterScreenPrep(BaseModel):
    what_they_will_likely_screen_for: list[str] = []
    likely_recruiter_questions: list[RecruiterQuestion] = []
    work_auth_notes: str | None = None
    compensation_notes: str | None = None
    availability_notes: str | None = None


class StoryBankItem(BaseModel):
    story_title: str
    best_for_questions: list[str] = []
    recommended_experience: str
    angle_to_emphasize: str
    key_metrics_or_outcomes: list[str] = []
    likely_follow_up_questions: list[str] = []


class InterviewRound(BaseModel):
    round_name: str  # recruiter_screen | hiring_manager | technical | behavioral | final_round
    round_goal: str
    what_they_will_likely_probe: list[str] = []
    best_stories_to_prepare: list[str] = []
    candidate_focus: list[str] = []


class InterviewQuestion(BaseModel):
    question: str
    category: str  # technical | behavioral | system_design | role_fit | company_fit
    why_they_may_ask: str
    best_story_or_topic: str = ""


class ReverseInterviewQuestion(BaseModel):
    target_interviewer: str  # recruiter | hiring_manager | engineer | panel | final_round
    question: str
    why_ask_this: str
    good_answer_signals: list[str] = []
    bad_answer_signals: list[str] = []
    follow_up_question: str | None = None


class LogisticsAndConstraints(BaseModel):
    work_model: str = "unknown"  # remote | hybrid | onsite | unknown
    location_notes: str | None = None
    visa_or_work_auth_signal: str | None = None
    level_clarity: str = "unknown"  # clear | unclear | unknown
    compensation_signal: str | None = None
    timeline_signal: str | None = None


class RedFlag(BaseModel):
    flag: str
    severity: str  # low | medium | high
    why_it_matters: str


class RedFlagsAndUnknowns(BaseModel):
    red_flags: list[RedFlag] = []
    unknowns_to_verify: list[str] = []


class ImmediateNextAction(BaseModel):
    priority: int
    action: str
    why: str
    time_estimate_minutes: int = 0


class PrepChecklistItem(BaseModel):
    item: str
    completed: bool = False


class ExportMetadata(BaseModel):
    export_title: str = ""
    export_subtitle: str = ""
    export_date: str = ""
    branding: str = "PrepLens"


# --- Top-level report ---


class PrepLensReportV2(BaseModel):
    schema_version: str = "2.0"
    generated_at: str = ""
    report_id: str = ""
    product_name: str = "PrepLens"
    input_summary: InputSummary
    executive_summary: ExecutiveSummary
    pursuit_recommendation: PursuitRecommendation
    company_snapshot: CompanySnapshot
    role_snapshot: RoleSnapshot
    hiring_priorities: list[HiringPriority] = []
    fit_analysis: FitAnalysis
    concerns_and_mitigation: list[ConcernItem] = []
    resume_tailoring: ResumeTailoring
    application_strategy: ApplicationStrategy
    recruiter_screen_prep: RecruiterScreenPrep
    story_bank: list[StoryBankItem] = []
    interview_rounds: list[InterviewRound] = []
    likely_interview_questions: list[InterviewQuestion] = []
    reverse_interview_questions: list[ReverseInterviewQuestion] = []
    logistics_and_constraints: LogisticsAndConstraints = LogisticsAndConstraints()
    red_flags_and_unknowns: RedFlagsAndUnknowns = RedFlagsAndUnknowns()
    immediate_next_actions: list[ImmediateNextAction] = []
    prep_checklist: list[PrepChecklistItem] = []
    export_metadata: ExportMetadata = ExportMetadata()

    # ATS-style scoring breakdown (populated by scoring service)
    scoring: dict | None = None


# --- API wrappers ---


class AnalyzeResponse(BaseModel):
    report: PrepLensReportV2


class ExportRequest(BaseModel):
    report: PrepLensReportV2


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
