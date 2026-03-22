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
} from "lucide-react";
import type { DossierReport } from "@/lib/types";
import { exportDossier } from "@/lib/api";
import { SectionCard } from "@/components/brief/section-card";
import { SidebarNav } from "@/components/brief/sidebar-nav";
import { SeverityBadge } from "@/components/brief/severity-badge";
import { AudienceBadge } from "@/components/brief/audience-badge";

export default function ResultsPage() {
  const router = useRouter();
  const [report, setReport] = useState<DossierReport | null>(null);
  const [exporting, setExporting] = useState<string | null>(null);

  useEffect(() => {
    const stored = sessionStorage.getItem("preplens_report");
    if (!stored) {
      router.push("/new");
      return;
    }
    try {
      setReport(JSON.parse(stored));
    } catch {
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
      const company = report.report_meta.company_name.replace(/\s+/g, "_");
      const role = report.report_meta.job_title.replace(/\s+/g, "_");
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

  return (
    <main className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-10 border-b border-border bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3">
          <div className="flex items-center gap-4">
            <Link href="/new" className="text-muted-foreground hover:text-foreground">
              <ArrowLeft className="h-5 w-5" />
            </Link>
            <div>
              <h1 className="text-lg font-bold">
                {report.report_meta.company_name} &mdash;{" "}
                {report.report_meta.job_title}
              </h1>
              <p className="text-xs text-muted-foreground">
                Generated{" "}
                {new Date(report.report_meta.generated_at).toLocaleDateString()}
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
            {/* Role Summary */}
            <SectionCard
              id="role-summary"
              title="Role Summary"
              icon={<FileText className="h-5 w-5 text-primary" />}
            >
              <p className="text-sm leading-relaxed text-foreground">
                {report.role_summary}
              </p>
            </SectionCard>

            {/* Hiring Priorities */}
            <SectionCard
              id="hiring-priorities"
              title="Likely Hiring Priorities"
              icon={<Target className="h-5 w-5 text-primary" />}
            >
              <ul className="space-y-2">
                {report.hiring_priorities.map((p, i) => (
                  <li
                    key={i}
                    className="flex items-start gap-2 rounded-lg border border-border bg-muted/50 p-3 text-sm"
                  >
                    <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">
                      {i + 1}
                    </span>
                    {p}
                  </li>
                ))}
              </ul>
            </SectionCard>

            {/* Candidate Strengths */}
            <SectionCard
              id="strengths"
              title="Your Strongest Alignment"
              icon={<Sparkles className="h-5 w-5 text-primary" />}
            >
              <ul className="space-y-2">
                {report.candidate_strengths.map((s, i) => (
                  <li
                    key={i}
                    className="flex items-start gap-2 text-sm"
                  >
                    <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-500" />
                    {s}
                  </li>
                ))}
              </ul>
            </SectionCard>

            {/* Concerns */}
            <SectionCard
              id="concerns"
              title="Likely Concerns & Gaps"
              icon={<AlertTriangle className="h-5 w-5 text-amber-500" />}
            >
              <div className="space-y-3">
                {report.candidate_concerns.map((c, i) => (
                  <div
                    key={i}
                    className="rounded-lg border border-border p-4"
                  >
                    <div className="mb-2 flex items-center gap-2">
                      <SeverityBadge severity={c.severity} />
                      <span className="text-sm font-medium">{c.concern}</span>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      <span className="font-medium text-foreground">Mitigation: </span>
                      {c.mitigation}
                    </p>
                  </div>
                ))}
              </div>
            </SectionCard>

            {/* Interview Questions */}
            <SectionCard
              id="interview-questions"
              title="Likely Interview Questions"
              icon={<MessageSquare className="h-5 w-5 text-primary" />}
            >
              <div className="space-y-3">
                {report.likely_interview_questions.map((q, i) => (
                  <div
                    key={i}
                    className="rounded-lg border border-border p-4"
                  >
                    <p className="mb-1 text-sm font-medium">{q.question}</p>
                    <p className="text-sm text-muted-foreground">
                      {q.why_they_might_ask}
                    </p>
                  </div>
                ))}
              </div>
            </SectionCard>

            {/* Reverse Questions */}
            <SectionCard
              id="reverse-questions"
              title="Reverse-Interview Questions"
              icon={<ArrowLeftRight className="h-5 w-5 text-primary" />}
            >
              <div className="space-y-3">
                {report.reverse_interview_questions.map((q, i) => (
                  <div
                    key={i}
                    className="rounded-lg border border-border p-4"
                  >
                    <div className="mb-2 flex items-center gap-2">
                      <AudienceBadge audience={q.audience} />
                    </div>
                    <p className="mb-1 text-sm font-medium">{q.question}</p>
                    <p className="text-sm text-muted-foreground">
                      {q.why_it_matters}
                    </p>
                  </div>
                ))}
              </div>
            </SectionCard>

            {/* Positioning */}
            <SectionCard
              id="positioning"
              title="Positioning Strategy"
              icon={<Compass className="h-5 w-5 text-primary" />}
            >
              <ul className="space-y-2">
                {report.positioning_strategy.map((s, i) => (
                  <li
                    key={i}
                    className="flex items-start gap-2 text-sm"
                  >
                    <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                    {s}
                  </li>
                ))}
              </ul>
            </SectionCard>

            {/* Red Flags */}
            <SectionCard
              id="red-flags"
              title="Red Flags & Unknowns"
              icon={<Flag className="h-5 w-5 text-amber-500" />}
              variant="warning"
            >
              <ul className="space-y-2">
                {report.red_flags_or_unknowns.map((r, i) => (
                  <li
                    key={i}
                    className="flex items-start gap-2 text-sm"
                  >
                    <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-amber-500" />
                    {r}
                  </li>
                ))}
              </ul>
            </SectionCard>

            {/* Prep Checklist */}
            <SectionCard
              id="checklist"
              title="Preparation Checklist"
              icon={<CheckSquare className="h-5 w-5 text-primary" />}
            >
              <ul className="space-y-2">
                {report.prep_checklist.map((item, i) => (
                  <li
                    key={i}
                    className="flex items-start gap-3 rounded-lg border border-border bg-muted/50 p-3 text-sm"
                  >
                    <input
                      type="checkbox"
                      className="mt-0.5 h-4 w-4 rounded border-border text-primary accent-primary"
                    />
                    {item}
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
