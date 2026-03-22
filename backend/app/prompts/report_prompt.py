SYSTEM_PROMPT = """You are PrepLens, an expert interview strategy advisor. Your job is to analyze a candidate's resume against a specific job description and produce a structured interview strategy brief.

Rules:
- Be specific and evidence-based. Anchor advice in the actual resume content and job description provided.
- Distinguish between direct evidence from the inputs and reasonable inferences.
- Do NOT fabricate company facts. If information is insufficient, label it as unknown.
- Keep outputs concise and actionable. Avoid generic filler.
- Each section should provide practical value for interview preparation.
- Questions should feel realistic for the specific role and company."""

USER_PROMPT_TEMPLATE = """Analyze the following inputs and produce a structured interview strategy brief.

## Company
Name: {company_name}
Title: {job_title}

## Job Description
{job_description}

## Candidate Resume
{resume_text}

{notes_section}

## Instructions
Produce a JSON object with exactly this structure:

{{
  "role_summary": "A 2-3 sentence summary of the role and what the company appears to be looking for.",
  "hiring_priorities": ["List of 4-6 likely hiring priorities based on the JD"],
  "candidate_strengths": ["List of 4-6 specific strengths from the resume that align with this role"],
  "candidate_concerns": [
    {{
      "concern": "A specific concern or gap",
      "severity": "low|medium|high",
      "mitigation": "How to address or frame this"
    }}
  ],
  "likely_interview_questions": [
    {{
      "question": "A realistic interview question",
      "why_they_might_ask": "Why this question is likely for this role"
    }}
  ],
  "reverse_interview_questions": [
    {{
      "audience": "Recruiter|Hiring Manager|Engineer",
      "question": "A question for the candidate to ask",
      "why_it_matters": "Why this question provides useful signal"
    }}
  ],
  "positioning_strategy": ["List of 3-5 specific positioning recommendations"],
  "red_flags_or_unknowns": ["List of 3-5 things to investigate or watch for"],
  "prep_checklist": ["List of 5-8 concrete preparation actions"]
}}

Generate 3-5 items for candidate_concerns, 6-8 for likely_interview_questions, 4-6 for reverse_interview_questions.
Return ONLY the JSON object. No markdown fencing, no explanation."""


def build_user_prompt(
    company_name: str,
    job_title: str,
    job_description: str,
    resume_text: str,
    recruiter_notes: str = "",
    company_notes: str = "",
) -> str:
    notes_parts = []
    if recruiter_notes.strip():
        notes_parts.append(f"## Recruiter Notes\n{recruiter_notes.strip()}")
    if company_notes.strip():
        notes_parts.append(f"## Company Notes\n{company_notes.strip()}")
    notes_section = "\n\n".join(notes_parts) if notes_parts else ""

    return USER_PROMPT_TEMPLATE.format(
        company_name=company_name,
        job_title=job_title,
        job_description=job_description,
        resume_text=resume_text,
        notes_section=notes_section,
    )
