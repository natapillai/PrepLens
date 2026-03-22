import { cn } from "@/lib/utils";

interface ScoreBadgeProps {
  score: number;
  max?: number;
  label?: string;
  size?: "sm" | "lg";
}

export function ScoreBadge({ score, max = 10, label, size = "sm" }: ScoreBadgeProps) {
  const pct = score / max;
  const color =
    pct >= 0.7
      ? "bg-emerald-100 text-emerald-700 border-emerald-200"
      : pct >= 0.4
        ? "bg-amber-100 text-amber-700 border-amber-200"
        : "bg-red-100 text-red-700 border-red-200";

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full border font-semibold",
        color,
        size === "lg" ? "px-3 py-1 text-sm" : "px-2 py-0.5 text-xs"
      )}
    >
      {score}/{max}
      {label && <span className="font-normal">{label}</span>}
    </span>
  );
}
