"use client";

const SECTIONS = [
  { id: "executive-summary", label: "Executive Summary" },
  { id: "pursuit-recommendation", label: "Pursuit Recommendation" },
  { id: "company-snapshot", label: "Company Snapshot" },
  { id: "role-snapshot", label: "Role Snapshot" },
  { id: "hiring-priorities", label: "Hiring Priorities" },
  { id: "fit-analysis", label: "Fit Analysis" },
  { id: "concerns", label: "Concerns & Mitigation" },
  { id: "resume-tailoring", label: "Resume Tailoring" },
  { id: "application-strategy", label: "Application Strategy" },
  { id: "recruiter-prep", label: "Recruiter Screen Prep" },
  { id: "story-bank", label: "Story Bank" },
  { id: "interview-rounds", label: "Interview Rounds" },
  { id: "interview-questions", label: "Interview Questions" },
  { id: "reverse-questions", label: "Reverse Questions" },
  { id: "logistics", label: "Logistics" },
  { id: "red-flags", label: "Red Flags & Unknowns" },
  { id: "next-actions", label: "Next Actions" },
  { id: "checklist", label: "Prep Checklist" },
];

export function SidebarNav() {
  return (
    <nav className="sticky top-24 space-y-0.5">
      <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Sections
      </p>
      {SECTIONS.map((s) => (
        <a
          key={s.id}
          href={`#${s.id}`}
          className="block rounded-md px-3 py-1.5 text-sm text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
        >
          {s.label}
        </a>
      ))}
    </nav>
  );
}
