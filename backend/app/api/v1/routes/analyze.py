from fastapi import APIRouter, File, Form, UploadFile, HTTPException

from app.core.config import settings
from app.services.resume_parser import extract_text_from_pdf

router = APIRouter()

MAX_JD_CHARS = 30_000
MAX_NOTES_CHARS = 5_000


@router.post("/analyze")
async def analyze(
    company_name: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
    recruiter_notes: str = Form(""),
    company_notes: str = Form(""),
):
    # Validate text inputs
    if not company_name.strip():
        raise HTTPException(status_code=400, detail="Company name is required.")
    if not job_title.strip():
        raise HTTPException(status_code=400, detail="Job title is required.")
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")
    if len(job_description) > MAX_JD_CHARS:
        raise HTTPException(status_code=400, detail=f"Job description exceeds {MAX_JD_CHARS} characters.")
    if len(recruiter_notes) > MAX_NOTES_CHARS:
        raise HTTPException(status_code=400, detail=f"Recruiter notes exceed {MAX_NOTES_CHARS} characters.")
    if len(company_notes) > MAX_NOTES_CHARS:
        raise HTTPException(status_code=400, detail=f"Company notes exceed {MAX_NOTES_CHARS} characters.")

    # Validate file
    if not resume_file.filename:
        raise HTTPException(status_code=400, detail="Resume file is required.")
    if not resume_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Only PDF resumes are supported.")
    if resume_file.content_type and "pdf" not in resume_file.content_type:
        raise HTTPException(status_code=415, detail="Only PDF resumes are supported.")

    # Read and validate file size
    file_bytes = await resume_file.read()
    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(status_code=413, detail=f"Resume file exceeds {settings.MAX_UPLOAD_MB}MB limit.")

    # Extract resume text
    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception:
        raise HTTPException(status_code=422, detail="Failed to parse the resume PDF.")

    # Placeholder: will call AI service in Milestone 3
    return {
        "status": "parsed",
        "resume_text_length": len(resume_text),
        "company_name": company_name.strip(),
        "job_title": job_title.strip(),
    }
