import json
import logging
from datetime import datetime, timezone

from openai import OpenAI

from app.core.config import settings
from app.models.report_schema import DossierReport, ReportMeta
from app.prompts.report_prompt import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)


def generate_dossier(
    company_name: str,
    job_title: str,
    job_description: str,
    resume_text: str,
    recruiter_notes: str = "",
    company_notes: str = "",
) -> DossierReport:
    """Call the OpenAI API to generate a structured dossier report."""
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    user_prompt = build_user_prompt(
        company_name=company_name,
        job_title=job_title,
        job_description=job_description,
        resume_text=resume_text,
        recruiter_notes=recruiter_notes,
        company_notes=company_notes,
    )

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

            # Attach metadata
            data["report_meta"] = {
                "company_name": company_name,
                "job_title": job_title,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "version": "1.0",
            }

            report = DossierReport.model_validate(data)
            return report

        except Exception as e:
            last_error = e
            logger.warning(
                "Dossier generation attempt %d failed: %s", attempt + 1, str(e)
            )

    raise RuntimeError(
        f"Failed to generate dossier after 2 attempts: {last_error}"
    )
