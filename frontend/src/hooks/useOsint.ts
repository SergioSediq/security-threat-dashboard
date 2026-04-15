import { useEffect, useState } from "react";
import { getJSON } from "../api/client";
import type { OSINTItem } from "../api/types";

type State =
  | { status: "loading" }
  | { status: "ok"; items: OSINTItem[] }
  | { status: "error"; message: string };

export function useOsint(): State {
  const [state, setState] = useState<State>({ status: "loading" });

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const pack = await getJSON<{ items: OSINTItem[] }>("/api/v1/osint");
        if (!cancelled) setState({ status: "ok", items: pack.items });
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
  }, []);

  return state;
}
