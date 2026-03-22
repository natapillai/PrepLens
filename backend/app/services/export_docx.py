import io

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from app.models.report_schema import PrepLensReportV2

INDIGO = RGBColor(79, 70, 229)
SLATE = RGBColor(148, 163, 184)


def generate_docx(report: PrepLensReportV2) -> bytes:
    """Generate a DOCX file from a PrepLensReportV2."""
    doc = Document()

    style = doc.styles["Normal"]
    font = style.font
    font.name = "Calibri"
    font.size = Pt(10.5)

    meta = report.input_summary

    # Title
    title = doc.add_heading(level=0)
    run = title.add_run("PrepLens Strategy Brief")
    run.font.color.rgb = INDIGO
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Meta
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(f"{meta.company_name} — {meta.job_title}").bold = True
    p.add_run(f"\nGenerated: {report.generated_at[:10]}")
    doc.add_paragraph()

    # 1. Executive Summary
    _h(doc, "Executive Summary")
    _bold_para(doc, report.executive_summary.headline)
    doc.add_paragraph(report.executive_summary.summary)
    for t in report.executive_summary.top_takeaways:
        doc.add_paragraph(t, style="List Bullet")

    # 2. Pursuit Recommendation
    _h(doc, "Pursuit Recommendation")
    pr = report.pursuit_recommendation
    p = doc.add_paragraph()
    p.add_run(f"Recommendation: {pr.recommendation.replace('_', ' ').title()}").bold = True
    p.add_run(f"  |  Fit: {pr.overall_fit_score}/10  |  Confidence: {pr.confidence_score}/10")
    doc.add_paragraph(f"Ideal Candidate: {pr.ideal_candidate_profile}")
    doc.add_paragraph(f"Your Outlook: {pr.candidate_outlook}")
    for reason in pr.reasoning:
        doc.add_paragraph(reason, style="List Bullet")

    # 3. Company Snapshot
    _h(doc, "Company Snapshot")
    cs = report.company_snapshot
    doc.add_paragraph(cs.company_overview)
    if cs.business_model:
        _kv(doc, "Business Model", cs.business_model)
    if cs.product_focus:
        _kv(doc, "Product Focus", cs.product_focus)
    if cs.company_stage != "unknown":
        _kv(doc, "Stage / Risk", f"{cs.company_stage.title()} / {cs.risk_level.title()}")
    for s in cs.engineering_signals:
        doc.add_paragraph(s, style="List Bullet")

    # 4. Role Snapshot
    _h(doc, "Role Snapshot")
    rs = report.role_snapshot
    doc.add_paragraph(rs.role_summary)
    if rs.seniority_signal != "unknown":
        _kv(doc, "Seniority", rs.seniority_signal.title())
    if rs.primary_stack_signals:
        _kv(doc, "Stack", ", ".join(rs.primary_stack_signals))
    if rs.success_profile:
        _kv(doc, "Success Profile", rs.success_profile)

    # 5. Hiring Priorities
    _h(doc, "Hiring Priorities")
    for hp in report.hiring_priorities:
        p = doc.add_paragraph()
        p.add_run(f"[{hp.importance_score}/5] {hp.priority}").bold = True
        doc.add_paragraph(hp.why_it_matters)

    # 6. Fit Analysis
    _h(doc, "Fit Analysis")
    if report.fit_analysis.strong_fit_signals:
        _sub(doc, "Strong Fit")
        for s in report.fit_analysis.strong_fit_signals:
            p = doc.add_paragraph()
            p.add_run(f"[{s.strength_score}/10] {s.signal}").bold = True
            doc.add_paragraph(s.evidence)
    if report.fit_analysis.partial_fit_signals:
        _sub(doc, "Partial Fit")
        for s in report.fit_analysis.partial_fit_signals:
            p = doc.add_paragraph()
            p.add_run(f"[{s.strength_score}/10] {s.signal}").bold = True
            doc.add_paragraph(s.evidence)
    if report.fit_analysis.missing_or_weak_signals:
        _sub(doc, "Gaps")
        for s in report.fit_analysis.missing_or_weak_signals:
            p = doc.add_paragraph()
            p.add_run(f"[{s.gap_severity.upper()}] {s.signal}").bold = True
            doc.add_paragraph(s.why_it_matters)

    # 7. Concerns & Mitigation
    _h(doc, "Concerns & Mitigation")
    for c in report.concerns_and_mitigation:
        p = doc.add_paragraph()
        p.add_run(f"[{c.severity.upper()}] {c.concern}").bold = True
        doc.add_paragraph(f"Why: {c.why_they_may_care}")
        doc.add_paragraph(f"Mitigation: {c.mitigation_strategy}")
        doc.add_paragraph(f"Best proof: {c.best_proof_to_use}")

    # 8. Resume Tailoring
    _h(doc, "Resume Tailoring")
    rt = report.resume_tailoring
    _kv(doc, "Verdict", rt.resume_verdict.replace("_", " ").title())
    if rt.positioning_angle:
        _kv(doc, "Positioning", rt.positioning_angle)
    for edit in rt.priority_edits:
        p = doc.add_paragraph()
        p.add_run(f"[{edit.type.replace('_', ' ')}] {edit.target}").bold = True
        doc.add_paragraph(edit.recommendation)
    if rt.missing_keywords:
        _kv(doc, "Missing Keywords", ", ".join(rt.missing_keywords))

    # 9. Application Strategy
    _h(doc, "Application Strategy")
    app_s = report.application_strategy
    _kv(doc, "Apply Now", "Yes" if app_s.apply_now else "No")
    if app_s.referral_recommended:
        _kv(doc, "Referral", "Recommended")
    if app_s.outreach_angle:
        _kv(doc, "Outreach", app_s.outreach_angle)
    if app_s.suggested_connection_note:
        doc.add_paragraph(f'Connection Note: "{app_s.suggested_connection_note}"')

    # 10. Recruiter Screen Prep
    _h(doc, "Recruiter Screen Prep")
    rp = report.recruiter_screen_prep
    for s in rp.what_they_will_likely_screen_for:
        doc.add_paragraph(s, style="List Bullet")
    for q in rp.likely_recruiter_questions:
        _bold_para(doc, q.question)
        doc.add_paragraph(f"Intent: {q.intent}")
        for pt in q.suggested_answer_points:
            doc.add_paragraph(f"  • {pt}")

    # 11. Story Bank
    _h(doc, "Story Bank")
    for s in report.story_bank:
        _bold_para(doc, s.story_title)
        doc.add_paragraph(f"Experience: {s.recommended_experience}")
        doc.add_paragraph(f"Angle: {s.angle_to_emphasize}")
        if s.key_metrics_or_outcomes:
            doc.add_paragraph(f"Metrics: {', '.join(s.key_metrics_or_outcomes)}")

    # 12. Interview Rounds
    _h(doc, "Interview Round Strategy")
    for rd in report.interview_rounds:
        _bold_para(doc, rd.round_name.replace("_", " ").title())
        doc.add_paragraph(rd.round_goal)
        for f in rd.candidate_focus:
            doc.add_paragraph(f"  • {f}")

    # 13. Interview Questions
    _h(doc, "Likely Interview Questions")
    for q in report.likely_interview_questions:
        p = doc.add_paragraph()
        p.add_run(f"[{q.category.replace('_', ' ').title()}] {q.question}").bold = True
        doc.add_paragraph(q.why_they_may_ask)
        if q.best_story_or_topic:
            doc.add_paragraph(f"Best story/topic: {q.best_story_or_topic}")

    # 14. Reverse Interview Questions
    _h(doc, "Reverse-Interview Questions")
    for q in report.reverse_interview_questions:
        p = doc.add_paragraph()
        p.add_run(f"[{q.target_interviewer.replace('_', ' ').title()}] {q.question}").bold = True
        doc.add_paragraph(q.why_ask_this)

    # 15. Logistics
    _h(doc, "Logistics & Constraints")
    lg = report.logistics_and_constraints
    _kv(doc, "Work Model", lg.work_model.title())
    _kv(doc, "Level Clarity", lg.level_clarity.title())
    if lg.location_notes:
        _kv(doc, "Location", lg.location_notes)
    if lg.compensation_signal:
        _kv(doc, "Compensation", lg.compensation_signal)
    if lg.timeline_signal:
        _kv(doc, "Timeline", lg.timeline_signal)

    # 16. Red Flags
    _h(doc, "Red Flags & Unknowns")
    for f in report.red_flags_and_unknowns.red_flags:
        p = doc.add_paragraph()
        p.add_run(f"[{f.severity.upper()}] {f.flag}").bold = True
        doc.add_paragraph(f.why_it_matters)
    if report.red_flags_and_unknowns.unknowns_to_verify:
        _sub(doc, "Unknowns to Verify")
        for u in report.red_flags_and_unknowns.unknowns_to_verify:
            doc.add_paragraph(u, style="List Bullet")

    # 17. Next Actions
    _h(doc, "Immediate Next Actions")
    for a in sorted(report.immediate_next_actions, key=lambda x: x.priority):
        time_str = f" (~{a.time_estimate_minutes}m)" if a.time_estimate_minutes else ""
        p = doc.add_paragraph()
        p.add_run(f"{a.priority}. {a.action}{time_str}").bold = True
        doc.add_paragraph(a.why)

    # 18. Checklist
    _h(doc, "Preparation Checklist")
    for item in report.prep_checklist:
        doc.add_paragraph(f"☐ {item.item}")

    # Footer
    doc.add_paragraph()
    footer = doc.add_paragraph("Generated by PrepLens")
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.runs[0].font.color.rgb = SLATE

    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


def _h(doc: Document, text: str):
    heading = doc.add_heading(text, level=2)
    for run in heading.runs:
        run.font.color.rgb = INDIGO


def _sub(doc: Document, text: str):
    heading = doc.add_heading(text, level=3)
    for run in heading.runs:
        run.font.color.rgb = RGBColor(100, 116, 139)


def _bold_para(doc: Document, text: str):
    p = doc.add_paragraph()
    p.add_run(text).bold = True


def _kv(doc: Document, key: str, value: str):
    p = doc.add_paragraph()
    p.add_run(f"{key}: ").bold = True
    p.add_run(value)
