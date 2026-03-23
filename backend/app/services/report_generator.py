import json
import logging
import uuid
from datetime import datetime, timezone

from openai import OpenAI

from app.core.config import settings
from app.models.report_schema import (
    PrepLensReportV2,
    InputSummary,
    ExportMetadata,
)
from app.prompts.report_prompt import SYSTEM_PROMPT, build_user_prompt
from app.services.scoring_service import compute_scores

logger = logging.getLogger(__name__)


def generate_dossier(
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
        scoring_result = compute_scores(
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
        logger.warning("Scoring pipeline failed, falling back to LLM-only: %s", str(e))
        scoring_result = None
        scoring_data = None

    # Step 2: Build the dossier prompt, injecting computed scores
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

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
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.4,
                response_format={"type": "json_object"},
            )

            raw_content = response.choices[0].message.content
            if not raw_content:
                raise ValueError("Empty response from model")

            data = json.loads(raw_content)

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
                data["pursuit_recommendation"]["overall_fit_score"] = round(
                    scoring_result.overall_fit_score
                )
                data["pursuit_recommendation"]["confidence_score"] = round(
                    scoring_result.confidence.overall_confidence
                )

            # Attach full scoring breakdown
            data["scoring"] = scoring_data

            report = PrepLensReportV2.model_validate(data)
            return report

        except Exception as e:
            last_error = e
            logger.warning(
                "Dossier generation attempt %d failed: %s", attempt + 1, str(e)
            )

    raise RuntimeError(
        f"Failed to generate dossier after 2 attempts: {last_error}"
    )
