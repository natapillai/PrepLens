"use client";

const SECTIONS = [
  { id: "role-summary", label: "Role Summary" },
  { id: "hiring-priorities", label: "Hiring Priorities" },
  { id: "strengths", label: "Your Strengths" },
  { id: "concerns", label: "Concerns & Gaps" },
  { id: "interview-questions", label: "Interview Questions" },
  { id: "reverse-questions", label: "Reverse Questions" },
  { id: "positioning", label: "Positioning Strategy" },
  { id: "red-flags", label: "Red Flags" },
  { id: "checklist", label: "Prep Checklist" },
];

export function SidebarNav() {
  return (
    <nav className="sticky top-24 space-y-1">
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
