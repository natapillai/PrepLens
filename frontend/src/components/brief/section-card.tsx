"use client";

import { cn } from "@/lib/utils";

interface SectionCardProps {
  id: string;
  title: string;
  icon?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
  variant?: "default" | "warning";
}

export function SectionCard({
  id,
  title,
  icon,
  children,
  className,
  variant = "default",
}: SectionCardProps) {
  return (
    <section
      id={id}
      className={cn(
        "rounded-xl border bg-card p-6 shadow-sm scroll-mt-24",
        variant === "warning" ? "border-amber-200 bg-amber-50/50" : "border-border",
        className
      )}
    >
      <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold text-foreground">
        {icon}
        {title}
      </h2>
      {children}
    </section>
  );
}
