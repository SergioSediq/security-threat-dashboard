const base = import.meta.env.VITE_API_BASE ?? "";

export async function getJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${base}${path}`, {
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}
