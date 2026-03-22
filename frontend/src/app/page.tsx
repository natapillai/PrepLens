import Link from "next/link";
import { FileText, Target, Shield } from "lucide-react";

export default function HomePage() {
  return (
    <main className="min-h-screen">
      {/* Navbar */}
      <nav className="border-b border-border bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <span className="text-xl font-bold text-primary">PrepLens</span>
          <Link
            href="/new"
            className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-accent transition-colors"
          >
            Generate Brief
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="mx-auto max-w-4xl px-6 py-24 text-center">
        <h1 className="text-5xl font-bold tracking-tight text-foreground">
          See how they&apos;ll evaluate you
          <br />
          <span className="text-primary">
            — and how to evaluate them back
          </span>
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground">
          PrepLens converts your resume, a job description, and company context
          into a structured interview strategy brief. No account required.
        </p>
        <Link
          href="/new"
          className="mt-10 inline-block rounded-lg bg-primary px-8 py-3 text-base font-semibold text-primary-foreground shadow-md hover:bg-accent transition-colors"
        >
          Generate Strategy Brief
        </Link>
      </section>

      {/* Value cards */}
      <section className="mx-auto max-w-5xl px-6 pb-24">
        <div className="grid gap-8 md:grid-cols-3">
          <div className="rounded-xl border border-border bg-card p-8 shadow-sm">
            <Target className="mb-4 h-10 w-10 text-primary" />
            <h3 className="mb-2 text-lg font-semibold">
              Understand the Role
            </h3>
            <p className="text-sm text-muted-foreground">
              See likely hiring priorities, interview focus areas, and what the
              team really cares about.
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card p-8 shadow-sm">
            <FileText className="mb-4 h-10 w-10 text-primary" />
            <h3 className="mb-2 text-lg font-semibold">
              Position Yourself
            </h3>
            <p className="text-sm text-muted-foreground">
              Get candidate-specific guidance on how to frame your experience,
              what stories to lead with, and gaps to address.
            </p>
          </div>
          <div className="rounded-xl border border-border bg-card p-8 shadow-sm">
            <Shield className="mb-4 h-10 w-10 text-primary" />
            <h3 className="mb-2 text-lg font-semibold">
              Evaluate Them Back
            </h3>
            <p className="text-sm text-muted-foreground">
              Receive reverse-interview questions with good and bad signals so
              you can assess the company too.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8 text-center text-sm text-muted-foreground">
        PrepLens &copy; {new Date().getFullYear()}. Built for candidates who
        prepare with intention.
      </footer>
    </main>
  );
}
