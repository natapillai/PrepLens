"""ATS-style scoring schema for PrepLens.

Pass 1: LLM extracts requirements from JD and matches them against the resume.
Pass 2: Deterministic scoring calculates category and overall fit scores.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# --- Requirement extraction (LLM output from Pass 1) ---


class ExtractedRequirement(BaseModel):
    """A single requirement extracted from the job description."""

    keyword: str = Field(description="The skill, qualification, or attribute")
    category: str = Field(
        description="hard_skill | soft_skill | domain_knowledge | tool_or_technology | education"
    )
    importance: str = Field(
        description="required | preferred | nice_to_have"
    )
    source_quote: str = Field(
        description="The exact or near-exact phrase from the JD that implies this requirement"
    )


class ResumeMatch(BaseModel):
    """How a single requirement matches against the candidate's resume."""

    keyword: str
    match_level: str = Field(description="direct | partial | none")
    resume_evidence: str = Field(
        description="Summary of resume evidence supporting this match"
    )
    resume_quotes: list[str] = Field(
        default=[],
        description="Exact phrases from the resume that support the match",
    )
    match_reasoning: str = Field(
        description="Why this was classified as direct/partial/none, including synonym recognition"
    )


class CategoryWeight(BaseModel):
    """LLM-assigned weight for a requirement category, driven by JD emphasis."""

    category: str
    weight: float = Field(
        ge=0.0,
        le=1.0,
        description="Weight for this category (all weights should sum to 1.0)",
    )
    reasoning: str = Field(
        description="Why this weight was assigned based on JD emphasis"
    )


class ExtractionResult(BaseModel):
    """Full output of Pass 1: LLM extraction and matching."""

    requirements: list[ExtractedRequirement]
    matches: list[ResumeMatch]
    category_weights: list[CategoryWeight]


# --- Deterministic scoring (computed in Pass 2) ---

# Weight multipliers for importance levels
IMPORTANCE_WEIGHTS = {
    "required": 5.0,
    "preferred": 3.0,
    "nice_to_have": 1.0,
}

# Score multipliers for match levels
MATCH_MULTIPLIERS = {
    "direct": 1.0,
    "partial": 0.5,
    "none": 0.0,
}


class ScoredRequirement(BaseModel):
    """A requirement with its computed score and full traceability."""

    keyword: str
    category: str
    importance: str
    importance_weight: float
    match_level: str
    match_multiplier: float
    earned_points: float
    max_points: float
    resume_evidence: str
    match_reasoning: str


class CategoryScore(BaseModel):
    """Aggregated score for a single category."""

    category: str
    category_label: str  # Human-readable label
    earned_points: float
    max_points: float
    percentage: float = Field(ge=0.0, le=100.0)
    score_out_of_10: float = Field(ge=0.0, le=10.0)
    category_weight: float
    weighted_contribution: float  # How much this category contributes to overall
    requirements: list[ScoredRequirement]


class ScoreImprovement(BaseModel):
    """A suggested action that would increase the score."""

    keyword: str
    category: str
    current_match: str  # none | partial
    potential_points: float  # Points gained if upgraded to direct match
    percentage_impact: float  # How much the overall score would increase
    suggestion: str


class ConfidenceBreakdown(BaseModel):
    """Breakdown of confidence score factors."""

    jd_specificity: float = Field(ge=0.0, le=10.0)
    jd_specificity_reasoning: str
    resume_detail: float = Field(ge=0.0, le=10.0)
    resume_detail_reasoning: str
    match_clarity: float = Field(ge=0.0, le=10.0)
    match_clarity_reasoning: str
    overall_confidence: float = Field(ge=0.0, le=10.0)


class ScoringResult(BaseModel):
    """Complete scoring output with full transparency."""

    overall_fit_score: float = Field(ge=0.0, le=10.0)
    overall_fit_percentage: float = Field(ge=0.0, le=100.0)
    total_earned_points: float
    total_max_points: float
    confidence: ConfidenceBreakdown
    category_scores: list[CategoryScore]
    scored_requirements: list[ScoredRequirement]
    top_improvements: list[ScoreImprovement]


# --- Category display labels ---

CATEGORY_LABELS = {
    "hard_skill": "Hard Skills",
    "soft_skill": "Soft Skills",
    "domain_knowledge": "Domain Knowledge",
    "tool_or_technology": "Tools & Technologies",
    "education": "Education & Certifications",
}
