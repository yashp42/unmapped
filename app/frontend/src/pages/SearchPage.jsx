import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { api } from "../lib/api";

export default function SearchPage() {
  const [params] = useSearchParams();
  const q = params.get("q") || "";
  const [r, setR] = useState({ tracks: [], albums: [], artists: [], vibes: [], lore: [] });
  useEffect(() => { if (q) api.get(`/search?q=${encodeURIComponent(q)}`).then((res) => setR(res.data)); }, [q]);
  const Section = ({ title, items, render }) => items.length > 0 && (
    <section className="mt-8">
      <div className="meta-ink mb-3">{title} · {items.length}</div>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">{items.map(render)}</div>
    </section>
  );
  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="meta-ink mb-2">search</div>
      <h1 className="font-display font-black text-5xl tracking-tighter">"{q}"</h1>
      <Section title="albums" items={r.albums} render={(a) => <Link key={a.id} to={`/album/${a.id}`} className="brutal-card p-5"><div className="meta-ink">album</div><div className="font-display font-bold text-xl">{a.title}</div></Link>} />
      <Section title="tracks" items={r.tracks} render={(t) => <Link key={t.id} to={`/track/${t.id}`} className="brutal-card p-5"><div className="meta-ink">track</div><div className="font-display font-bold text-xl">{t.title}</div></Link>} />
      <Section title="artists" items={r.artists} render={(a) => <div key={a.id} className="brutal-card-static p-5"><div className="meta-ink">artist</div><div className="font-display font-bold text-xl">{a.name}</div></div>} />
      <Section title="vibes" items={r.vibes} render={(v) => <Link key={v.id} to={`/vibe/${v.id}`} className="brutal-card p-5" style={{background: v.color}}><div className="meta-ink mix-blend-multiply">vibe</div><div className="font-display font-bold text-xl mix-blend-multiply">{v.name}</div></Link>} />
      <Section title="lore" items={r.lore} render={(l) => <Link key={l.id} to={`/lore/${l.id}`} className="brutal-card p-5"><div className="meta-ink">lore</div><div className="font-display font-bold text-xl">{l.title}</div></Link>} />
      {Object.values(r).every((x) => x.length === 0) && <p className="font-editorial italic text-xl mt-8">no results. try a feeling instead — like "longing" or "summer".</p>}
    </div>
  );
}
