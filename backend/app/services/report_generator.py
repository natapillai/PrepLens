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

logger = logging.getLogger(__name__)


def generate_dossier(
    company_name: str,
    job_title: str,
    job_description: str,
    resume_text: str,
    recruiter_notes: str = "",
    company_notes: str = "",
) -> PrepLensReportV2:
    """Call the OpenAI API to generate a structured V2 dossier report."""
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    user_prompt = build_user_prompt(
        company_name=company_name,
        job_title=job_title,
        job_description=job_description,
        resume_text=resume_text,
        recruiter_notes=recruiter_notes,
        company_notes=company_notes,
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
