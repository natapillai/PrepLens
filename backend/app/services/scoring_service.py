"""ATS-style scoring service.

Pass 1: LLM extracts requirements from JD and matches against resume.
Pass 2: Deterministic scoring engine computes category and overall scores.
"""

import json
import logging
from collections import defaultdict

from openai import AsyncOpenAI

from app.core.config import settings
from app.models.scoring_schema import (
    CATEGORY_LABELS,
    IMPORTANCE_WEIGHTS,
    MATCH_MULTIPLIERS,
    CategoryScore,
    CategoryWeight,
    ConfidenceBreakdown,
    ExtractionResult,
    ScoreImprovement,
    ScoredRequirement,
    ScoringResult,
)
from app.prompts.scoring_prompt import (
    CONFIDENCE_SYSTEM_PROMPT,
    SCORING_SYSTEM_PROMPT,
    build_confidence_prompt,
    build_scoring_prompt,
)

logger = logging.getLogger(__name__)


async def _extract_requirements(
    client: AsyncOpenAI,
    job_description: str,
    resume_text: str,
) -> ExtractionResult:
    """Pass 1: LLM extracts JD requirements and matches them to the resume."""

    user_prompt = build_scoring_prompt(job_description, resume_text)

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SCORING_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,  # Very low temp for consistent, conservative extraction
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    if not raw:
        raise ValueError("Empty response from scoring extraction")

    data = json.loads(raw)
    return ExtractionResult.model_validate(data)


async def _compute_confidence(
    client: AsyncOpenAI,
    job_description: str,
    resume_text: str,
    scored_reqs: list[ScoredRequirement],
) -> ConfidenceBreakdown:
    """Compute confidence score based on input quality."""

    direct = sum(1 for r in scored_reqs if r.match_level == "direct")
    partial = sum(1 for r in scored_reqs if r.match_level == "partial")
    none_ = sum(1 for r in scored_reqs if r.match_level == "none")

    user_prompt = build_confidence_prompt(
        job_description=job_description,
        resume_text=resume_text,
        total_requirements=len(scored_reqs),
        direct_matches=direct,
        partial_matches=partial,
        no_matches=none_,
    )

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": CONFIDENCE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    if not raw:
        raise ValueError("Empty response from confidence evaluation")

    data = json.loads(raw)

    # Compute overall confidence as average of the three factors
    jd = float(data["jd_specificity"])
    resume = float(data["resume_detail"])
    clarity = float(data["match_clarity"])
    overall = round((jd + resume + clarity) / 3, 1)

    return ConfidenceBreakdown(
        jd_specificity=jd,
        jd_specificity_reasoning=data["jd_specificity_reasoning"],
        resume_detail=resume,
        resume_detail_reasoning=data["resume_detail_reasoning"],
        match_clarity=clarity,
        match_clarity_reasoning=data["match_clarity_reasoning"],
        overall_confidence=overall,
    )


def _normalize_category_weights(
    extraction: ExtractionResult,
) -> list[CategoryWeight]:
    """Deterministically compute category weights from requirement distribution.

    Instead of using LLM-assigned weights (which vary per run), we derive
    weights from the importance-weighted point share of each category.
    This ensures identical extractions always produce identical weights.
    """
    # Compute total importance-weighted points per category
    cat_points: dict[str, float] = defaultdict(float)
    for req in extraction.requirements:
        cat_points[req.category] += IMPORTANCE_WEIGHTS.get(req.importance, 3.0)

    total = sum(cat_points.values())
    if total == 0:
        # Fallback: equal weights
        n = len(cat_points) or 1
        return [
            CategoryWeight(category=c, weight=round(1.0 / n, 3), reasoning="equal fallback")
            for c in cat_points
        ]

    # Derive weights proportional to each category's importance-weighted share
    return [
        CategoryWeight(
            category=cat,
            weight=round(pts / total, 3),
            reasoning=f"Derived from requirement distribution: {pts:.1f}/{total:.1f} importance-weighted points",
        )
        for cat, pts in cat_points.items()
    ]


def _score_requirements(
    extraction: ExtractionResult,
) -> list[ScoredRequirement]:
    """Deterministically score each requirement based on extraction results."""

    # Build a lookup from keyword -> match
    match_lookup = {m.keyword: m for m in extraction.matches}

    scored = []
    for req in extraction.requirements:
        match = match_lookup.get(req.keyword)
        importance_weight = IMPORTANCE_WEIGHTS.get(req.importance, 3.0)
        match_level = match.match_level if match else "none"
        match_mult = MATCH_MULTIPLIERS.get(match_level, 0.0)

        max_points = importance_weight
        earned_points = importance_weight * match_mult

        scored.append(
            ScoredRequirement(
                keyword=req.keyword,
                category=req.category,
                importance=req.importance,
                importance_weight=importance_weight,
                match_level=match_level,
                match_multiplier=match_mult,
                earned_points=round(earned_points, 2),
                max_points=max_points,
                resume_evidence=match.resume_evidence if match else "No evidence found",
                match_reasoning=match.match_reasoning if match else "No matching entry from analysis",
            )
        )

    return scored


def _compute_category_scores(
    scored_reqs: list[ScoredRequirement],
    category_weights: list[CategoryWeight],
) -> list[CategoryScore]:
    """Aggregate scores by category."""

    weight_lookup = {cw.category: cw.weight for cw in category_weights}

    # Group requirements by category
    by_category: dict[str, list[ScoredRequirement]] = defaultdict(list)
    for req in scored_reqs:
        by_category[req.category].append(req)

    category_scores = []
    for category, reqs in by_category.items():
        earned = sum(r.earned_points for r in reqs)
        max_pts = sum(r.max_points for r in reqs)
        percentage = round((earned / max_pts * 100) if max_pts > 0 else 0, 1)
        score_10 = round((earned / max_pts * 10) if max_pts > 0 else 0, 1)
        cat_weight = weight_lookup.get(category, 0.2)
        weighted = round(score_10 * cat_weight, 2)

        category_scores.append(
            CategoryScore(
                category=category,
                category_label=CATEGORY_LABELS.get(category, category),
                earned_points=round(earned, 2),
                max_points=round(max_pts, 2),
                percentage=percentage,
                score_out_of_10=score_10,
                category_weight=cat_weight,
                weighted_contribution=weighted,
                requirements=reqs,
            )
        )

    return category_scores


def _compute_improvements(
    scored_reqs: list[ScoredRequirement],
    total_max_points: float,
) -> list[ScoreImprovement]:
    """Identify top improvements the candidate could make."""

    improvements = []
    for req in scored_reqs:
        if req.match_level in ("none", "partial"):
            if req.match_level == "none":
                potential = req.max_points
            else:  # partial
                potential = req.max_points * 0.5  # Upgrading from 0.5 to 1.0

            pct_impact = round(
                (potential / total_max_points * 100) if total_max_points > 0 else 0, 1
            )

            if req.match_level == "none":
                suggestion = f"Add '{req.keyword}' experience or projects to your resume"
            else:
                suggestion = f"Strengthen '{req.keyword}' evidence with specific examples or metrics"

            improvements.append(
                ScoreImprovement(
                    keyword=req.keyword,
                    category=req.category,
                    current_match=req.match_level,
                    potential_points=round(potential, 2),
                    percentage_impact=pct_impact,
                    suggestion=suggestion,
                )
            )

    # Sort by impact descending, return top 5
    improvements.sort(key=lambda x: x.potential_points, reverse=True)
    return improvements[:5]


async def compute_scores(
    job_description: str,
    resume_text: str,
) -> ScoringResult:
    """Full scoring pipeline: extract, score, compute confidence."""

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    # Pass 1: LLM extraction
    logger.info("Scoring: starting requirement extraction...")
    extraction = await _extract_requirements(client, job_description, resume_text)
    logger.info("Scoring: extracted %d requirements.", len(extraction.requirements))

    # Pass 2: Deterministic scoring (use derived weights, not LLM-assigned)
    scored_reqs = _score_requirements(extraction)
    deterministic_weights = _normalize_category_weights(extraction)
    category_scores = _compute_category_scores(scored_reqs, deterministic_weights)

    total_earned = sum(cs.earned_points for cs in category_scores)
    total_max = sum(cs.max_points for cs in category_scores)

    # Overall fit = weighted sum of category scores
    overall_weighted = sum(cs.weighted_contribution for cs in category_scores)
    overall_fit = round(min(overall_weighted / 1.0, 10.0), 1)  # Already on 0-10 scale

    overall_pct = round((total_earned / total_max * 100) if total_max > 0 else 0, 1)

    # Improvements
    improvements = _compute_improvements(scored_reqs, total_max)

    # Confidence
    logger.info("Scoring: starting confidence evaluation...")
    confidence = await _compute_confidence(client, job_description, resume_text, scored_reqs)
    logger.info("Scoring: confidence=%.1f", confidence.overall_confidence)

    return ScoringResult(
        overall_fit_score=overall_fit,
        overall_fit_percentage=overall_pct,
        total_earned_points=round(total_earned, 2),
        total_max_points=round(total_max, 2),
        confidence=confidence,
        category_scores=category_scores,
        scored_requirements=scored_reqs,
        top_improvements=improvements,
    )
