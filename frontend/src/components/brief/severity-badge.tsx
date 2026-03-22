import { cn } from "@/lib/utils";

interface SeverityBadgeProps {
  severity: string;
}

export function SeverityBadge({ severity }: SeverityBadgeProps) {
  return (
    <span
      className={cn(
        "inline-block rounded-full px-2.5 py-0.5 text-xs font-medium",
        severity === "high" && "bg-red-100 text-red-700",
        severity === "medium" && "bg-amber-100 text-amber-700",
        severity === "low" && "bg-green-100 text-green-700"
      )}
    >
      {severity}
    </span>
  );
}
