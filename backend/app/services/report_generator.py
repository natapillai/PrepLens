import json
import logging
import uuid
from datetime import datetime, timezone

from openai import AsyncOpenAI

from app.core.config import settings
from app.models.report_schema import (
    PrepLensReportV2,
    InputSummary,
    ExportMetadata,
)
from app.prompts.report_prompt import SYSTEM_PROMPT, build_user_prompt
from app.services.scoring_service import compute_scores

logger = logging.getLogger(__name__)

# Default values for sections the LLM sometimes omits
_SECTION_DEFAULTS: dict[str, object] = {
    "executive_summary": {"headline": "", "summary": "", "top_takeaways": []},
    "pursuit_recommendation": {
        "overall_fit_score": 5,
        "confidence_score": 5,
        "recommendation": "insufficient_information",
        "reasoning": [],
        "ideal_candidate_profile": "",
        "candidate_outlook": "",
    },
    "company_snapshot": {"company_overview": ""},
    "role_snapshot": {"role_summary": ""},
    "fit_analysis": {
        "strong_fit_signals": [],
        "partial_fit_signals": [],
        "missing_or_weak_signals": [],
    },
    "resume_tailoring": {"resume_verdict": "tailor_before_applying"},
    "application_strategy": {},
    "recruiter_screen_prep": {},
    "logistics_and_constraints": {},
    "red_flags_and_unknowns": {"red_flags": [], "unknowns_to_verify": []},
    "hiring_priorities": [],
    "concerns_and_mitigation": [],
    "story_bank": [],
    "interview_rounds": [],
    "likely_interview_questions": [],
    "reverse_interview_questions": [],
    "immediate_next_actions": [],
    "prep_checklist": [],
}


def _patch_missing_sections(data: dict) -> None:
    """Fill in missing sections with safe defaults so Pydantic never fails
    on fields the LLM omitted."""
    for key, default in _SECTION_DEFAULTS.items():
        if key not in data:
            logger.warning("LLM omitted section '%s', using default", key)
            data[key] = default


async def generate_dossier(
    company_name: str,
    job_title: str,
    job_description: str,
    resume_text: str,
    recruiter_notes: str = "",
    company_notes: str = "",
) -> PrepLensReportV2:
    """Call the OpenAI API to generate a structured V2 dossier report.

    Pipeline:
    1. Run ATS-style scoring (extract requirements, match, compute scores)
    2. Feed computed scores into the dossier prompt so the LLM uses them
    3. Generate the full dossier with evidence-backed scores
    """
    # Step 1: Compute ATS-style scores
    logger.info("Starting ATS-style scoring pipeline...")
    try:
        scoring_result = await compute_scores(
            job_description=job_description,
            resume_text=resume_text,
        )
        scoring_data = scoring_result.model_dump()
        logger.info(
            "Scoring complete: overall_fit=%.1f, confidence=%.1f",
            scoring_result.overall_fit_score,
            scoring_result.confidence.overall_confidence,
        )
    except Exception as e:
        logger.warning(
            "Scoring pipeline failed (%s: %s), falling back to LLM-only",
            type(e).__name__, str(e),
        )
        scoring_result = None
        scoring_data = None

    # Step 2: Build the dossier prompt, injecting computed scores
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    user_prompt = build_user_prompt(
        company_name=company_name,
        job_title=job_title,
        job_description=job_description,
        resume_text=resume_text,
        recruiter_notes=recruiter_notes,
        company_notes=company_notes,
        scoring_result=scoring_result,
    )

    now = datetime.now(timezone.utc)

    # Try up to 2 times (initial + 1 retry)
    last_error = None
    for attempt in range(2):
        try:
            logger.info("Dossier LLM call attempt %d starting...", attempt + 1)
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.4,
                response_format={"type": "json_object"},
            )
            logger.info("Dossier LLM call attempt %d complete.", attempt + 1)

            raw_content = response.choices[0].message.content
            if not raw_content:
                raise ValueError("Empty response from model")

            data = json.loads(raw_content)

            # Patch missing optional sections — LLM sometimes omits
            # later sections when the prompt is long
            _patch_missing_sections(data)

            # Attach metadata that the model doesn't generate
            data["schema_version"] = "2.0"
            data["generated_at"] = now.isoformat()
            data["report_id"] = str(uuid.uuid4())
            data["product_name"] = "PrepLens"
            data["input_summary"] = {
                "company_name": company_name,
                "job_title": job_title,
                "job_posting_url": None,
                "resume_filename": None,
                "candidate_notes_present": bool(
                    recruiter_notes.strip() or company_notes.strip()
                ),
                "job_description_present": True,
                "job_description_length": len(job_description),
            }
            data["export_metadata"] = {
                "export_title": f"PrepLens Strategy Brief — {company_name}",
                "export_subtitle": job_title,
                "export_date": now.strftime("%Y-%m-%d"),
                "branding": "PrepLens",
            }

            # Override LLM scores with computed scores
            if scoring_result:
                data["pursuit_recommendation"]["overall_fit_score"] = scoring_result.overall_fit_score
                data["pursuit_recommendation"]["confidence_score"] = scoring_result.confidence.overall_confidence

            # Attach full scoring breakdown
            data["scoring"] = scoring_data

            report = PrepLensReportV2.model_validate(data)
            logger.info("Dossier generated successfully (report_id=%s)", data["report_id"])
            return report

        except Exception as e:
            last_error = e
            logger.warning(
                "Dossier generation attempt %d failed (%s): %s",
                attempt + 1, type(e).__name__, str(e) or repr(e),
            )

    raise RuntimeError(
        f"Failed to generate dossier after 2 attempts: {type(last_error).__name__}: {last_error!r}"
    )
