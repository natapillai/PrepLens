import io

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
    HRFlowable,
)

from app.models.report_schema import PrepLensReportV2

PRIMARY = HexColor("#4f46e5")
MUTED = HexColor("#64748b")
EMERALD = HexColor("#059669")
AMBER = HexColor("#d97706")
RED = HexColor("#dc2626")


def generate_pdf(report: PrepLensReportV2) -> bytes:
    """Generate a PDF file from a PrepLensReportV2."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle("BriefTitle", parent=styles["Title"], fontSize=20, textColor=PRIMARY, spaceAfter=6))
    styles.add(ParagraphStyle("BriefMeta", parent=styles["Normal"], fontSize=11, textColor=MUTED, alignment=1, spaceAfter=20))
    styles.add(ParagraphStyle("SectionHead", parent=styles["Heading2"], fontSize=14, textColor=PRIMARY, spaceBefore=16, spaceAfter=8))
    styles.add(ParagraphStyle("SubHead", parent=styles["Heading3"], fontSize=11, textColor=MUTED, spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle("BriefBody", parent=styles["Normal"], fontSize=10, leading=14, spaceAfter=4))
    styles.add(ParagraphStyle("BriefBold", parent=styles["Normal"], fontSize=10, leading=14, spaceAfter=2))
    styles.add(ParagraphStyle("BriefSmall", parent=styles["Normal"], fontSize=9, leading=12, textColor=MUTED, spaceAfter=2))

    el = []  # elements
    meta = report.input_summary

    # Title
    el.append(Paragraph("PrepLens Strategy Brief", styles["BriefTitle"]))
    el.append(Paragraph(
        f"{meta.company_name} — {meta.job_title}<br/>Generated: {report.generated_at[:10]}",
        styles["BriefMeta"],
    ))
    el.append(HRFlowable(width="100%", color=PRIMARY, thickness=1))
    el.append(Spacer(1, 12))

    # 1. Executive Summary
    el.append(Paragraph("Executive Summary", styles["SectionHead"]))
    el.append(Paragraph(f"<b>{report.executive_summary.headline}</b>", styles["BriefBold"]))
    el.append(Paragraph(report.executive_summary.summary, styles["BriefBody"]))
    for t in report.executive_summary.top_takeaways:
        el.append(Paragraph(f"• {t}", styles["BriefBody"]))

    # 2. Pursuit Recommendation
    el.append(Paragraph("Pursuit Recommendation", styles["SectionHead"]))
    pr = report.pursuit_recommendation
    el.append(Paragraph(
        f"<b>Recommendation:</b> {pr.recommendation.replace('_', ' ').title()} | "
        f"<b>Fit:</b> {pr.overall_fit_score}/10 | <b>Confidence:</b> {pr.confidence_score}/10",
        styles["BriefBold"],
    ))
    el.append(Paragraph(f"<b>Ideal Candidate:</b> {pr.ideal_candidate_profile}", styles["BriefBody"]))
    el.append(Paragraph(f"<b>Your Outlook:</b> {pr.candidate_outlook}", styles["BriefBody"]))
    for reason in pr.reasoning:
        el.append(Paragraph(f"• {reason}", styles["BriefBody"]))

    # 3. Company Snapshot
    el.append(Paragraph("Company Snapshot", styles["SectionHead"]))
    cs = report.company_snapshot
    el.append(Paragraph(cs.company_overview, styles["BriefBody"]))
    if cs.business_model:
        el.append(Paragraph(f"<b>Business Model:</b> {cs.business_model}", styles["BriefBody"]))
    if cs.product_focus:
        el.append(Paragraph(f"<b>Product Focus:</b> {cs.product_focus}", styles["BriefBody"]))
    if cs.company_stage != "unknown":
        el.append(Paragraph(f"<b>Stage:</b> {cs.company_stage.title()} | <b>Risk:</b> {cs.risk_level.title()}", styles["BriefBody"]))
    for s in cs.engineering_signals:
        el.append(Paragraph(f"• {s}", styles["BriefBody"]))

    # 4. Role Snapshot
    el.append(Paragraph("Role Snapshot", styles["SectionHead"]))
    rs = report.role_snapshot
    el.append(Paragraph(rs.role_summary, styles["BriefBody"]))
    if rs.seniority_signal != "unknown":
        el.append(Paragraph(f"<b>Seniority:</b> {rs.seniority_signal.title()}", styles["BriefBody"]))
    if rs.primary_stack_signals:
        el.append(Paragraph(f"<b>Stack:</b> {', '.join(rs.primary_stack_signals)}", styles["BriefBody"]))
    if rs.success_profile:
        el.append(Paragraph(f"<b>Success Profile:</b> {rs.success_profile}", styles["BriefBody"]))

    # 5. Hiring Priorities
    el.append(Paragraph("Hiring Priorities", styles["SectionHead"]))
    for hp in report.hiring_priorities:
        el.append(Paragraph(f"<b>[{hp.importance_score}/5]</b> {hp.priority}", styles["BriefBold"]))
        el.append(Paragraph(hp.why_it_matters, styles["BriefSmall"]))

    # 6. Fit Analysis
    el.append(Paragraph("Fit Analysis", styles["SectionHead"]))
    if report.fit_analysis.strong_fit_signals:
        el.append(Paragraph("Strong Fit", styles["SubHead"]))
        for s in report.fit_analysis.strong_fit_signals:
            el.append(Paragraph(f"<b>[{s.strength_score}/10]</b> {s.signal}", styles["BriefBold"]))
            el.append(Paragraph(s.evidence, styles["BriefSmall"]))
    if report.fit_analysis.partial_fit_signals:
        el.append(Paragraph("Partial Fit", styles["SubHead"]))
        for s in report.fit_analysis.partial_fit_signals:
            el.append(Paragraph(f"<b>[{s.strength_score}/10]</b> {s.signal}", styles["BriefBold"]))
            el.append(Paragraph(s.evidence, styles["BriefSmall"]))
    if report.fit_analysis.missing_or_weak_signals:
        el.append(Paragraph("Gaps", styles["SubHead"]))
        for s in report.fit_analysis.missing_or_weak_signals:
            el.append(Paragraph(f"<b>[{s.gap_severity.upper()}]</b> {s.signal}", styles["BriefBold"]))
            el.append(Paragraph(s.why_it_matters, styles["BriefSmall"]))

    # 7. Concerns & Mitigation
    el.append(Paragraph("Concerns & Mitigation", styles["SectionHead"]))
    for c in report.concerns_and_mitigation:
        el.append(Paragraph(f"<b>[{c.severity.upper()}]</b> {c.concern}", styles["BriefBold"]))
        el.append(Paragraph(f"Why: {c.why_they_may_care}", styles["BriefSmall"]))
        el.append(Paragraph(f"Mitigation: {c.mitigation_strategy}", styles["BriefBody"]))
        el.append(Paragraph(f"Best proof: {c.best_proof_to_use}", styles["BriefSmall"]))
        el.append(Spacer(1, 4))

    # 8. Resume Tailoring
    el.append(Paragraph("Resume Tailoring", styles["SectionHead"]))
    rt = report.resume_tailoring
    el.append(Paragraph(f"<b>Verdict:</b> {rt.resume_verdict.replace('_', ' ').title()}", styles["BriefBold"]))
    if rt.positioning_angle:
        el.append(Paragraph(f"<b>Positioning:</b> {rt.positioning_angle}", styles["BriefBody"]))
    for edit in rt.priority_edits:
        el.append(Paragraph(f"<b>[{edit.type.replace('_', ' ')}]</b> {edit.target}: {edit.recommendation}", styles["BriefBody"]))
    if rt.missing_keywords:
        el.append(Paragraph(f"<b>Missing Keywords:</b> {', '.join(rt.missing_keywords)}", styles["BriefBody"]))

    # 9. Application Strategy
    el.append(Paragraph("Application Strategy", styles["SectionHead"]))
    app_s = report.application_strategy
    el.append(Paragraph(f"<b>Apply Now:</b> {'Yes' if app_s.apply_now else 'No'} | <b>Referral:</b> {'Recommended' if app_s.referral_recommended else 'Not required'}", styles["BriefBold"]))
    if app_s.outreach_angle:
        el.append(Paragraph(f"<b>Outreach:</b> {app_s.outreach_angle}", styles["BriefBody"]))
    if app_s.suggested_connection_note:
        el.append(Paragraph(f"<b>Connection Note:</b> \"{app_s.suggested_connection_note}\"", styles["BriefBody"]))

    # 10. Recruiter Screen Prep
    el.append(Paragraph("Recruiter Screen Prep", styles["SectionHead"]))
    rp = report.recruiter_screen_prep
    for s in rp.what_they_will_likely_screen_for:
        el.append(Paragraph(f"• {s}", styles["BriefBody"]))
    for q in rp.likely_recruiter_questions:
        el.append(Paragraph(f"<b>{q.question}</b>", styles["BriefBold"]))
        el.append(Paragraph(f"Intent: {q.intent}", styles["BriefSmall"]))
        for p in q.suggested_answer_points:
            el.append(Paragraph(f"  • {p}", styles["BriefSmall"]))
        el.append(Spacer(1, 4))

    # 11. Story Bank
    el.append(Paragraph("Story Bank", styles["SectionHead"]))
    for s in report.story_bank:
        el.append(Paragraph(f"<b>{s.story_title}</b>", styles["BriefBold"]))
        el.append(Paragraph(f"Experience: {s.recommended_experience} | Angle: {s.angle_to_emphasize}", styles["BriefSmall"]))
        if s.key_metrics_or_outcomes:
            el.append(Paragraph(f"Metrics: {', '.join(s.key_metrics_or_outcomes)}", styles["BriefSmall"]))
        el.append(Spacer(1, 4))

    # 12. Interview Rounds
    el.append(Paragraph("Interview Round Strategy", styles["SectionHead"]))
    for rd in report.interview_rounds:
        el.append(Paragraph(f"<b>{rd.round_name.replace('_', ' ').title()}</b>", styles["BriefBold"]))
        el.append(Paragraph(rd.round_goal, styles["BriefBody"]))
        for p in rd.candidate_focus:
            el.append(Paragraph(f"  • {p}", styles["BriefSmall"]))
        el.append(Spacer(1, 4))

    # 13. Interview Questions
    el.append(Paragraph("Likely Interview Questions", styles["SectionHead"]))
    for q in report.likely_interview_questions:
        el.append(Paragraph(f"<b>[{q.category.replace('_', ' ').title()}]</b> {q.question}", styles["BriefBold"]))
        el.append(Paragraph(q.why_they_may_ask, styles["BriefSmall"]))
        if q.best_story_or_topic:
            el.append(Paragraph(f"Best story/topic: {q.best_story_or_topic}", styles["BriefSmall"]))
        el.append(Spacer(1, 4))

    # 14. Reverse Interview Questions
    el.append(Paragraph("Reverse-Interview Questions", styles["SectionHead"]))
    for q in report.reverse_interview_questions:
        el.append(Paragraph(f"<b>[{q.target_interviewer.replace('_', ' ').title()}]</b> {q.question}", styles["BriefBold"]))
        el.append(Paragraph(q.why_ask_this, styles["BriefSmall"]))
        el.append(Spacer(1, 4))

    # 15. Logistics
    el.append(Paragraph("Logistics & Constraints", styles["SectionHead"]))
    lg = report.logistics_and_constraints
    el.append(Paragraph(f"<b>Work Model:</b> {lg.work_model.title()} | <b>Level Clarity:</b> {lg.level_clarity.title()}", styles["BriefBody"]))
    if lg.location_notes:
        el.append(Paragraph(f"<b>Location:</b> {lg.location_notes}", styles["BriefBody"]))
    if lg.compensation_signal:
        el.append(Paragraph(f"<b>Compensation:</b> {lg.compensation_signal}", styles["BriefBody"]))
    if lg.timeline_signal:
        el.append(Paragraph(f"<b>Timeline:</b> {lg.timeline_signal}", styles["BriefBody"]))

    # 16. Red Flags & Unknowns
    el.append(Paragraph("Red Flags & Unknowns", styles["SectionHead"]))
    for f in report.red_flags_and_unknowns.red_flags:
        el.append(Paragraph(f"<b>[{f.severity.upper()}]</b> {f.flag}", styles["BriefBold"]))
        el.append(Paragraph(f.why_it_matters, styles["BriefSmall"]))
    if report.red_flags_and_unknowns.unknowns_to_verify:
        el.append(Paragraph("Unknowns to Verify", styles["SubHead"]))
        for u in report.red_flags_and_unknowns.unknowns_to_verify:
            el.append(Paragraph(f"• {u}", styles["BriefBody"]))

    # 17. Immediate Next Actions
    el.append(Paragraph("Immediate Next Actions", styles["SectionHead"]))
    for a in sorted(report.immediate_next_actions, key=lambda x: x.priority):
        time_str = f" (~{a.time_estimate_minutes}m)" if a.time_estimate_minutes else ""
        el.append(Paragraph(f"<b>{a.priority}.</b> {a.action}{time_str}", styles["BriefBold"]))
        el.append(Paragraph(a.why, styles["BriefSmall"]))

    # 18. Prep Checklist
    el.append(Paragraph("Preparation Checklist", styles["SectionHead"]))
    for item in report.prep_checklist:
        el.append(Paragraph(f"☐ {item.item}", styles["BriefBody"]))

    # Footer
    el.append(Spacer(1, 24))
    el.append(HRFlowable(width="100%", color=MUTED, thickness=0.5))
    el.append(Paragraph(
        "Generated by PrepLens",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8, textColor=MUTED, alignment=1),
    ))

    doc.build(el)
    return buffer.getvalue()
