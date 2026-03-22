"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";
import { ResumeUploadDropzone } from "./resume-upload-dropzone";
import { analyzeResume } from "@/lib/api";
import type { DossierReport } from "@/lib/types";

interface FormErrors {
  company_name?: string;
  job_title?: string;
  job_description?: string;
  resume_file?: string;
  general?: string;
}

const STEPS = [
  "Uploading resume...",
  "Analyzing role requirements...",
  "Generating strategy brief...",
];

export function BriefForm() {
  const router = useRouter();
  const [companyName, setCompanyName] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [recruiterNotes, setRecruiterNotes] = useState("");
  const [companyNotes, setCompanyNotes] = useState("");
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);

  function validate(): boolean {
    const errs: FormErrors = {};
    if (!companyName.trim()) errs.company_name = "Company name is required.";
    if (!jobTitle.trim()) errs.job_title = "Job title is required.";
    if (!jobDescription.trim())
      errs.job_description = "Job description is required.";
    if (!resumeFile) errs.resume_file = "Resume PDF is required.";
    setErrors(errs);
    return Object.keys(errs).length === 0;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    setCurrentStep(0);
    setErrors({});

    try {
      const formData = new FormData();
      formData.append("company_name", companyName.trim());
      formData.append("job_title", jobTitle.trim());
      formData.append("job_description", jobDescription.trim());
      formData.append("resume_file", resumeFile!);
      if (recruiterNotes.trim())
        formData.append("recruiter_notes", recruiterNotes.trim());
      if (companyNotes.trim())
        formData.append("company_notes", companyNotes.trim());

      // Simulate step progress
      const stepTimer = setInterval(() => {
        setCurrentStep((prev) => Math.min(prev + 1, STEPS.length - 1));
      }, 3000);

      const data = await analyzeResume(formData);

      clearInterval(stepTimer);

      // Store the report in sessionStorage and navigate to results
      const report = data.report as DossierReport;
      sessionStorage.setItem("preplens_report", JSON.stringify(report));
      router.push("/results");
    } catch (err) {
      setErrors({
        general:
          err instanceof Error ? err.message : "Something went wrong.",
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {errors.general && (
        <div className="rounded-lg border border-destructive/30 bg-destructive/5 p-4 text-sm text-destructive">
          {errors.general}
        </div>
      )}

      {/* Company Name */}
      <div>
        <label className="mb-1.5 block text-sm font-medium text-foreground">
          Company Name <span className="text-destructive">*</span>
        </label>
        <input
          type="text"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          placeholder="e.g. Stripe"
          disabled={isLoading}
          className="w-full rounded-md border border-border bg-white px-3 py-2 text-sm placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary disabled:opacity-50"
        />
        {errors.company_name && (
          <p className="mt-1 text-sm text-destructive">{errors.company_name}</p>
        )}
      </div>

      {/* Job Title */}
      <div>
        <label className="mb-1.5 block text-sm font-medium text-foreground">
          Job Title <span className="text-destructive">*</span>
        </label>
        <input
          type="text"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          placeholder="e.g. Senior Software Engineer"
          disabled={isLoading}
          className="w-full rounded-md border border-border bg-white px-3 py-2 text-sm placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary disabled:opacity-50"
        />
        {errors.job_title && (
          <p className="mt-1 text-sm text-destructive">{errors.job_title}</p>
        )}
      </div>

      {/* Job Description */}
      <div>
        <label className="mb-1.5 block text-sm font-medium text-foreground">
          Job Description <span className="text-destructive">*</span>
        </label>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the full job description here..."
          rows={8}
          disabled={isLoading}
          className="w-full rounded-md border border-border bg-white px-3 py-2 text-sm placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary disabled:opacity-50"
        />
        {errors.job_description && (
          <p className="mt-1 text-sm text-destructive">
            {errors.job_description}
          </p>
        )}
      </div>

      {/* Resume Upload */}
      <ResumeUploadDropzone
        onFileSelect={setResumeFile}
        selectedFile={resumeFile}
        error={errors.resume_file}
      />

      {/* Recruiter Notes */}
      <div>
        <label className="mb-1.5 block text-sm font-medium text-foreground">
          Recruiter Notes{" "}
          <span className="text-muted-foreground font-normal">(optional)</span>
        </label>
        <textarea
          value={recruiterNotes}
          onChange={(e) => setRecruiterNotes(e.target.value)}
          placeholder="Anything the recruiter mentioned about the role, team, or process..."
          rows={3}
          disabled={isLoading}
          className="w-full rounded-md border border-border bg-white px-3 py-2 text-sm placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary disabled:opacity-50"
        />
      </div>

      {/* Company Notes */}
      <div>
        <label className="mb-1.5 block text-sm font-medium text-foreground">
          Company Notes{" "}
          <span className="text-muted-foreground font-normal">(optional)</span>
        </label>
        <textarea
          value={companyNotes}
          onChange={(e) => setCompanyNotes(e.target.value)}
          placeholder="Any additional context about the company you want to factor in..."
          rows={3}
          disabled={isLoading}
          className="w-full rounded-md border border-border bg-white px-3 py-2 text-sm placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary disabled:opacity-50"
        />
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={isLoading}
        className="flex w-full items-center justify-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground shadow-md hover:bg-accent transition-colors disabled:opacity-50"
      >
        {isLoading ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" />
            {STEPS[currentStep]}
          </>
        ) : (
          "Generate Strategy Brief"
        )}
      </button>

      {/* Progress steps */}
      {isLoading && (
        <div className="space-y-2 pt-2">
          {STEPS.map((step, i) => (
            <div
              key={step}
              className={`flex items-center gap-2 text-sm ${
                i <= currentStep
                  ? "text-primary font-medium"
                  : "text-muted-foreground"
              }`}
            >
              <div
                className={`h-2 w-2 rounded-full ${
                  i < currentStep
                    ? "bg-primary"
                    : i === currentStep
                      ? "bg-primary animate-pulse"
                      : "bg-border"
                }`}
              />
              {step}
            </div>
          ))}
        </div>
      )}
    </form>
  );
}
