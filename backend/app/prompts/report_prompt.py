SYSTEM_PROMPT = """You are PrepLens, an expert job-search strategy advisor. Your job is to analyze a candidate's resume against a specific job description and produce a comprehensive PrepLens V2 dossier.

The dossier helps the candidate answer four questions:
1. Should I pursue this role?
2. How should I tailor my application?
3. How should I position myself in interviews?
4. What should I do next?

Rules:
- Be specific and evidence-based. Anchor advice in the actual resume content and job description provided.
- Distinguish between direct evidence from the inputs and reasonable inferences.
- Do NOT fabricate company facts. If information is insufficient, use null, "unknown", or an empty array.
- Keep outputs concise and actionable. Avoid generic filler.
- Each section should provide practical value.
- Questions should feel realistic for the specific role and company.
- Use scoring conventions consistently:
  - overall_fit_score and confidence_score: 0-10 scale
  - importance_score for priorities: 1-5 scale
  - strength_score for fit signals: 1-10 scale
- Return ONLY valid JSON. No markdown. No code fences. No commentary outside the JSON."""

USER_PROMPT_TEMPLATE = """Analyze the following inputs and produce a PrepLens V2 strategy dossier.

## Company
Name: {company_name}
Title: {job_title}

## Job Description
{job_description}

## Candidate Resume
{resume_text}

{notes_section}

## Instructions
Produce a JSON object with exactly this structure. Follow it precisely.

{{
  "executive_summary": {{
    "headline": "One-line verdict on fit and opportunity",
    "summary": "2-3 sentence overview of the match",
    "top_takeaways": ["3-5 key takeaways"]
  }},
  "pursuit_recommendation": {{
    "overall_fit_score": 0,
    "confidence_score": 0,
    "recommendation": "pursue|pursue_selectively|low_priority|insufficient_information",
    "reasoning": ["3-5 reasons supporting the recommendation"],
    "ideal_candidate_profile": "What the ideal candidate looks like for this role",
    "candidate_outlook": "How the candidate compares to the ideal profile"
  }},
  "company_snapshot": {{
    "company_overview": "Brief overview of the company",
    "business_model": "string or null",
    "product_focus": "string or null",
    "engineering_signals": ["signals about eng culture/practices"],
    "company_stage": "startup|growth|enterprise|public|unknown",
    "risk_level": "low|medium|high|unknown",
    "notable_unknowns": ["things not clear about the company"]
  }},
  "role_snapshot": {{
    "role_summary": "2-3 sentence role summary",
    "seniority_signal": "junior|mid|senior|staff|unknown",
    "core_domain": ["primary domains for this role"],
    "primary_stack_signals": ["tech stack signals from the JD"],
    "success_profile": "What success looks like in the first 6-12 months"
  }},
  "hiring_priorities": [
    {{
      "priority": "A hiring priority",
      "why_it_matters": "Why this matters for this role",
      "importance_score": 1
    }}
  ],
  "fit_analysis": {{
    "strong_fit_signals": [
      {{
        "signal": "A strong fit signal",
        "evidence": "Evidence from resume",
        "strength_score": 1
      }}
    ],
    "partial_fit_signals": [
      {{
        "signal": "A partial fit signal",
        "evidence": "Evidence with caveats",
        "strength_score": 1
      }}
    ],
    "missing_or_weak_signals": [
      {{
        "signal": "A gap or weak area",
        "why_it_matters": "Why this matters",
        "gap_severity": "low|medium|high"
      }}
    ]
  }},
  "concerns_and_mitigation": [
    {{
      "concern": "A concern the interviewer may have",
      "why_they_may_care": "Why this is a concern",
      "severity": "low|medium|high",
      "mitigation_strategy": "How to address it",
      "best_proof_to_use": "Best evidence to counter the concern",
      "sample_response": "A sample response if asked about this"
    }}
  ],
  "resume_tailoring": {{
    "resume_verdict": "good_to_apply|tailor_before_applying|needs_significant_rewrite",
    "priority_edits": [
      {{
        "type": "bullet_rewrite|keyword_addition|reorder_section|project_highlight|summary_adjustment",
        "target": "Which part of the resume",
        "recommendation": "What to change",
        "why": "Why this edit matters"
      }}
    ],
    "missing_keywords": ["keywords from JD missing in resume"],
    "bullets_to_emphasize": [
      {{
        "experience_area": "Which experience area",
        "why": "Why to emphasize it"
      }}
    ],
    "positioning_angle": "Overall positioning angle for the resume"
  }},
  "application_strategy": {{
    "apply_now": true,
    "referral_recommended": true,
    "best_outreach_target": "recruiter|hiring_manager|engineer|alumni|none",
    "outreach_angle": "How to frame outreach",
    "suggested_connection_note": "Short LinkedIn connection note",
    "suggested_email_angle": "Email angle if reaching out directly"
  }},
  "recruiter_screen_prep": {{
    "what_they_will_likely_screen_for": ["screening criteria"],
    "likely_recruiter_questions": [
      {{
        "question": "A likely recruiter question",
        "intent": "What the recruiter is trying to learn",
        "suggested_answer_points": ["key points to include in the answer"]
      }}
    ],
    "work_auth_notes": "string or null",
    "compensation_notes": "string or null",
    "availability_notes": "string or null"
  }},
  "story_bank": [
    {{
      "story_title": "Short title for this story",
      "best_for_questions": ["types of questions this story answers"],
      "recommended_experience": "Which resume experience to draw from",
      "angle_to_emphasize": "How to frame the story",
      "key_metrics_or_outcomes": ["quantifiable results"],
      "likely_follow_up_questions": ["follow-ups to prepare for"]
    }}
  ],
  "interview_rounds": [
    {{
      "round_name": "recruiter_screen|hiring_manager|technical|behavioral|final_round",
      "round_goal": "What the round evaluates",
      "what_they_will_likely_probe": ["topics they will probe"],
      "best_stories_to_prepare": ["stories to have ready"],
      "candidate_focus": ["what to focus on in this round"]
    }}
  ],
  "likely_interview_questions": [
    {{
      "question": "A realistic interview question",
      "category": "technical|behavioral|system_design|role_fit|company_fit",
      "why_they_may_ask": "Why this question is likely",
      "best_story_or_topic": "Best story or topic to use in response"
    }}
  ],
  "reverse_interview_questions": [
    {{
      "target_interviewer": "recruiter|hiring_manager|engineer|panel|final_round",
      "question": "A question for the candidate to ask",
      "why_ask_this": "Why this question provides useful signal",
      "good_answer_signals": ["signals of a good answer"],
      "bad_answer_signals": ["signals of a bad answer"],
      "follow_up_question": "string or null"
    }}
  ],
  "logistics_and_constraints": {{
    "work_model": "remote|hybrid|onsite|unknown",
    "location_notes": "string or null",
    "visa_or_work_auth_signal": "string or null",
    "level_clarity": "clear|unclear|unknown",
    "compensation_signal": "string or null",
    "timeline_signal": "string or null"
  }},
  "red_flags_and_unknowns": {{
    "red_flags": [
      {{
        "flag": "A red flag",
        "severity": "low|medium|high",
        "why_it_matters": "Why this is concerning"
      }}
    ],
    "unknowns_to_verify": ["things to verify before or during the process"]
  }},
  "immediate_next_actions": [
    {{
      "priority": 1,
      "action": "A specific next action",
      "why": "Why this action matters",
      "time_estimate_minutes": 15
    }}
  ],
  "prep_checklist": [
    {{
      "item": "A preparation item",
      "completed": false
    }}
  ]
}}

Generate:
- 4-6 hiring_priorities
- 3-5 strong_fit_signals, 2-4 partial_fit_signals, 2-4 missing_or_weak_signals
- 3-5 concerns_and_mitigation items
- 3-5 resume priority_edits
- 3-5 likely_recruiter_questions
- 4-6 story_bank items
- 3-5 interview_rounds
- 8-12 likely_interview_questions
- 5-8 reverse_interview_questions
- 5-8 immediate_next_actions
- 6-10 prep_checklist items

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
