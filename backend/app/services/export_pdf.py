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

from app.models.report_schema import DossierReport

PRIMARY = HexColor("#4f46e5")
MUTED = HexColor("#64748b")


def generate_pdf(report: DossierReport) -> bytes:
    """Generate a PDF file from a DossierReport."""
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

    # Custom styles
    styles.add(
        ParagraphStyle(
            "BriefTitle",
            parent=styles["Title"],
            fontSize=20,
            textColor=PRIMARY,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            "BriefMeta",
            parent=styles["Normal"],
            fontSize=11,
            textColor=MUTED,
            alignment=1,
            spaceAfter=20,
        )
    )
    styles.add(
        ParagraphStyle(
            "SectionHead",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=PRIMARY,
            spaceBefore=16,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            "BriefBody",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            "BriefBold",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            spaceAfter=2,
        )
    )

    elements = []

    # Title
    elements.append(
        Paragraph("PrepLens Interview Strategy Brief", styles["BriefTitle"])
    )
    elements.append(
        Paragraph(
            f"{report.report_meta.company_name} — {report.report_meta.job_title}<br/>"
            f"Generated: {report.report_meta.generated_at[:10]}",
            styles["BriefMeta"],
        )
    )
    elements.append(HRFlowable(width="100%", color=PRIMARY, thickness=1))
    elements.append(Spacer(1, 12))

    # Role Summary
    elements.append(Paragraph("Role Summary", styles["SectionHead"]))
    elements.append(Paragraph(report.role_summary, styles["BriefBody"]))

    # Hiring Priorities
    elements.append(Paragraph("Likely Hiring Priorities", styles["SectionHead"]))
    items = [
        ListItem(Paragraph(p, styles["BriefBody"]))
        for p in report.hiring_priorities
    ]
    elements.append(ListFlowable(items, bulletType="1", start=1))

    # Strengths
    elements.append(Paragraph("Your Strongest Alignment", styles["SectionHead"]))
    items = [
        ListItem(Paragraph(s, styles["BriefBody"]))
        for s in report.candidate_strengths
    ]
    elements.append(ListFlowable(items, bulletType="bullet"))

    # Concerns
    elements.append(Paragraph("Likely Concerns & Gaps", styles["SectionHead"]))
    for c in report.candidate_concerns:
        elements.append(
            Paragraph(
                f"<b>[{c.severity.upper()}]</b> {c.concern}",
                styles["BriefBold"],
            )
        )
        elements.append(
            Paragraph(f"Mitigation: {c.mitigation}", styles["BriefBody"])
        )
        elements.append(Spacer(1, 4))

    # Interview Questions
    elements.append(
        Paragraph("Likely Interview Questions", styles["SectionHead"])
    )
    for q in report.likely_interview_questions:
        elements.append(Paragraph(f"<b>{q.question}</b>", styles["BriefBold"]))
        elements.append(
            Paragraph(q.why_they_might_ask, styles["BriefBody"])
        )
        elements.append(Spacer(1, 4))

    # Reverse Questions
    elements.append(
        Paragraph("Reverse-Interview Questions", styles["SectionHead"])
    )
    for q in report.reverse_interview_questions:
        elements.append(
            Paragraph(
                f"<b>[{q.audience}]</b> {q.question}", styles["BriefBold"]
            )
        )
        elements.append(Paragraph(q.why_it_matters, styles["BriefBody"]))
        elements.append(Spacer(1, 4))

    # Positioning
    elements.append(Paragraph("Positioning Strategy", styles["SectionHead"]))
    items = [
        ListItem(Paragraph(s, styles["BriefBody"]))
        for s in report.positioning_strategy
    ]
    elements.append(ListFlowable(items, bulletType="bullet"))

    # Red Flags
    elements.append(Paragraph("Red Flags & Unknowns", styles["SectionHead"]))
    items = [
        ListItem(Paragraph(r, styles["BriefBody"]))
        for r in report.red_flags_or_unknowns
    ]
    elements.append(ListFlowable(items, bulletType="bullet"))

    # Checklist
    elements.append(Paragraph("Preparation Checklist", styles["SectionHead"]))
    for item in report.prep_checklist:
        elements.append(Paragraph(f"☐ {item}", styles["BriefBody"]))

    # Footer
    elements.append(Spacer(1, 24))
    elements.append(HRFlowable(width="100%", color=MUTED, thickness=0.5))
    elements.append(
        Paragraph(
            "Generated by PrepLens",
            ParagraphStyle(
                "Footer",
                parent=styles["Normal"],
                fontSize=8,
                textColor=MUTED,
                alignment=1,
            ),
        )
    )

    doc.build(elements)
    return buffer.getvalue()
