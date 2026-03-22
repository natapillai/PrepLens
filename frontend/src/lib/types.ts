export interface ReportMeta {
  company_name: string;
  job_title: string;
  generated_at: string;
  version: string;
}

export interface InterviewQuestion {
  question: string;
  why_they_might_ask: string;
}

export interface ReverseQuestion {
  audience: "Recruiter" | "Hiring Manager" | "Engineer";
  question: string;
  why_it_matters: string;
}

export interface CandidateConcern {
  concern: string;
  severity: "low" | "medium" | "high";
  mitigation: string;
}

export interface DossierReport {
  report_meta: ReportMeta;
  role_summary: string;
  hiring_priorities: string[];
  candidate_strengths: string[];
  candidate_concerns: CandidateConcern[];
  likely_interview_questions: InterviewQuestion[];
  reverse_interview_questions: ReverseQuestion[];
  positioning_strategy: string[];
  red_flags_or_unknowns: string[];
  prep_checklist: string[];
}

export interface AnalyzeResponse {
  report: DossierReport;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
}
