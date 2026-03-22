# PrepLens

**See how they'll evaluate you — and how to evaluate them back.**

PrepLens is an interview strategy generator that converts your resume, a job description, and company context into a structured interview-prep dossier. No account required.

## What It Does

1. Upload your resume (PDF) and paste a job description
2. PrepLens analyzes the match using AI
3. Get a structured strategy brief with:
   - Role summary and likely hiring priorities
   - Your strongest alignment points
   - Likely concerns and how to mitigate them
   - Probable interview questions with reasoning
   - Reverse-interview questions to ask
   - Positioning strategy
   - Red flags to investigate
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

Both export endpoints accept the canonical report JSON and return a file:

- **PDF**: `POST /api/v1/export/pdf` — branded PDF with sections and checklist
- **DOCX**: `POST /api/v1/export/docx` — styled Word document

Exports are triggered from the results page UI via the Download buttons.

## API Endpoints

| Method | Path                  | Description              |
| ------ | --------------------- | ------------------------ |
| GET    | `/api/v1/health`      | Health check             |
| POST   | `/api/v1/analyze`     | Generate strategy brief  |
| POST   | `/api/v1/export/pdf`  | Export brief as PDF      |
| POST   | `/api/v1/export/docx` | Export brief as DOCX     |

## Architecture

```
Browser → Next.js Frontend → FastAPI Backend → OpenAI API
                                    ↓
                            Export (PDF/DOCX)
```

- **Stateless**: No database, no accounts. Reports live in browser sessionStorage.
- **Schema-driven**: One canonical `DossierReport` schema powers UI rendering, PDF, and DOCX.
- **Separation of concerns**: Route handlers are thin; business logic lives in services.

## Project Structure

```
PrepLens/
  frontend/           # Next.js app
    src/
      app/            # Pages: /, /new, /results
      components/     # UI components
      lib/            # API client, types, utilities
  backend/            # FastAPI app
    app/
      api/v1/routes/  # health, analyze, export
      core/           # config
      models/         # Pydantic schemas
      prompts/        # AI prompt templates
      services/       # resume_parser, report_generator, export_*
    tests/            # pytest tests
```
