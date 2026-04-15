import { useMemo, useState } from "react";
import { OsintPanel } from "./components/OsintPanel";
import { StreamToolbar } from "./components/StreamToolbar";
import { SummaryStrip } from "./components/SummaryStrip";
import { ThreatTable } from "./components/ThreatTable";
import { useOsint } from "./hooks/useOsint";
import { useSituation } from "./hooks/useSituation";

export function App() {
  const [tab, setTab] = useState<"stream" | "osint">("stream");
  const [severity, setSeverity] = useState<string | null>(null);
  const situation = useSituation(severity);
  const osint = useOsint();

  const header = useMemo(
    () => (
      <header className="header">
        <h1>Situation</h1>
        <p className="sub">CVE context · MITRE ATT&amp;CK · OSINT rows (fixture feed)</p>
        <nav className="tabs" aria-label="Views">
          <button
            type="button"
            className={tab === "stream" ? "tab active" : "tab"}
            onClick={() => setTab("stream")}
          >
            Stream
          </button>
          <button
            type="button"
            className={tab === "osint" ? "tab active" : "tab"}
            onClick={() => setTab("osint")}
          >
            OSINT
          </button>
        </nav>
      </header>
    ),
    [tab]
  );

  if (situation.status === "loading" || osint.status === "loading") {
    return (
      <div className="page">
        <p className="muted">Loading…</p>
      </div>
    );
  }

  if (situation.status === "error") {
    return (
      <div className="page">
        <h1>Situation</h1>
        <p className="error">
          Backend not reachable ({situation.message}). For local dev run uvicorn on
          :8000; Vite proxies <code>/api</code>.
        </p>
      </div>
    );
  }

  if (osint.status === "error") {
    return (
      <div className="page">
        <h1>Situation</h1>
        <p className="error">OSINT feed failed ({osint.message}).</p>
      </div>
    );
  }

  return (
    <div className="page">
      {header}

      <SummaryStrip data={situation.summary} />

      {tab === "stream" ? (
        <section>
          <StreamToolbar
            severity={severity}
            onSeverity={setSeverity}
            total={situation.threatTotal}
          />
          <h2>Stream</h2>
          <ThreatTable rows={situation.threats} />
        </section>
      ) : (
        <OsintPanel items={osint.items} />
      )}
    </div>
  );
}
