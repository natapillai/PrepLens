import { cn } from "@/lib/utils";

interface AudienceBadgeProps {
  audience: string;
}

const STYLE_MAP: Record<string, string> = {
  recruiter: "bg-blue-100 text-blue-700",
  hiring_manager: "bg-purple-100 text-purple-700",
  engineer: "bg-emerald-100 text-emerald-700",
  panel: "bg-indigo-100 text-indigo-700",
  final_round: "bg-rose-100 text-rose-700",
};

export function AudienceBadge({ audience }: AudienceBadgeProps) {
  const key = audience.toLowerCase().replace(/\s+/g, "_");
  const style = STYLE_MAP[key] || "bg-gray-100 text-gray-700";
  const label = audience.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <span
      className={cn(
        "inline-block rounded-full px-2.5 py-0.5 text-xs font-medium capitalize",
        style
      )}
    >
      {label}
    </span>
  );
}
