import type { SituationSummary } from "../api/types";

export function SummaryStrip({ data }: { data: SituationSummary }) {
  return (
    <section className="tiles" aria-label="Counts">
      <div className="tile">
        <span className="n">{data.total_events}</span>
        <span>Events</span>
      </div>
      <div className="tile critical">
        <span className="n">{data.critical}</span>
        <span>Critical</span>
      </div>
      <div className="tile">
        <span className="n">{data.mitre_techniques_observed}</span>
        <span>MITRE (distinct)</span>
      </div>
      <div className="tile">
        <span className="n">{data.osint_items}</span>
        <span>OSINT rows</span>
      </div>
    </section>
  );
}
