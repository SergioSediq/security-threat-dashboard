export type SituationSummary = {
  total_events: number;
  critical: number;
  mitre_techniques_observed: number;
  osint_items: number;
};

export type ThreatRow = {
  id: string;
  title: string;
  severity: string;
  cve_ids: string[];
  mitre_techniques: string[];
  summary: string;
  source: string;
  observed_at: string;
};

export type OSINTItem = {
  id: string;
  title: string;
  url: string;
  tags: string[];
  fetched_at: string;
};
