import io
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Image,
    Table,
    TableStyle,
    KeepTogether,
    PageBreak,
)

from app.models.report_schema import PrepLensReportV2

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LOGO_PATH = ASSETS / "logo.png"

PRIMARY = HexColor("#4f46e5")
PRIMARY_LIGHT = HexColor("#e0e7ff")
DARK = HexColor("#1e293b")
MUTED = HexColor("#64748b")
LIGHT_GRAY = HexColor("#f1f5f9")
BORDER = HexColor("#cbd5e1")
EMERALD = HexColor("#059669")
EMERALD_BG = HexColor("#ecfdf5")
AMBER = HexColor("#d97706")
AMBER_BG = HexColor("#fffbeb")
RED = HexColor("#dc2626")
RED_BG = HexColor("#fef2f2")
WHITE = HexColor("#ffffff")


def _score_color(score: float, max_val: float = 10) -> Color:
    ratio = score / max_val
    if ratio >= 0.7:
        return EMERALD
    elif ratio >= 0.4:
        return AMBER
    return RED


def _severity_color(severity: str) -> Color:
    return {"high": RED, "medium": AMBER, "low": EMERALD}.get(severity, MUTED)


def generate_pdf(report: PrepLensReportV2) -> bytes:
    """Generate a professionally styled PDF from a PrepLensReportV2."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )

    styles = getSampleStyleSheet()

    # --- Custom styles ---
    styles.add(ParagraphStyle(
        "DocTitle", parent=styles["Title"], fontSize=22, textColor=PRIMARY,
        spaceAfter=2, alignment=TA_CENTER, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "DocSubtitle", parent=styles["Normal"], fontSize=12, textColor=DARK,
        alignment=TA_CENTER, spaceAfter=2, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "DocMeta", parent=styles["Normal"], fontSize=9, textColor=MUTED,
        alignment=TA_CENTER, spaceAfter=16,
    ))
    styles.add(ParagraphStyle(
        "SectionHead", parent=styles["Heading2"], fontSize=13, textColor=PRIMARY,
        spaceBefore=18, spaceAfter=8, fontName="Helvetica-Bold",
        borderPadding=(0, 0, 4, 0),
    ))
    styles.add(ParagraphStyle(
        "SubHead", parent=styles["Heading3"], fontSize=10.5, textColor=DARK,
        spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "Body", parent=styles["Normal"], fontSize=9.5, leading=13.5,
        spaceAfter=4, textColor=DARK,
    ))
    styles.add(ParagraphStyle(
        "BodyBold", parent=styles["Normal"], fontSize=9.5, leading=13.5,
        spaceAfter=2, textColor=DARK, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "Detail", parent=styles["Normal"], fontSize=8.5, leading=12,
        textColor=MUTED, spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        "BulletItem", parent=styles["Normal"], fontSize=9.5, leading=13.5,
        textColor=DARK, leftIndent=14, spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        "Footer", parent=styles["Normal"], fontSize=7.5, textColor=MUTED,
        alignment=TA_CENTER,
    ))

    el = []
    meta = report.input_summary

    # ── HEADER WITH LOGO ──
    if LOGO_PATH.exists():
        logo = Image(str(LOGO_PATH), width=1.6 * inch, height=0.4 * inch)
        logo.hAlign = "CENTER"
        el.append(logo)
        el.append(Spacer(1, 8))

    el.append(Paragraph("Interview Strategy Dossier", styles["DocTitle"]))
    el.append(Paragraph(
        f"{meta.company_name}  ·  {meta.job_title}",
        styles["DocSubtitle"],
    ))
    el.append(Paragraph(
        f"Generated {report.generated_at[:10]}  ·  Report ID: {report.report_id[:8]}",
        styles["DocMeta"],
    ))
    el.append(HRFlowable(width="100%", color=PRIMARY, thickness=1.5))
    el.append(Spacer(1, 6))

    # ── SCORE SUMMARY BAR ──
    pr = report.pursuit_recommendation
    fit_color = _score_color(pr.overall_fit_score)
    conf_color = _score_color(pr.confidence_score)
    rec_label = pr.recommendation.replace("_", " ").title()

    def _score_cell(value: str, label: str, color: Color) -> Paragraph:
        return Paragraph(
            f'<font size="18" color="{color}"><b>{value}</b></font>'
            f'<br/><font size="8" color="{MUTED}">{label}</font>',
            ParagraphStyle("_sc", parent=styles["Normal"], alignment=TA_CENTER,
                           leading=22, spaceAfter=0, spaceBefore=0),
        )

    score_data = [[
        _score_cell(f"{pr.overall_fit_score}/10", "Overall Fit", fit_color),
        _score_cell(f"{pr.confidence_score}/10", "Confidence", conf_color),
        _score_cell(rec_label, "Recommendation", PRIMARY),
    ]]
    col_w = 2.2 * inch
    score_table = Table(score_data, colWidths=[col_w, col_w, col_w])
    score_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
        ("TOPPADDING", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        # vertical dividers between columns
        ("LINEAFTER", (0, 0), (0, -1), 0.5, BORDER),
        ("LINEAFTER", (1, 0), (1, -1), 0.5, BORDER),
    ]))
    el.append(score_table)
    el.append(Spacer(1, 10))

    def section(title: str):
        el.append(Spacer(1, 4))
        el.append(HRFlowable(width="100%", color=BORDER, thickness=0.5))
        el.append(Paragraph(title, styles["SectionHead"]))

    def sub(title: str):
        el.append(Paragraph(title, styles["SubHead"]))

    def body(text: str):
        el.append(Paragraph(text, styles["Body"]))

    def bold(text: str):
        el.append(Paragraph(text, styles["BodyBold"]))

    def detail(text: str):
        el.append(Paragraph(text, styles["Detail"]))

    def bullet(text: str):
        el.append(Paragraph(f"•  {text}", styles["BulletItem"]))

    def kv(key: str, value: str):
        el.append(Paragraph(f"<b>{key}:</b>  {value}", styles["Body"]))

    def spacer(h: int = 4):
        el.append(Spacer(1, h))

    # ── 1. EXECUTIVE SUMMARY ──
    section("1  Executive Summary")
    bold(report.executive_summary.headline)
    body(report.executive_summary.summary)
    for t in report.executive_summary.top_takeaways:
        bullet(t)

    # ── 2. PURSUIT RECOMMENDATION ──
    section("2  Pursuit Recommendation")
    kv("Ideal Candidate", pr.ideal_candidate_profile)
    kv("Your Outlook", pr.candidate_outlook)
    sub("Reasoning")
    for reason in pr.reasoning:
        bullet(reason)

    # ── 3. COMPANY SNAPSHOT ──
    section("3  Company Snapshot")
    cs = report.company_snapshot
    body(cs.company_overview)
    if cs.business_model:
        kv("Business Model", cs.business_model)
    if cs.product_focus:
        kv("Product Focus", cs.product_focus)
    if cs.company_stage != "unknown":
        kv("Stage", f"{cs.company_stage.title()}  ·  Risk: {cs.risk_level.title()}")
    if cs.engineering_signals:
        sub("Engineering Signals")
        for s in cs.engineering_signals:
            bullet(s)

    # ── 4. ROLE SNAPSHOT ──
    section("4  Role Snapshot")
    rs = report.role_snapshot
    body(rs.role_summary)
    if rs.seniority_signal != "unknown":
        kv("Seniority", rs.seniority_signal.title())
    if rs.primary_stack_signals:
        kv("Stack", ", ".join(rs.primary_stack_signals))
    if rs.success_profile:
        kv("Success Profile", rs.success_profile)

    # ── 5. HIRING PRIORITIES ──
    section("5  Hiring Priorities")
    for hp in report.hiring_priorities:
        color = _score_color(hp.importance_score, 5)
        el.append(Paragraph(
            f'<font color="{color}"><b>[{hp.importance_score}/5]</b></font>  <b>{hp.priority}</b>',
            styles["Body"],
        ))
        detail(hp.why_it_matters)
        spacer()

    # ── 6. FIT ANALYSIS ──
    section("6  Fit Analysis")
    if report.fit_analysis.strong_fit_signals:
        sub("Strong Fit")
        for s in report.fit_analysis.strong_fit_signals:
            color = _score_color(s.strength_score)
            el.append(Paragraph(
                f'<font color="{color}"><b>[{s.strength_score}/10]</b></font>  <b>{s.signal}</b>',
                styles["Body"],
            ))
            detail(s.evidence)
            spacer()
    if report.fit_analysis.partial_fit_signals:
        sub("Partial Fit")
        for s in report.fit_analysis.partial_fit_signals:
            color = _score_color(s.strength_score)
            el.append(Paragraph(
                f'<font color="{color}"><b>[{s.strength_score}/10]</b></font>  <b>{s.signal}</b>',
                styles["Body"],
            ))
            detail(s.evidence)
            spacer()
    if report.fit_analysis.missing_or_weak_signals:
        sub("Gaps")
        for s in report.fit_analysis.missing_or_weak_signals:
            color = _severity_color(s.gap_severity)
            el.append(Paragraph(
                f'<font color="{color}"><b>[{s.gap_severity.upper()}]</b></font>  <b>{s.signal}</b>',
                styles["Body"],
            ))
            detail(s.why_it_matters)
            spacer()

    # ── 7. CONCERNS & MITIGATION ──
    section("7  Concerns & Mitigation")
    for c in report.concerns_and_mitigation:
        color = _severity_color(c.severity)
        el.append(Paragraph(
            f'<font color="{color}"><b>[{c.severity.upper()}]</b></font>  <b>{c.concern}</b>',
            styles["Body"],
        ))
        detail(f"Why they may care: {c.why_they_may_care}")
        kv("Mitigation", c.mitigation_strategy)
        detail(f"Best proof: {c.best_proof_to_use}")
        spacer(6)

    # ── 8. RESUME TAILORING ──
    section("8  Resume Tailoring")
    rt = report.resume_tailoring
    kv("Verdict", rt.resume_verdict.replace("_", " ").title())
    if rt.positioning_angle:
        kv("Positioning", rt.positioning_angle)
    if rt.priority_edits:
        sub("Priority Edits")
        for edit in rt.priority_edits:
            el.append(Paragraph(
                f'<b>[{edit.type.replace("_", " ").title()}]</b>  {edit.target}',
                styles["BodyBold"],
            ))
            detail(edit.recommendation)
            spacer()
    if rt.missing_keywords:
        kv("Missing Keywords", ", ".join(rt.missing_keywords))

    # ── 9. APPLICATION STRATEGY ──
    section("9  Application Strategy")
    app_s = report.application_strategy
    kv("Apply Now", "Yes" if app_s.apply_now else "No")
    kv("Referral", "Recommended" if app_s.referral_recommended else "Not required")
    if app_s.outreach_angle:
        kv("Outreach Angle", app_s.outreach_angle)
    if app_s.suggested_connection_note:
        body(f'<i>"{app_s.suggested_connection_note}"</i>')

    # ── 10. RECRUITER SCREEN PREP ──
    section("10  Recruiter Screen Prep")
    rp = report.recruiter_screen_prep
    sub("Screening Focus Areas")
    for s in rp.what_they_will_likely_screen_for:
        bullet(s)
    sub("Likely Questions")
    for q in rp.likely_recruiter_questions:
        bold(q.question)
        detail(f"Intent: {q.intent}")
        for p in q.suggested_answer_points:
            bullet(p)
        spacer(4)

    # ── 11. STORY BANK ──
    section("11  Story Bank")
    for s in report.story_bank:
        bold(s.story_title)
        kv("Experience", s.recommended_experience)
        kv("Angle", s.angle_to_emphasize)
        if s.key_metrics_or_outcomes:
            kv("Metrics", ", ".join(s.key_metrics_or_outcomes))
        spacer(6)

    # ── 12. INTERVIEW ROUNDS ──
    section("12  Interview Round Strategy")
    for rd in report.interview_rounds:
        bold(rd.round_name.replace("_", " ").title())
        body(rd.round_goal)
        for f in rd.candidate_focus:
            bullet(f)
        spacer(4)

    # ── 13. INTERVIEW QUESTIONS ──
    section("13  Likely Interview Questions")
    for q in report.likely_interview_questions:
        el.append(Paragraph(
            f'<font color="{PRIMARY}"><b>[{q.category.replace("_", " ").title()}]</b></font>  {q.question}',
            styles["BodyBold"],
        ))
        detail(q.why_they_may_ask)
        if q.best_story_or_topic:
            detail(f"Best story/topic: {q.best_story_or_topic}")
        spacer(4)

    # ── 14. REVERSE INTERVIEW ──
    section("14  Reverse-Interview Questions")
    for q in report.reverse_interview_questions:
        el.append(Paragraph(
            f'<font color="{PRIMARY}"><b>[{q.target_interviewer.replace("_", " ").title()}]</b></font>  {q.question}',
            styles["BodyBold"],
        ))
        detail(q.why_ask_this)
        spacer(4)

    # ── 15. LOGISTICS ──
    section("15  Logistics & Constraints")
    lg = report.logistics_and_constraints
    kv("Work Model", lg.work_model.title())
    kv("Level Clarity", lg.level_clarity.title())
    if lg.location_notes:
        kv("Location", lg.location_notes)
    if lg.compensation_signal:
        kv("Compensation", lg.compensation_signal)
    if lg.timeline_signal:
        kv("Timeline", lg.timeline_signal)

    # ── 16. RED FLAGS ──
    section("16  Red Flags & Unknowns")
    for f in report.red_flags_and_unknowns.red_flags:
        color = _severity_color(f.severity)
        el.append(Paragraph(
            f'<font color="{color}"><b>[{f.severity.upper()}]</b></font>  <b>{f.flag}</b>',
            styles["Body"],
        ))
        detail(f.why_it_matters)
        spacer()
    if report.red_flags_and_unknowns.unknowns_to_verify:
        sub("Unknowns to Verify")
        for u in report.red_flags_and_unknowns.unknowns_to_verify:
            bullet(u)

    # ── 17. NEXT ACTIONS ──
    section("17  Immediate Next Actions")
    for a in sorted(report.immediate_next_actions, key=lambda x: x.priority):
        time_str = f"  (~{a.time_estimate_minutes} min)" if a.time_estimate_minutes else ""
        bold(f"{a.priority}.  {a.action}{time_str}")
        detail(a.why)
        spacer()

    # ── 18. PREP CHECKLIST ──
    section("18  Preparation Checklist")
    for item in report.prep_checklist:
        el.append(Paragraph(f"[ ]  {item.item}", styles["Body"]))

    # ── SCORING APPENDIX ──
    if report.scoring:
        _build_scoring_appendix(el, report.scoring, styles, section, sub, body, bold, detail, bullet, kv, spacer)

    # ── FOOTER ──
    el.append(Spacer(1, 28))
    el.append(HRFlowable(width="100%", color=BORDER, thickness=0.5))
    el.append(Spacer(1, 6))
    el.append(Paragraph(
        "Generated by PrepLens  ·  Confidential  ·  For candidate use only",
        styles["Footer"],
    ))

    doc.build(el)
    return buffer.getvalue()


def _build_scoring_appendix(el, scoring, styles, section, sub, body, bold, detail, bullet, kv, spacer):
    """Build the Score Methodology appendix page."""

    el.append(PageBreak())
    el.append(HRFlowable(width="100%", color=PRIMARY, thickness=1.5))
    el.append(Spacer(1, 6))
    el.append(Paragraph("Appendix: Score Methodology", styles["DocTitle"]))
    el.append(Paragraph(
        "Transparent, ATS-style scoring breakdown — every score is traceable to evidence.",
        styles["DocMeta"],
    ))
    el.append(HRFlowable(width="100%", color=PRIMARY, thickness=1.5))
    el.append(Spacer(1, 10))

    # -- Overall Score Summary --
    section("Overall Score")
    fit_score = scoring.get("overall_fit_score", 0)
    fit_pct = scoring.get("overall_fit_percentage", 0)
    earned = scoring.get("total_earned_points", 0)
    max_pts = scoring.get("total_max_points", 0)

    body(
        f'<b>Overall Fit: <font color="{_score_color(fit_score)}">'
        f"{fit_score}/10</font></b> ({fit_pct}% match)"
    )
    body(f"Total Points: {earned} earned out of {max_pts} possible")
    body(
        "Score = weighted sum of category scores. Each category is scored independently "
        "based on keyword matching between the job description and resume, then weighted "
        "by the category's importance for this specific role."
    )
    spacer(6)

    # -- Confidence Breakdown --
    confidence = scoring.get("confidence", {})
    if confidence:
        section("Confidence Score")
        conf_overall = confidence.get("overall_confidence", 0)
        body(
            f'<b>Overall Confidence: <font color="{_score_color(conf_overall)}">'
            f"{conf_overall}/10</font></b>"
        )
        spacer(4)

        for factor, label in [
            ("jd_specificity", "Job Description Specificity"),
            ("resume_detail", "Resume Detail Level"),
            ("match_clarity", "Match Clarity"),
        ]:
            score_val = confidence.get(factor, 0)
            reasoning = confidence.get(f"{factor}_reasoning", "")
            color = _score_color(score_val)
            bold(f'{label}: <font color="{color}">{score_val}/10</font>')
            detail(reasoning)
            spacer(4)

    # -- Category Breakdown --
    category_scores = scoring.get("category_scores", [])
    if category_scores:
        section("Category Breakdown")
        body(
            "Each category is weighted based on what the job description emphasizes. "
            "The weighted contribution shows how much each category affects the overall score."
        )
        spacer(6)

        # Category summary table
        cat_header = [
            Paragraph("<b>Category</b>", styles["Body"]),
            Paragraph("<b>Score</b>", styles["Body"]),
            Paragraph("<b>Match %</b>", styles["Body"]),
            Paragraph("<b>Weight</b>", styles["Body"]),
            Paragraph("<b>Contribution</b>", styles["Body"]),
        ]
        cat_rows = [cat_header]
        for cs in category_scores:
            color = _score_color(cs["score_out_of_10"])
            cat_rows.append([
                Paragraph(cs.get("category_label", cs["category"]), styles["Body"]),
                Paragraph(
                    f'<font color="{color}"><b>{cs["score_out_of_10"]}/10</b></font>',
                    styles["Body"],
                ),
                Paragraph(f'{cs["percentage"]}%', styles["Body"]),
                Paragraph(f'{cs["category_weight"]}', styles["Body"]),
                Paragraph(f'{cs["weighted_contribution"]}', styles["Body"]),
            ])

        cat_table = Table(
            cat_rows,
            colWidths=[2.0 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch, 1.2 * inch],
        )
        cat_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_LIGHT),
            ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]))
        el.append(cat_table)
        spacer(10)

    # -- Detailed Requirements Table --
    scored_reqs = scoring.get("scored_requirements", [])
    if scored_reqs:
        section("Detailed Requirements Breakdown")
        body(
            "Every requirement extracted from the job description, matched against your resume. "
            "Weight is determined by importance: Required (5), Preferred (3), Nice-to-have (1)."
        )
        spacer(6)

        req_header = [
            Paragraph("<b>Requirement</b>", styles["Body"]),
            Paragraph("<b>Category</b>", styles["Body"]),
            Paragraph("<b>Importance</b>", styles["Body"]),
            Paragraph("<b>Match</b>", styles["Body"]),
            Paragraph("<b>Points</b>", styles["Body"]),
        ]
        req_rows = [req_header]

        match_icons = {"direct": "DIRECT", "partial": "PARTIAL", "none": "NONE"}
        match_colors = {"direct": EMERALD, "partial": AMBER, "none": RED}

        for req in scored_reqs:
            m_level = req.get("match_level", "none")
            m_color = match_colors.get(m_level, MUTED)
            req_rows.append([
                Paragraph(req["keyword"], styles["Body"]),
                Paragraph(
                    CATEGORY_LABELS_SHORT.get(req["category"], req["category"]),
                    styles["Detail"],
                ),
                Paragraph(req["importance"].replace("_", " ").title(), styles["Detail"]),
                Paragraph(
                    f'<font color="{m_color}"><b>{match_icons.get(m_level, m_level)}</b></font>',
                    styles["Body"],
                ),
                Paragraph(
                    f'{req["earned_points"]}/{req["max_points"]}',
                    styles["Body"],
                ),
            ])

        req_table = Table(
            req_rows,
            colWidths=[2.0 * inch, 1.2 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch],
        )
        req_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_LIGHT),
            ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
            ("ALIGN", (2, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]))
        el.append(req_table)
        spacer(10)

    # -- Evidence Details --
    if scored_reqs:
        section("Match Evidence")
        body("Detailed justification for each requirement match.")
        spacer(4)
        for req in scored_reqs:
            m_level = req.get("match_level", "none")
            m_color = match_colors.get(m_level, MUTED)
            bold(
                f'{req["keyword"]} — '
                f'<font color="{m_color}">{m_level.upper()}</font>'
            )
            detail(f"Evidence: {req.get('resume_evidence', 'N/A')}")
            detail(f"Reasoning: {req.get('match_reasoning', 'N/A')}")
            spacer(4)

    # -- Top Improvements --
    improvements = scoring.get("top_improvements", [])
    if improvements:
        section("Top Score Improvements")
        body("Changes that would have the biggest impact on your overall score.")
        spacer(4)
        for imp in improvements:
            bold(
                f'{imp["keyword"]} — +{imp["potential_points"]} pts '
                f'({imp["percentage_impact"]}% impact)'
            )
            detail(imp["suggestion"])
            spacer(4)


# Short category labels for the requirements table
CATEGORY_LABELS_SHORT = {
    "hard_skill": "Hard Skill",
    "soft_skill": "Soft Skill",
    "domain_knowledge": "Domain",
    "tool_or_technology": "Tool/Tech",
    "education": "Education",
}
