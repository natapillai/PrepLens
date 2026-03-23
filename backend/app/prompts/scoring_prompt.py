"""Prompts for Pass 1: requirement extraction and resume matching."""

SCORING_SYSTEM_PROMPT = """You are an expert ATS (Applicant Tracking System) analyzer. Your job is to:

1. Extract every skill, qualification, and attribute the job description requires or prefers.
2. Match each requirement against the candidate's resume.
3. Assign category weights based on what the job description emphasizes most.

Rules:
- Be thorough. Extract ALL requirements, even implicit ones (e.g. if the JD says "design scalable APIs", extract both "API design" and "scalability").
- Recognize synonyms and related terms. "AWS Lambda" matches "serverless computing". "FastAPI" matches "Python web frameworks". "CI/CD" matches "Jenkins" or "GitHub Actions".
- A "direct" match means the resume clearly demonstrates this skill with evidence.
- A "partial" match means the resume shows related experience but not an exact match.
- A "none" match means no evidence of this skill in the resume.
- Be honest and conservative. Do not inflate matches.
- Category weights must sum to 1.0 and reflect the JD's emphasis, not a generic formula.
- Return ONLY valid JSON. No markdown. No code fences."""

SCORING_USER_PROMPT_TEMPLATE = """Analyze the following job description and resume. Extract all requirements and match them.

## Job Description
{job_description}

## Candidate Resume
{resume_text}

## Instructions

Return a JSON object with exactly this structure:

{{
  "requirements": [
    {{
      "keyword": "The skill or qualification (e.g. 'Python', 'distributed systems', 'team leadership')",
      "category": "hard_skill | soft_skill | domain_knowledge | tool_or_technology | education",
      "importance": "required | preferred | nice_to_have",
      "source_quote": "The phrase from the JD that implies this requirement"
    }}
  ],
  "matches": [
    {{
      "keyword": "Must match a keyword from requirements above",
      "match_level": "direct | partial | none",
      "resume_evidence": "Summary of what the resume shows for this skill",
      "resume_quotes": ["Exact phrases from the resume"],
      "match_reasoning": "Why this is direct/partial/none. Mention synonym recognition if applicable."
    }}
  ],
  "category_weights": [
    {{
      "category": "hard_skill",
      "weight": 0.0,
      "reasoning": "Why this weight based on JD emphasis"
    }},
    {{
      "category": "soft_skill",
      "weight": 0.0,
      "reasoning": "Why this weight based on JD emphasis"
    }},
    {{
      "category": "domain_knowledge",
      "weight": 0.0,
      "reasoning": "Why this weight based on JD emphasis"
    }},
    {{
      "category": "tool_or_technology",
      "weight": 0.0,
      "reasoning": "Why this weight based on JD emphasis"
    }},
    {{
      "category": "education",
      "weight": 0.0,
      "reasoning": "Why this weight based on JD emphasis"
    }}
  ]
}}

Guidelines for extraction:
- Extract 15-30 requirements depending on JD complexity.
- Every requirement MUST have exactly one match entry.
- Categories:
  - hard_skill: Programming languages, frameworks, methodologies (e.g. Python, microservices, TDD)
  - soft_skill: Communication, leadership, collaboration, adaptability
  - domain_knowledge: Industry or domain expertise (e.g. fintech, healthcare, AI/ML)
  - tool_or_technology: Specific tools, platforms, services (e.g. AWS, Docker, PostgreSQL)
  - education: Degrees, certifications, coursework
- Importance levels:
  - required: Explicitly stated as required, or strongly implied as essential
  - preferred: Listed as preferred, desired, or "nice to have" but emphasized
  - nice_to_have: Mentioned briefly or implied but not critical
- Category weights should reflect the JD. A deeply technical backend role might weight hard_skill at 0.35 and tool_or_technology at 0.30. A management role might weight soft_skill at 0.35.
- All category weights MUST sum to 1.0.

Return ONLY the JSON object."""


CONFIDENCE_SYSTEM_PROMPT = """You are evaluating the quality and specificity of job application inputs to determine scoring confidence. Return ONLY valid JSON."""

CONFIDENCE_USER_PROMPT_TEMPLATE = """Evaluate the quality of these inputs for scoring confidence.

## Job Description
{job_description}

## Candidate Resume
{resume_text}

## Matching Summary
- Total requirements extracted: {total_requirements}
- Direct matches: {direct_matches}
- Partial matches: {partial_matches}
- No matches: {no_matches}

Return a JSON object:
{{
  "jd_specificity": 0.0,
  "jd_specificity_reasoning": "How specific and detailed is the JD? Vague JDs with generic requirements score lower.",
  "resume_detail": 0.0,
  "resume_detail_reasoning": "How detailed is the resume? Resumes with metrics, specific projects, and clear descriptions score higher.",
  "match_clarity": 0.0,
  "match_clarity_reasoning": "How clear-cut were the matches? Many ambiguous/partial matches lower this score."
}}

All scores are 0.0-10.0. Return ONLY the JSON object."""


def build_scoring_prompt(job_description: str, resume_text: str) -> str:
    return SCORING_USER_PROMPT_TEMPLATE.format(
        job_description=job_description,
        resume_text=resume_text,
    )


def build_confidence_prompt(
    job_description: str,
    resume_text: str,
    total_requirements: int,
    direct_matches: int,
    partial_matches: int,
    no_matches: int,
) -> str:
    return CONFIDENCE_USER_PROMPT_TEMPLATE.format(
        job_description=job_description,
        resume_text=resume_text,
        total_requirements=total_requirements,
        direct_matches=direct_matches,
        partial_matches=partial_matches,
        no_matches=no_matches,
    )
