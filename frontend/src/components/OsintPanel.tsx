import type { OSINTItem } from "../api/types";

type Props = { items: OSINTItem[] };

export function OsintPanel({ items }: Props) {
  return (
    <section>
      <h2>OSINT references</h2>
      <ul className="osint">
        {items.map((o) => (
          <li key={o.id}>
            <a href={o.url} target="_blank" rel="noreferrer">
              {o.title}
            </a>
            <div className="tags">
              {o.tags.map((t) => (
                <span key={t} className="pill">
                  {t}
                </span>
              ))}
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
