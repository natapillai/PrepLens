# PrepLens

**See how they'll evaluate you — and how to evaluate them back.**

PrepLens is a job-search strategy assistant that converts your resume, a job description, and company context into a comprehensive decision and interview-prep dossier. No account required.

## What It Does

1. Upload your resume (PDF) and paste a job description
2. PrepLens analyzes the match using AI
3. Get a structured V2 strategy dossier with 18 sections:
   - Executive summary and pursuit recommendation (with fit/confidence scores)
   - Company and role snapshots
   - Hiring priorities with importance scoring
   - Fit analysis (strong, partial, and gap signals)
   - Concerns with mitigation strategies and sample responses
   - Resume tailoring suggestions with missing keywords
   - Application strategy and outreach recommendations
   - Recruiter screen prep with likely questions
   - Story bank mapping for behavioral interviews
   - Interview round strategy by stage
   - Likely interview questions by category
   - Reverse-interview questions with good/bad answer signals
   - Logistics and constraints
   - Red flags and unknowns to verify
   - Immediate next actions with time estimates
   - Preparation checklist
4. Export as PDF or DOCX

## Stack

| Layer    | Technology                         |
| -------- | ---------------------------------- |
| Frontend | Next.js, TypeScript, Tailwind CSS  |
| Backend  | FastAPI, Python 3.12, Pydantic     |
| AI       | OpenAI API (structured JSON output)|
| Export   | python-docx (DOCX), ReportLab (PDF)|

## Local Setup

### Prerequisites

- Node.js 18+
- Python 3.12+
- An OpenAI API key

### 1. Clone and configure environment

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Docker (alternative)

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
docker-compose up
```

## Environment Variables

| Variable                   | Required | Default              | Description              |
| -------------------------- | -------- | -------------------- | ------------------------ |
| `OPENAI_API_KEY`           | Yes      |                      | OpenAI API key           |
| `OPENAI_MODEL`             | No       | `gpt-4o-mini`        | Model for generation     |
| `NEXT_PUBLIC_API_BASE_URL` | No       | `http://localhost:8000` | Backend URL for frontend |
| `MAX_UPLOAD_MB`            | No       | `5`                  | Max resume file size     |
| `CORS_ALLOWED_ORIGINS`     | No       | `http://localhost:3000` | Allowed CORS origins   |

## Testing

### Backend tests

```bash
cd backend
python -m pytest tests/ -v
```

### Frontend build check

```bash
cd frontend
npm run build
```

## Export

Both export endpoints accept the canonical V2 report JSON and return a file:

- **PDF**: `POST /api/v1/export/pdf` — branded PDF with all 18 sections
- **DOCX**: `POST /api/v1/export/docx` — styled Word document with all 18 sections

Exports are triggered from the results page UI via the Download buttons.

## API Endpoints

| Method | Path                  | Description              |
| ------ | --------------------- | ------------------------ |
| GET    | `/api/v1/health`      | Health check             |
| POST   | `/api/v1/analyze`     | Generate V2 strategy dossier |
| POST   | `/api/v1/export/pdf`  | Export dossier as PDF    |
| POST   | `/api/v1/export/docx` | Export dossier as DOCX   |

## Architecture

```
Browser → Next.js Frontend → FastAPI Backend → OpenAI API
                                    ↓
                            Export (PDF/DOCX)
```

- **Stateless**: No database, no accounts. Reports live in browser sessionStorage.
- **Schema-driven**: One canonical `PrepLensReportV2` schema powers UI rendering, PDF, and DOCX.
- **Separation of concerns**: Route handlers are thin; business logic lives in services.

## V2 Report Schema

The V2 dossier answers four primary questions:

1. **Should I pursue this role?** — Executive summary, pursuit recommendation, company/role snapshots
2. **How should I tailor my application?** — Resume tailoring, application strategy, missing keywords
3. **How should I position myself?** — Story bank, interview rounds, concerns with mitigations
4. **What should I do next?** — Immediate next actions with priorities and time estimates

All sections use validated Pydantic models with scoring conventions:
- Fit/confidence scores: 0-10
- Importance scores: 1-5
- Strength scores: 1-10
- Severity levels: low/medium/high

## Project Structure

```
PrepLens/
  frontend/           # Next.js app
    src/
      app/            # Pages: /, /new, /results
      components/     # UI components (brief/, forms/)
      lib/            # API client, types, utilities
  backend/            # FastAPI app
    app/
      api/v1/routes/  # health, analyze, export
      core/           # config
      models/         # Pydantic V2 schemas
      prompts/        # AI prompt templates
      services/       # resume_parser, report_generator, export_*
    tests/            # pytest tests (16 tests)
```
