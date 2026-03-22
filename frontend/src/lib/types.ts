// --- Nested types ---

export interface InputSummary {
  company_name: string;
  job_title: string;
  job_posting_url: string | null;
  resume_filename: string | null;
  candidate_notes_present: boolean;
  job_description_present: boolean;
  job_description_length: number;
}

export interface ExecutiveSummary {
  headline: string;
  summary: string;
  top_takeaways: string[];
}

export interface PursuitRecommendation {
  overall_fit_score: number;
  confidence_score: number;
  recommendation:
    | "pursue"
    | "pursue_selectively"
    | "low_priority"
    | "insufficient_information";
  reasoning: string[];
  ideal_candidate_profile: string;
  candidate_outlook: string;
}

export interface CompanySnapshot {
  company_overview: string;
  business_model: string | null;
  product_focus: string | null;
  engineering_signals: string[];
  company_stage:
    | "startup"
    | "growth"
    | "enterprise"
    | "public"
    | "unknown";
  risk_level: "low" | "medium" | "high" | "unknown";
  notable_unknowns: string[];
}

export interface RoleSnapshot {
  role_summary: string;
  seniority_signal: "junior" | "mid" | "senior" | "staff" | "unknown";
  core_domain: string[];
  primary_stack_signals: string[];
  success_profile: string;
}

export interface HiringPriority {
  priority: string;
  why_it_matters: string;
  importance_score: number;
}

export interface FitSignal {
  signal: string;
  evidence: string;
  strength_score: number;
}

export interface WeakSignal {
  signal: string;
  why_it_matters: string;
  gap_severity: "low" | "medium" | "high";
}

export interface FitAnalysis {
  strong_fit_signals: FitSignal[];
  partial_fit_signals: FitSignal[];
  missing_or_weak_signals: WeakSignal[];
}

export interface ConcernItem {
  concern: string;
  why_they_may_care: string;
  severity: "low" | "medium" | "high";
  mitigation_strategy: string;
  best_proof_to_use: string;
  sample_response: string;
}

export interface ResumePriorityEdit {
  type: string;
  target: string;
  recommendation: string;
  why: string;
}

export interface BulletToEmphasize {
  experience_area: string;
  why: string;
}

export interface ResumeTailoring {
  resume_verdict:
    | "good_to_apply"
    | "tailor_before_applying"
    | "needs_significant_rewrite";
  priority_edits: ResumePriorityEdit[];
  missing_keywords: string[];
  bullets_to_emphasize: BulletToEmphasize[];
  positioning_angle: string;
}

export interface ApplicationStrategy {
  apply_now: boolean;
  referral_recommended: boolean;
  best_outreach_target: string;
  outreach_angle: string;
  suggested_connection_note: string;
  suggested_email_angle: string;
}

export interface RecruiterQuestion {
  question: string;
  intent: string;
  suggested_answer_points: string[];
}

export interface RecruiterScreenPrep {
  what_they_will_likely_screen_for: string[];
  likely_recruiter_questions: RecruiterQuestion[];
  work_auth_notes: string | null;
  compensation_notes: string | null;
  availability_notes: string | null;
}

export interface StoryBankItem {
  story_title: string;
  best_for_questions: string[];
  recommended_experience: string;
  angle_to_emphasize: string;
  key_metrics_or_outcomes: string[];
  likely_follow_up_questions: string[];
}

export interface InterviewRound {
  round_name: string;
  round_goal: string;
  what_they_will_likely_probe: string[];
  best_stories_to_prepare: string[];
  candidate_focus: string[];
}

export interface InterviewQuestion {
  question: string;
  category: string;
  why_they_may_ask: string;
  best_story_or_topic: string;
}

export interface ReverseInterviewQuestion {
  target_interviewer: string;
  question: string;
  why_ask_this: string;
  good_answer_signals: string[];
  bad_answer_signals: string[];
  follow_up_question: string | null;
}

export interface LogisticsAndConstraints {
  work_model: "remote" | "hybrid" | "onsite" | "unknown";
  location_notes: string | null;
  visa_or_work_auth_signal: string | null;
  level_clarity: "clear" | "unclear" | "unknown";
  compensation_signal: string | null;
  timeline_signal: string | null;
}

export interface RedFlag {
  flag: string;
  severity: "low" | "medium" | "high";
  why_it_matters: string;
}

export interface RedFlagsAndUnknowns {
  red_flags: RedFlag[];
  unknowns_to_verify: string[];
}

export interface ImmediateNextAction {
  priority: number;
  action: string;
  why: string;
  time_estimate_minutes: number;
}

export interface PrepChecklistItem {
  item: string;
  completed: boolean;
}

export interface ExportMetadata {
  export_title: string;
  export_subtitle: string;
  export_date: string;
  branding: string;
}

// --- Top-level report ---

export interface PrepLensReportV2 {
  schema_version: string;
  generated_at: string;
  report_id: string;
  product_name: string;
  input_summary: InputSummary;
  executive_summary: ExecutiveSummary;
  pursuit_recommendation: PursuitRecommendation;
  company_snapshot: CompanySnapshot;
  role_snapshot: RoleSnapshot;
  hiring_priorities: HiringPriority[];
  fit_analysis: FitAnalysis;
  concerns_and_mitigation: ConcernItem[];
  resume_tailoring: ResumeTailoring;
  application_strategy: ApplicationStrategy;
  recruiter_screen_prep: RecruiterScreenPrep;
  story_bank: StoryBankItem[];
  interview_rounds: InterviewRound[];
  likely_interview_questions: InterviewQuestion[];
  reverse_interview_questions: ReverseInterviewQuestion[];
  logistics_and_constraints: LogisticsAndConstraints;
  red_flags_and_unknowns: RedFlagsAndUnknowns;
  immediate_next_actions: ImmediateNextAction[];
  prep_checklist: PrepChecklistItem[];
  export_metadata: ExportMetadata;
}

// --- API wrappers ---

export interface AnalyzeResponse {
  report: PrepLensReportV2;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
}
