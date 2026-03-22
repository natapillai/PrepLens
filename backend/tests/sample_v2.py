"""Shared V2 sample report data for tests."""

SAMPLE_REPORT_V2 = {
    "schema_version": "2.0",
    "generated_at": "2026-03-22T00:00:00Z",
    "report_id": "test-id-123",
    "product_name": "PrepLens",
    "input_summary": {
        "company_name": "TestCo",
        "job_title": "Engineer",
        "job_posting_url": None,
        "resume_filename": None,
        "candidate_notes_present": False,
        "job_description_present": True,
        "job_description_length": 500,
    },
    "executive_summary": {
        "headline": "Strong fit for a backend-focused engineering role",
        "summary": "The candidate has relevant backend experience that aligns well with TestCo's needs.",
        "top_takeaways": ["Strong Python skills", "Relevant domain experience"],
    },
    "pursuit_recommendation": {
        "overall_fit_score": 7,
        "confidence_score": 6,
        "recommendation": "pursue",
        "reasoning": ["Strong backend alignment", "Domain overlap"],
        "ideal_candidate_profile": "Senior backend engineer with distributed systems experience",
        "candidate_outlook": "Good fit with minor gaps in frontend experience",
    },
    "company_snapshot": {
        "company_overview": "TestCo is a mid-stage technology company.",
        "business_model": "B2B SaaS",
        "product_focus": "Developer tools",
        "engineering_signals": ["Uses Python", "Microservices architecture"],
        "company_stage": "growth",
        "risk_level": "medium",
        "notable_unknowns": ["Team size unclear"],
    },
    "role_snapshot": {
        "role_summary": "Backend engineer building APIs and services.",
        "seniority_signal": "senior",
        "core_domain": ["backend", "APIs"],
        "primary_stack_signals": ["Python", "FastAPI", "PostgreSQL"],
        "success_profile": "Ship reliable backend services within 6 months.",
    },
    "hiring_priorities": [
        {
            "priority": "Backend systems experience",
            "why_it_matters": "Core of the role",
            "importance_score": 5,
        },
        {
            "priority": "API design",
            "why_it_matters": "Key deliverable",
            "importance_score": 4,
        },
    ],
    "fit_analysis": {
        "strong_fit_signals": [
            {
                "signal": "Python expertise",
                "evidence": "5 years of Python development",
                "strength_score": 8,
            }
        ],
        "partial_fit_signals": [
            {
                "signal": "Cloud experience",
                "evidence": "Some AWS usage but not primary",
                "strength_score": 5,
            }
        ],
        "missing_or_weak_signals": [
            {
                "signal": "Frontend skills",
                "why_it_matters": "Some full-stack work expected",
                "gap_severity": "low",
            }
        ],
    },
    "concerns_and_mitigation": [
        {
            "concern": "Limited leadership experience",
            "why_they_may_care": "Senior role implies mentoring",
            "severity": "medium",
            "mitigation_strategy": "Highlight code review and mentoring examples",
            "best_proof_to_use": "Led architecture review sessions",
            "sample_response": "I regularly led design reviews and mentored junior engineers.",
        }
    ],
    "resume_tailoring": {
        "resume_verdict": "tailor_before_applying",
        "priority_edits": [
            {
                "type": "keyword_addition",
                "target": "Skills section",
                "recommendation": "Add FastAPI explicitly",
                "why": "Listed in JD requirements",
            }
        ],
        "missing_keywords": ["FastAPI", "microservices"],
        "bullets_to_emphasize": [
            {
                "experience_area": "API development",
                "why": "Directly relevant to role",
            }
        ],
        "positioning_angle": "Experienced backend engineer specializing in Python APIs",
    },
    "application_strategy": {
        "apply_now": True,
        "referral_recommended": True,
        "best_outreach_target": "hiring_manager",
        "outreach_angle": "Mention shared interest in developer tools",
        "suggested_connection_note": "Hi, I noticed TestCo is hiring for backend engineers.",
        "suggested_email_angle": "Reference specific product features",
    },
    "recruiter_screen_prep": {
        "what_they_will_likely_screen_for": ["Python experience", "System design"],
        "likely_recruiter_questions": [
            {
                "question": "Tell me about your Python experience",
                "intent": "Verify core skill match",
                "suggested_answer_points": ["Years of experience", "Types of projects"],
            }
        ],
        "work_auth_notes": None,
        "compensation_notes": "Market rate for senior backend",
        "availability_notes": None,
    },
    "story_bank": [
        {
            "story_title": "API Migration Project",
            "best_for_questions": ["Tell me about a complex project"],
            "recommended_experience": "Led REST to GraphQL migration",
            "angle_to_emphasize": "Technical leadership and delivery",
            "key_metrics_or_outcomes": ["50% latency reduction"],
            "likely_follow_up_questions": ["What were the tradeoffs?"],
        }
    ],
    "interview_rounds": [
        {
            "round_name": "technical",
            "round_goal": "Assess coding and system design skills",
            "what_they_will_likely_probe": ["API design", "Database modeling"],
            "best_stories_to_prepare": ["API Migration Project"],
            "candidate_focus": ["Show depth in backend systems"],
        }
    ],
    "likely_interview_questions": [
        {
            "question": "Design an API for a task management system",
            "category": "system_design",
            "why_they_may_ask": "Core skill for the role",
            "best_story_or_topic": "API Migration Project",
        },
        {
            "question": "Tell me about a time you resolved a production incident",
            "category": "behavioral",
            "why_they_may_ask": "Assess operational maturity",
            "best_story_or_topic": "On-call experience",
        },
    ],
    "reverse_interview_questions": [
        {
            "target_interviewer": "hiring_manager",
            "question": "How is success measured for this role?",
            "why_ask_this": "Understand expectations",
            "good_answer_signals": ["Clear metrics", "Defined goals"],
            "bad_answer_signals": ["Vague answers"],
            "follow_up_question": "What does the first 90 days look like?",
        }
    ],
    "logistics_and_constraints": {
        "work_model": "hybrid",
        "location_notes": "Office in SF",
        "visa_or_work_auth_signal": None,
        "level_clarity": "clear",
        "compensation_signal": "$180-220k base",
        "timeline_signal": "Hiring urgently",
    },
    "red_flags_and_unknowns": {
        "red_flags": [
            {
                "flag": "High turnover mentioned in reviews",
                "severity": "medium",
                "why_it_matters": "May indicate culture issues",
            }
        ],
        "unknowns_to_verify": ["Team size", "Tech debt level"],
    },
    "immediate_next_actions": [
        {
            "priority": 1,
            "action": "Tailor resume with missing keywords",
            "why": "Improve ATS match rate",
            "time_estimate_minutes": 30,
        },
        {
            "priority": 2,
            "action": "Research TestCo engineering blog",
            "why": "Prepare informed questions",
            "time_estimate_minutes": 20,
        },
    ],
    "prep_checklist": [
        {"item": "Update resume", "completed": False},
        {"item": "Research company", "completed": False},
        {"item": "Prepare stories", "completed": False},
    ],
    "export_metadata": {
        "export_title": "PrepLens Strategy Brief — TestCo",
        "export_subtitle": "Engineer",
        "export_date": "2026-03-22",
        "branding": "PrepLens",
    },
}
