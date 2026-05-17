export default function Marquee({ items }) {
  const doubled = [...items, ...items];
  return (
    <div className="overflow-hidden border-y-2 border-[var(--ink)] bg-[var(--ink)] text-[var(--parchment)] py-3">
      <div className="marquee-track">
        {doubled.map((t, i) => (
          <span key={i} className="meta-ink !text-[var(--parchment)] text-sm flex items-center gap-3">
            <span className="inline-block w-2 h-2 bg-[var(--acid)]" />{t}
          </span>
        ))}
      </div>
    </div>
  );
}
