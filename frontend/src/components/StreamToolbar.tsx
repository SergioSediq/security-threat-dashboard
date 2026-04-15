type Props = {
  severity: string | null;
  onSeverity: (v: string | null) => void;
  total: number;
};

const levels = ["", "CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"] as const;

export function StreamToolbar({ severity, onSeverity, total }: Props) {
  return (
    <div className="toolbar">
      <label htmlFor="sev">Severity</label>
      <select
        id="sev"
        value={severity ?? ""}
        onChange={(e) => onSeverity(e.target.value ? e.target.value : null)}
      >
        {levels.map((lvl) => (
          <option key={lvl || "all"} value={lvl}>
            {lvl || "All"}
          </option>
        ))}
      </select>
      <span className="muted">
        Showing {total} row{total === 1 ? "" : "s"} (fixture feed)
      </span>
      <a className="export" href="/api/v1/export/threats.jsonl">
        Export JSONL
      </a>
    </div>
  );
}
