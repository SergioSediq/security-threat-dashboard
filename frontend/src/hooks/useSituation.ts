import { useEffect, useState } from "react";
import { getJSON } from "../api/client";
import type { SituationSummary, ThreatRow } from "../api/types";

type State =
  | { status: "loading" }
  | {
      status: "ok";
      summary: SituationSummary;
      threats: ThreatRow[];
      threatTotal: number;
    }
  | { status: "error"; message: string };

export function useSituation(severity: string | null): State {
  const [state, setState] = useState<State>({ status: "loading" });

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading" });
    (async () => {
      try {
        const q = new URLSearchParams({ limit: "100", offset: "0" });
        if (severity) q.set("severity", severity);
        const [summary, threatPack] = await Promise.all([
          getJSON<SituationSummary>("/api/v1/situation/summary"),
          getJSON<{ items: ThreatRow[]; total: number }>(
            `/api/v1/threats?${q.toString()}`
          ),
        ]);
        if (!cancelled) {
          setState({
            status: "ok",
            summary,
            threats: threatPack.items,
            threatTotal: threatPack.total,
          });
        }
      } catch (e) {
        if (!cancelled) {
          setState({
            status: "error",
            message: e instanceof Error ? e.message : "request failed",
          });
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [severity]);

  return state;
}
