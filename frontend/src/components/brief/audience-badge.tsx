import { cn } from "@/lib/utils";

interface AudienceBadgeProps {
  audience: string;
}

export function AudienceBadge({ audience }: AudienceBadgeProps) {
  return (
    <span
      className={cn(
        "inline-block rounded-full px-2.5 py-0.5 text-xs font-medium",
        audience === "Recruiter" && "bg-blue-100 text-blue-700",
        audience === "Hiring Manager" && "bg-purple-100 text-purple-700",
        audience === "Engineer" && "bg-emerald-100 text-emerald-700"
      )}
    >
      {audience}
    </span>
  );
}
