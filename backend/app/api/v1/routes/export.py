from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.models.report_schema import ExportRequest
from app.services.export_docx import generate_docx
from app.services.export_pdf import generate_pdf

router = APIRouter()


@router.post("/export/docx")
async def export_docx(request: ExportRequest):
    try:
        file_bytes = generate_docx(request.report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DOCX export failed: {str(e)}")

    company = request.report.report_meta.company_name.replace(" ", "_")
    role = request.report.report_meta.job_title.replace(" ", "_")
    filename = f"PrepLens_{company}_{role}.docx"

    return Response(
        content=file_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/export/pdf")
async def export_pdf(request: ExportRequest):
    try:
        file_bytes = generate_pdf(request.report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")

    company = request.report.report_meta.company_name.replace(" ", "_")
    role = request.report.report_meta.job_title.replace(" ", "_")
    filename = f"PrepLens_{company}_{role}.pdf"

    return Response(
        content=file_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
