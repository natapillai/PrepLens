import Link from "next/link";
import { BriefForm } from "@/components/forms/brief-form";

export default function NewBriefPage() {
  return (
    <main className="min-h-screen bg-background">
      {/* Navbar */}
      <nav className="border-b border-border bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link href="/">
            <img src="/logo.png" alt="PrepLens" className="h-8" />
          </Link>
        </div>
      </nav>

      <div className="mx-auto max-w-6xl px-6 py-12">
        <div className="grid gap-12 lg:grid-cols-[1fr_340px]">
          {/* Form */}
          <div>
            <h1 className="mb-2 text-3xl font-bold tracking-tight">
              Generate Strategy Brief
            </h1>
            <p className="mb-8 text-muted-foreground">
              Provide the role details and your resume. PrepLens will analyze
              the match and generate a structured interview strategy.
            </p>
            <BriefForm />
          </div>

          {/* Sidebar help text */}
          <aside className="hidden lg:block">
            <div className="sticky top-8 space-y-6">
              <div className="rounded-xl border border-border bg-card p-6">
                <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
                  What you&apos;ll get
                </h3>
                <ul className="space-y-2.5 text-sm text-foreground">
                  <li>Likely hiring priorities for the role</li>
                  <li>Your strongest alignment points</li>
                  <li>Concerns the team may have</li>
                  <li>Probable interview questions</li>
                  <li>Reverse-interview questions to ask</li>
                  <li>Positioning strategy for your narrative</li>
                  <li>Red flags to investigate</li>
                  <li>Preparation checklist</li>
                </ul>
              </div>
              <div className="rounded-xl border border-border bg-card p-6">
                <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
                  Tips
                </h3>
                <ul className="space-y-2.5 text-sm text-muted-foreground">
                  <li>
                    Paste the <strong>full</strong> job description for best
                    results.
                  </li>
                  <li>
                    Include recruiter notes about the team, process, or
                    timeline.
                  </li>
                  <li>
                    Add company context if you know specifics about their
                    culture or recent news.
                  </li>
                </ul>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </main>
  );
}
