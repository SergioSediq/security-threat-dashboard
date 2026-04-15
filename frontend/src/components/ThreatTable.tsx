import type { ThreatRow } from "../api/types";

function sevClass(s: string): string {
  const x = s.toLowerCase();
  if (x === "critical") return "sev-critical";
  if (x === "high") return "sev-high";
  if (x === "medium") return "sev-medium";
  return "sev-low";
}

export function ThreatTable({ rows }: { rows: ThreatRow[] }) {
  return (
    <table className="table">
      <thead>
        <tr>
          <th>Severity</th>
          <th>Title</th>
          <th>CVE</th>
          <th>Techniques</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((t) => (
          <tr key={t.id}>
            <td>
              <span className={`sev ${sevClass(t.severity)}`}>{t.severity}</span>
            </td>
            <td>{t.title}</td>
            <td>{t.cve_ids.length ? t.cve_ids.join(", ") : "—"}</td>
            <td>
              {t.mitre_techniques.map((m) => (
                <span key={m} className="chip">
                  {m}
                </span>
              ))}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
