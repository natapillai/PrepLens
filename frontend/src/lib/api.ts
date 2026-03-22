const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function analyzeResume(formData: FormData) {
  const res = await fetch(`${API_BASE}/api/v1/analyze`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: { message: "Request failed" } }));
    throw new Error(err.error?.message || `Server error: ${res.status}`);
  }
  return res.json();
}

export async function exportDossier(
  report: unknown,
  format: "pdf" | "docx"
) {
  const res = await fetch(`${API_BASE}/api/v1/export/${format}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ report }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: { message: "Export failed" } }));
    throw new Error(err.error?.message || `Export error: ${res.status}`);
  }
  return res.blob();
}
