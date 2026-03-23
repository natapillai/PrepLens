"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  Target,
  Sparkles,
  AlertTriangle,
  MessageSquare,
  ArrowLeftRight,
  Compass,
  Flag,
  CheckSquare,
  FileText,
  Download,
  ArrowLeft,
  Building2,
  Briefcase,
  TrendingUp,
  FileEdit,
  Send,
  Phone,
  BookOpen,
  Layers,
  MapPin,
  Zap,
} from "lucide-react";
import type { PrepLensReportV2 } from "@/lib/types";
import { exportDossier } from "@/lib/api";
import { SectionCard } from "@/components/brief/section-card";
import { SidebarNav } from "@/components/brief/sidebar-nav";
import { SeverityBadge } from "@/components/brief/severity-badge";
import { AudienceBadge } from "@/components/brief/audience-badge";
import { ScoreBadge } from "@/components/brief/score-badge";
import { RecommendationBadge } from "@/components/brief/recommendation-badge";

export default function ResultsPage() {
  const router = useRouter();
  const [report, setReport] = useState<PrepLensReportV2 | null>(null);
  const [exporting, setExporting] = useState<string | null>(null);

  useEffect(() => {
    const stored = sessionStorage.getItem("preplens_report");
    if (!stored) {
      router.push("/new");
      return;
    }
    try {
      const parsed = JSON.parse(stored);
      // Validate V2 structure — reject stale V1 data
      if (!parsed.schema_version || !parsed.input_summary?.company_name) {
        sessionStorage.removeItem("preplens_report");
        router.push("/new");
        return;
      }
      setReport(parsed);
    } catch {
      sessionStorage.removeItem("preplens_report");
      router.push("/new");
    }
  }, [router]);

  async function handleExport(format: "pdf" | "docx") {
    if (!report) return;
    setExporting(format);
    try {
      const blob = await exportDossier(report, format);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      const company = report.input_summary.company_name.replace(/\s+/g, "_");
      const role = report.input_summary.job_title.replace(/\s+/g, "_");
      const date = new Date().toISOString().slice(0, 10).replace(/-/g, "");
      a.href = url;
      a.download = `PrepLens_${company}_${role}_${date}.${format}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      alert(err instanceof Error ? err.message : "Export failed");
    } finally {
      setExporting(null);
    }
  }

  if (!report) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    );
  }

  const r = report;

  return (
    <main className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-10 border-b border-border bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3">
          <div className="flex items-center gap-4">
            <Link href="/new" className="text-muted-foreground hover:text-foreground">
              <ArrowLeft className="h-5 w-5" />
            </Link>
            <Link href="/" className="hidden sm:block">
              <img src="/logo.png" alt="PrepLens" className="h-6" />
            </Link>
            <div className="border-l border-border pl-4 hidden sm:block" />
            <div>
              <h1 className="text-lg font-bold">
                {r.input_summary.company_name} &mdash; {r.input_summary.job_title}
              </h1>
              <p className="text-xs text-muted-foreground">
                Generated {new Date(r.generated_at).toLocaleDateString()}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => handleExport("docx")}
              disabled={exporting !== null}
              className="flex items-center gap-1.5 rounded-md border border-border bg-white px-3 py-1.5 text-sm font-medium hover:bg-secondary transition-colors disabled:opacity-50"
            >
              <Download className="h-3.5 w-3.5" />
              {exporting === "docx" ? "Exporting..." : "DOCX"}
            </button>
            <button
              onClick={() => handleExport("pdf")}
              disabled={exporting !== null}
              className="flex items-center gap-1.5 rounded-md bg-primary px-3 py-1.5 text-sm font-medium text-primary-foreground hover:bg-accent transition-colors disabled:opacity-50"
            >
              <Download className="h-3.5 w-3.5" />
              {exporting === "pdf" ? "Exporting..." : "PDF"}
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-8">
        <div className="grid gap-8 lg:grid-cols-[200px_1fr]">
          {/* Sidebar */}
          <aside className="hidden lg:block">
            <SidebarNav />
          </aside>

          {/* Main content */}
          <div className="space-y-6">
            {/* 1. Executive Summary */}
            <SectionCard
              id="executive-summary"
              title="Executive Summary"
              icon={<FileText className="h-5 w-5 text-primary" />}
            >
              <p className="mb-3 text-base font-semibold text-foreground">
                {r.executive_summary.headline}
              </p>
              <p className="mb-4 text-sm leading-relaxed text-foreground">
                {r.executive_summary.summary}
              </p>
              {r.executive_summary.top_takeaways.length > 0 && (
                <div>
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    Key Takeaways
                  </p>
                  <ul className="space-y-1.5">
                    {r.executive_summary.top_takeaways.map((t: string, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-sm">
                        <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                        {t}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </SectionCard>

            {/* 2. Pursuit Recommendation */}
            <SectionCard
              id="pursuit-recommendation"
              title="Pursuit Recommendation"
              icon={<TrendingUp className="h-5 w-5 text-primary" />}
            >
              <div className="mb-4 flex flex-wrap items-center gap-3">
                <RecommendationBadge recommendation={r.pursuit_recommendation.recommendation} />
                <ScoreBadge score={r.pursuit_recommendation.overall_fit_score} label="fit" size="lg" />
                <ScoreBadge score={r.pursuit_recommendation.confidence_score} label="confidence" size="lg" />
              </div>
              <div className="mb-4 grid gap-4 sm:grid-cols-2">
                <div className="rounded-lg border border-border p-3">
                  <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Ideal Candidate</p>
                  <p className="text-sm">{r.pursuit_recommendation.ideal_candidate_profile}</p>
                </div>
                <div className="rounded-lg border border-border p-3">
                  <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Your Outlook</p>
                  <p className="text-sm">{r.pursuit_recommendation.candidate_outlook}</p>
                </div>
              </div>
              <ul className="space-y-1.5">
                {r.pursuit_recommendation.reasoning.map((reason: string, i: number) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                    {reason}
                  </li>
                ))}
              </ul>
            </SectionCard>

            {/* 3. Company Snapshot */}
            <SectionCard
              id="company-snapshot"
              title="Company Snapshot"
              icon={<Building2 className="h-5 w-5 text-primary" />}
            >
              <p className="mb-3 text-sm leading-relaxed">{r.company_snapshot.company_overview}</p>
              <div className="mb-3 flex flex-wrap gap-2 text-xs">
                {r.company_snapshot.company_stage !== "unknown" && (
                  <span className="rounded-full border border-border px-2.5 py-0.5 font-medium capitalize">
                    {r.company_snapshot.company_stage}
                  </span>
                )}
                {r.company_snapshot.risk_level !== "unknown" && (
                  <SeverityBadge severity={r.company_snapshot.risk_level} />
                )}
              </div>
              {r.company_snapshot.business_model && (
                <p className="mb-1 text-sm"><span className="font-medium">Business Model:</span> {r.company_snapshot.business_model}</p>
              )}
              {r.company_snapshot.product_focus && (
                <p className="mb-3 text-sm"><span className="font-medium">Product Focus:</span> {r.company_snapshot.product_focus}</p>
              )}
              {r.company_snapshot.engineering_signals.length > 0 && (
                <div className="mb-3">
                  <p className="mb-1.5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Engineering Signals</p>
                  <ul className="space-y-1">
                    {r.company_snapshot.engineering_signals.map((s: string, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-sm">
                        <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                        {s}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {r.company_snapshot.notable_unknowns.length > 0 && (
                <div>
                  <p className="mb-1.5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Notable Unknowns</p>
                  <ul className="space-y-1">
                    {r.company_snapshot.notable_unknowns.map((u: string, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                        <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-amber-400" />
                        {u}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </SectionCard>

            {/* 4. Role Snapshot */}
            <SectionCard
              id="role-snapshot"
              title="Role Snapshot"
              icon={<Briefcase className="h-5 w-5 text-primary" />}
            >
              <p className="mb-3 text-sm leading-relaxed">{r.role_snapshot.role_summary}</p>
              <div className="mb-3 flex flex-wrap gap-2">
                {r.role_snapshot.seniority_signal !== "unknown" && (
                  <span className="rounded-full border border-border px-2.5 py-0.5 text-xs font-medium capitalize">
                    {r.role_snapshot.seniority_signal}
                  </span>
                )}
                {r.role_snapshot.core_domain.map((d: string, i: number) => (
                  <span key={i} className="rounded-full bg-primary/10 px-2.5 py-0.5 text-xs font-medium text-primary">
                    {d}
                  </span>
                ))}
              </div>
              {r.role_snapshot.primary_stack_signals.length > 0 && (
                <div className="mb-3">
                  <p className="mb-1.5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Stack Signals</p>
                  <div className="flex flex-wrap gap-1.5">
                    {r.role_snapshot.primary_stack_signals.map((s: string, i: number) => (
                      <span key={i} className="rounded-md bg-muted px-2 py-0.5 text-xs">{s}</span>
                    ))}
                  </div>
                </div>
              )}
              {r.role_snapshot.success_profile && (
                <div className="rounded-lg border border-border bg-muted/50 p-3">
                  <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Success Profile</p>
                  <p className="text-sm">{r.role_snapshot.success_profile}</p>
                </div>
              )}
            </SectionCard>

            {/* 5. Hiring Priorities */}
            <SectionCard
              id="hiring-priorities"
              title="Hiring Priorities"
              icon={<Target className="h-5 w-5 text-primary" />}
            >
              <ul className="space-y-2">
                {r.hiring_priorities.map((p, i: number) => (
                  <li key={i} className="rounded-lg border border-border bg-muted/50 p-3">
                    <div className="mb-1 flex items-center gap-2">
                      <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">
                        {p.importance_score}
                      </span>
                      <span className="text-sm font-medium">{p.priority}</span>
                    </div>
                    <p className="pl-7 text-sm text-muted-foreground">{p.why_it_matters}</p>
                  </li>
                ))}
              </ul>
            </SectionCard>

            {/* 6. Fit Analysis */}
            <SectionCard
              id="fit-analysis"
              title="Fit Analysis"
              icon={<Sparkles className="h-5 w-5 text-primary" />}
            >
              {r.fit_analysis.strong_fit_signals.length > 0 && (
                <div className="mb-4">
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-emerald-600">Strong Fit</p>
                  <div className="space-y-2">
                    {r.fit_analysis.strong_fit_signals.map((s, i: number) => (
                      <div key={i} className="rounded-lg border border-emerald-200 bg-emerald-50/50 p-3">
                        <div className="mb-1 flex items-center gap-2">
                          <ScoreBadge score={s.strength_score} />
                          <span className="text-sm font-medium">{s.signal}</span>
                        </div>
                        <p className="text-sm text-muted-foreground">{s.evidence}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {r.fit_analysis.partial_fit_signals.length > 0 && (
                <div className="mb-4">
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-amber-600">Partial Fit</p>
                  <div className="space-y-2">
                    {r.fit_analysis.partial_fit_signals.map((s, i: number) => (
                      <div key={i} className="rounded-lg border border-amber-200 bg-amber-50/50 p-3">
                        <div className="mb-1 flex items-center gap-2">
                          <ScoreBadge score={s.strength_score} />
                          <span className="text-sm font-medium">{s.signal}</span>
                        </div>
                        <p className="text-sm text-muted-foreground">{s.evidence}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {r.fit_analysis.missing_or_weak_signals.length > 0 && (
                <div>
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-red-600">Gaps</p>
                  <div className="space-y-2">
                    {r.fit_analysis.missing_or_weak_signals.map((s, i: number) => (
                      <div key={i} className="rounded-lg border border-red-200 bg-red-50/50 p-3">
                        <div className="mb-1 flex items-center gap-2">
                          <SeverityBadge severity={s.gap_severity} />
                          <span className="text-sm font-medium">{s.signal}</span>
                        </div>
                        <p className="text-sm text-muted-foreground">{s.why_it_matters}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </SectionCard>

            {/* 7. Concerns & Mitigation */}
            <SectionCard
              id="concerns"
              title="Concerns & Mitigation"
              icon={<AlertTriangle className="h-5 w-5 text-amber-500" />}
            >
              <div className="space-y-3">
                {r.concerns_and_mitigation.map((c, i: number) => (
                  <div key={i} className="rounded-lg border border-border p-4">
                    <div className="mb-2 flex items-center gap-2">
                      <SeverityBadge severity={c.severity} />
                      <span className="text-sm font-medium">{c.concern}</span>
                    </div>
                    <p className="mb-1 text-sm text-muted-foreground">
                      <span className="font-medium text-foreground">Why they care: </span>
                      {c.why_they_may_care}
                    </p>
                    <p className="mb-1 text-sm text-muted-foreground">
                      <span className="font-medium text-foreground">Mitigation: </span>
                      {c.mitigation_strategy}
                    </p>
                    <p className="mb-1 text-sm text-muted-foreground">
                      <span className="font-medium text-foreground">Best proof: </span>
                      {c.best_proof_to_use}
                    </p>
                    {c.sample_response && (
                      <div className="mt-2 rounded-md bg-muted/50 p-2">
                        <p className="text-xs font-semibold text-muted-foreground mb-1">Sample Response</p>
                        <p className="text-sm italic">&ldquo;{c.sample_response}&rdquo;</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </SectionCard>

            {/* 8. Resume Tailoring */}
            <SectionCard
              id="resume-tailoring"
              title="Resume Tailoring"
              icon={<FileEdit className="h-5 w-5 text-primary" />}
            >
              <div className="mb-4 flex items-center gap-2">
                <span className={`rounded-full border px-3 py-1 text-sm font-semibold ${
                  r.resume_tailoring.resume_verdict === "good_to_apply"
                    ? "border-emerald-200 bg-emerald-100 text-emerald-700"
                    : r.resume_tailoring.resume_verdict === "tailor_before_applying"
                      ? "border-amber-200 bg-amber-100 text-amber-700"
                      : "border-red-200 bg-red-100 text-red-700"
                }`}>
                  {r.resume_tailoring.resume_verdict.replace(/_/g, " ").replace(/\b\w/g, (c: string) => c.toUpperCase())}
                </span>
              </div>
              {r.resume_tailoring.positioning_angle && (
                <p className="mb-4 text-sm"><span className="font-medium">Positioning angle:</span> {r.resume_tailoring.positioning_angle}</p>
              )}
              {r.resume_tailoring.priority_edits.length > 0 && (
                <div className="mb-4">
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Priority Edits</p>
                  <div className="space-y-2">
                    {r.resume_tailoring.priority_edits.map((e, i: number) => (
                      <div key={i} className="rounded-lg border border-border p-3">
                        <div className="mb-1 flex items-center gap-2">
                          <span className="rounded bg-primary/10 px-1.5 py-0.5 text-xs font-medium text-primary">{e.type.replace(/_/g, " ")}</span>
                          <span className="text-sm font-medium">{e.target}</span>
                        </div>
                        <p className="text-sm text-muted-foreground">{e.recommendation}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {r.resume_tailoring.missing_keywords.length > 0 && (
                <div className="mb-4">
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Missing Keywords</p>
                  <div className="flex flex-wrap gap-1.5">
                    {r.resume_tailoring.missing_keywords.map((k: string, i: number) => (
                      <span key={i} className="rounded-md bg-amber-100 px-2 py-0.5 text-xs text-amber-700">{k}</span>
                    ))}
                  </div>
                </div>
              )}
              {r.resume_tailoring.bullets_to_emphasize.length > 0 && (
                <div>
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Bullets to Emphasize</p>
                  <ul className="space-y-1.5">
                    {r.resume_tailoring.bullets_to_emphasize.map((b, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-sm">
                        <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                        <span><span className="font-medium">{b.experience_area}:</span> {b.why}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </SectionCard>

            {/* 9. Application Strategy */}
            <SectionCard
              id="application-strategy"
              title="Application Strategy"
              icon={<Send className="h-5 w-5 text-primary" />}
            >
              <div className="mb-4 flex flex-wrap gap-3">
                <span className={`rounded-full border px-2.5 py-0.5 text-xs font-medium ${
                  r.application_strategy.apply_now
                    ? "border-emerald-200 bg-emerald-100 text-emerald-700"
                    : "border-amber-200 bg-amber-100 text-amber-700"
                }`}>
                  {r.application_strategy.apply_now ? "Apply Now" : "Wait / Prepare First"}
                </span>
                {r.application_strategy.referral_recommended && (
                  <span className="rounded-full border border-blue-200 bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-700">
                    Referral Recommended
                  </span>
                )}
                {r.application_strategy.best_outreach_target !== "none" && (
                  <span className="rounded-full border border-border px-2.5 py-0.5 text-xs font-medium capitalize">
                    Target: {r.application_strategy.best_outreach_target.replace(/_/g, " ")}
                  </span>
                )}
              </div>
              {r.application_strategy.outreach_angle && (
                <p className="mb-2 text-sm"><span className="font-medium">Outreach angle:</span> {r.application_strategy.outreach_angle}</p>
              )}
              {r.application_strategy.suggested_connection_note && (
                <div className="mb-2 rounded-md bg-muted/50 p-3">
                  <p className="mb-1 text-xs font-semibold text-muted-foreground">Connection Note</p>
                  <p className="text-sm italic">&ldquo;{r.application_strategy.suggested_connection_note}&rdquo;</p>
                </div>
              )}
              {r.application_strategy.suggested_email_angle && (
                <div className="rounded-md bg-muted/50 p-3">
                  <p className="mb-1 text-xs font-semibold text-muted-foreground">Email Angle</p>
                  <p className="text-sm italic">&ldquo;{r.application_strategy.suggested_email_angle}&rdquo;</p>
                </div>
              )}
            </SectionCard>

            {/* 10. Recruiter Screen Prep */}
            <SectionCard
              id="recruiter-prep"
              title="Recruiter Screen Prep"
              icon={<Phone className="h-5 w-5 text-primary" />}
            >
              {r.recruiter_screen_prep.what_they_will_likely_screen_for.length > 0 && (
                <div className="mb-4">
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Screening Criteria</p>
                  <ul className="space-y-1">
                    {r.recruiter_screen_prep.what_they_will_likely_screen_for.map((s: string, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-sm">
                        <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                        {s}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {r.recruiter_screen_prep.likely_recruiter_questions.length > 0 && (
                <div className="mb-4 space-y-3">
                  <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Likely Questions</p>
                  {r.recruiter_screen_prep.likely_recruiter_questions.map((q, i: number) => (
                    <div key={i} className="rounded-lg border border-border p-3">
                      <p className="mb-1 text-sm font-medium">{q.question}</p>
                      <p className="mb-2 text-sm text-muted-foreground">{q.intent}</p>
                      {q.suggested_answer_points.length > 0 && (
                        <ul className="space-y-0.5">
                          {q.suggested_answer_points.map((p: string, j: number) => (
                            <li key={j} className="flex items-start gap-2 text-sm text-muted-foreground">
                              <span className="mt-1 h-1 w-1 shrink-0 rounded-full bg-muted-foreground" />
                              {p}
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  ))}
                </div>
              )}
              <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                {r.recruiter_screen_prep.compensation_notes && (
                  <p><span className="font-medium text-foreground">Comp:</span> {r.recruiter_screen_prep.compensation_notes}</p>
                )}
                {r.recruiter_screen_prep.work_auth_notes && (
                  <p><span className="font-medium text-foreground">Work Auth:</span> {r.recruiter_screen_prep.work_auth_notes}</p>
                )}
              </div>
            </SectionCard>

            {/* 11. Story Bank */}
            <SectionCard
              id="story-bank"
              title="Story Bank"
              icon={<BookOpen className="h-5 w-5 text-primary" />}
            >
              <div className="space-y-3">
                {r.story_bank.map((s, i: number) => (
                  <div key={i} className="rounded-lg border border-border p-4">
                    <p className="mb-2 text-sm font-semibold">{s.story_title}</p>
                    <p className="mb-1 text-sm"><span className="font-medium">Experience:</span> {s.recommended_experience}</p>
                    <p className="mb-2 text-sm"><span className="font-medium">Angle:</span> {s.angle_to_emphasize}</p>
                    {s.key_metrics_or_outcomes.length > 0 && (
                      <div className="mb-2 flex flex-wrap gap-1.5">
                        {s.key_metrics_or_outcomes.map((m: string, j: number) => (
                          <span key={j} className="rounded-md bg-emerald-50 px-2 py-0.5 text-xs text-emerald-700">{m}</span>
                        ))}
                      </div>
                    )}
                    {s.best_for_questions.length > 0 && (
                      <p className="text-xs text-muted-foreground">
                        <span className="font-medium">Best for:</span> {s.best_for_questions.join(", ")}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </SectionCard>

            {/* 12. Interview Rounds */}
            <SectionCard
              id="interview-rounds"
              title="Interview Round Strategy"
              icon={<Layers className="h-5 w-5 text-primary" />}
            >
              <div className="space-y-3">
                {r.interview_rounds.map((round, i: number) => (
                  <div key={i} className="rounded-lg border border-border p-4">
                    <div className="mb-2 flex items-center gap-2">
                      <AudienceBadge audience={round.round_name} />
                    </div>
                    <p className="mb-2 text-sm">{round.round_goal}</p>
                    {round.what_they_will_likely_probe.length > 0 && (
                      <div className="mb-2">
                        <p className="mb-1 text-xs font-medium text-muted-foreground">They will probe:</p>
                        <ul className="space-y-0.5">
                          {round.what_they_will_likely_probe.map((p: string, j: number) => (
                            <li key={j} className="flex items-start gap-2 text-sm text-muted-foreground">
                              <span className="mt-1 h-1 w-1 shrink-0 rounded-full bg-muted-foreground" />
                              {p}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {round.candidate_focus.length > 0 && (
                      <div>
                        <p className="mb-1 text-xs font-medium text-muted-foreground">Your focus:</p>
                        <ul className="space-y-0.5">
                          {round.candidate_focus.map((f: string, j: number) => (
                            <li key={j} className="flex items-start gap-2 text-sm">
                              <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                              {f}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </SectionCard>

            {/* 13. Likely Interview Questions */}
            <SectionCard
              id="interview-questions"
              title="Likely Interview Questions"
              icon={<MessageSquare className="h-5 w-5 text-primary" />}
            >
              <div className="space-y-3">
                {r.likely_interview_questions.map((q, i: number) => (
                  <div key={i} className="rounded-lg border border-border p-4">
                    <div className="mb-2 flex items-center gap-2">
                      <span className="rounded-full bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary capitalize">
                        {q.category.replace(/_/g, " ")}
                      </span>
                    </div>
                    <p className="mb-1 text-sm font-medium">{q.question}</p>
                    <p className="text-sm text-muted-foreground">{q.why_they_may_ask}</p>
                    {q.best_story_or_topic && (
                      <p className="mt-1 text-sm"><span className="font-medium">Best story/topic:</span> {q.best_story_or_topic}</p>
                    )}
                  </div>
                ))}
              </div>
            </SectionCard>

            {/* 14. Reverse Interview Questions */}
            <SectionCard
              id="reverse-questions"
              title="Reverse-Interview Questions"
              icon={<ArrowLeftRight className="h-5 w-5 text-primary" />}
            >
              <div className="space-y-3">
                {r.reverse_interview_questions.map((q, i: number) => (
                  <div key={i} className="rounded-lg border border-border p-4">
                    <div className="mb-2">
                      <AudienceBadge audience={q.target_interviewer} />
                    </div>
                    <p className="mb-1 text-sm font-medium">{q.question}</p>
                    <p className="mb-2 text-sm text-muted-foreground">{q.why_ask_this}</p>
                    <div className="grid gap-2 sm:grid-cols-2">
                      {q.good_answer_signals.length > 0 && (
                        <div className="rounded-md bg-emerald-50/50 p-2">
                          <p className="mb-1 text-xs font-medium text-emerald-700">Good Signals</p>
                          <ul className="space-y-0.5">
                            {q.good_answer_signals.map((s: string, j: number) => (
                              <li key={j} className="text-xs text-emerald-600">{s}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {q.bad_answer_signals.length > 0 && (
                        <div className="rounded-md bg-red-50/50 p-2">
                          <p className="mb-1 text-xs font-medium text-red-700">Warning Signals</p>
                          <ul className="space-y-0.5">
                            {q.bad_answer_signals.map((s: string, j: number) => (
                              <li key={j} className="text-xs text-red-600">{s}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </SectionCard>

            {/* 15. Logistics & Constraints */}
            <SectionCard
              id="logistics"
              title="Logistics & Constraints"
              icon={<MapPin className="h-5 w-5 text-primary" />}
            >
              <div className="grid gap-3 sm:grid-cols-2">
                <div className="rounded-lg border border-border p-3">
                  <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Work Model</p>
                  <p className="text-sm capitalize">{r.logistics_and_constraints.work_model}</p>
                </div>
                <div className="rounded-lg border border-border p-3">
                  <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Level Clarity</p>
                  <p className="text-sm capitalize">{r.logistics_and_constraints.level_clarity}</p>
                </div>
                {r.logistics_and_constraints.location_notes && (
                  <div className="rounded-lg border border-border p-3">
                    <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Location</p>
                    <p className="text-sm">{r.logistics_and_constraints.location_notes}</p>
                  </div>
                )}
                {r.logistics_and_constraints.compensation_signal && (
                  <div className="rounded-lg border border-border p-3">
                    <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Compensation</p>
                    <p className="text-sm">{r.logistics_and_constraints.compensation_signal}</p>
                  </div>
                )}
                {r.logistics_and_constraints.timeline_signal && (
                  <div className="rounded-lg border border-border p-3">
                    <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Timeline</p>
                    <p className="text-sm">{r.logistics_and_constraints.timeline_signal}</p>
                  </div>
                )}
                {r.logistics_and_constraints.visa_or_work_auth_signal && (
                  <div className="rounded-lg border border-border p-3">
                    <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Work Auth</p>
                    <p className="text-sm">{r.logistics_and_constraints.visa_or_work_auth_signal}</p>
                  </div>
                )}
              </div>
            </SectionCard>

            {/* 16. Red Flags & Unknowns */}
            <SectionCard
              id="red-flags"
              title="Red Flags & Unknowns"
              icon={<Flag className="h-5 w-5 text-amber-500" />}
              variant="warning"
            >
              {r.red_flags_and_unknowns.red_flags.length > 0 && (
                <div className="mb-4">
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-red-600">Red Flags</p>
                  <div className="space-y-2">
                    {r.red_flags_and_unknowns.red_flags.map((f, i: number) => (
                      <div key={i} className="flex items-start gap-2 rounded-lg border border-red-200 bg-white p-3">
                        <SeverityBadge severity={f.severity} />
                        <div>
                          <p className="text-sm font-medium">{f.flag}</p>
                          <p className="text-sm text-muted-foreground">{f.why_it_matters}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {r.red_flags_and_unknowns.unknowns_to_verify.length > 0 && (
                <div>
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-amber-600">Unknowns to Verify</p>
                  <ul className="space-y-1.5">
                    {r.red_flags_and_unknowns.unknowns_to_verify.map((u: string, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-sm">
                        <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-amber-500" />
                        {u}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </SectionCard>

            {/* 17. Immediate Next Actions */}
            <SectionCard
              id="next-actions"
              title="Immediate Next Actions"
              icon={<Zap className="h-5 w-5 text-primary" />}
            >
              <div className="space-y-2">
                {r.immediate_next_actions
                  .sort((a, b) => a.priority - b.priority)
                  .map((action, i: number) => (
                    <div key={i} className="flex items-start gap-3 rounded-lg border border-border bg-muted/50 p-3">
                      <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
                        {action.priority}
                      </span>
                      <div className="flex-1">
                        <p className="text-sm font-medium">{action.action}</p>
                        <p className="text-sm text-muted-foreground">{action.why}</p>
                      </div>
                      {action.time_estimate_minutes > 0 && (
                        <span className="shrink-0 rounded-md bg-muted px-2 py-0.5 text-xs text-muted-foreground">
                          ~{action.time_estimate_minutes}m
                        </span>
                      )}
                    </div>
                  ))}
              </div>
            </SectionCard>

            {/* 18. Prep Checklist */}
            <SectionCard
              id="checklist"
              title="Preparation Checklist"
              icon={<CheckSquare className="h-5 w-5 text-primary" />}
            >
              <ul className="space-y-2">
                {r.prep_checklist.map((item, i: number) => (
                  <li
                    key={i}
                    className="flex items-start gap-3 rounded-lg border border-border bg-muted/50 p-3 text-sm"
                  >
                    <input
                      type="checkbox"
                      defaultChecked={item.completed}
                      className="mt-0.5 h-4 w-4 rounded border-border text-primary accent-primary"
                    />
                    {item.item}
                  </li>
                ))}
              </ul>
            </SectionCard>
          </div>
        </div>
      </div>
    </main>
  );
}
