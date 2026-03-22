import { cn } from "@/lib/utils";

interface RecommendationBadgeProps {
  recommendation: string;
}

const STYLES: Record<string, string> = {
  pursue: "bg-emerald-100 text-emerald-700 border-emerald-200",
  pursue_selectively: "bg-blue-100 text-blue-700 border-blue-200",
  low_priority: "bg-amber-100 text-amber-700 border-amber-200",
  insufficient_information: "bg-gray-100 text-gray-600 border-gray-200",
};

const LABELS: Record<string, string> = {
  pursue: "Pursue",
  pursue_selectively: "Pursue Selectively",
  low_priority: "Low Priority",
  insufficient_information: "Insufficient Information",
};

export function RecommendationBadge({ recommendation }: RecommendationBadgeProps) {
  return (
    <span
      className={cn(
        "inline-block rounded-full border px-3 py-1 text-sm font-semibold",
        STYLES[recommendation] || STYLES.insufficient_information
      )}
    >
      {LABELS[recommendation] || recommendation}
    </span>
  );
}
