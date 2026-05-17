import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../lib/api";

export default function VibePage() {
  const { id } = useParams();
  const [d, setD] = useState(null);
  useEffect(() => { api.get(`/vibes/${id}`).then((r) => setD(r.data)); }, [id]);
  if (!d) return <div className="px-6 py-20 meta-ink">loading…</div>;
  const { vibe, tracks } = d;
  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="brutal-card-static p-10 grain relative" style={{ background: vibe.color }}>
        <div className="meta-ink mix-blend-multiply">felt state · vibe cluster</div>
        <h1 className="font-display font-black text-6xl md:text-8xl tracking-tighter mt-2 mix-blend-multiply lowercase">{vibe.name}</h1>
        <p className="font-editorial italic text-2xl md:text-3xl mt-4 max-w-3xl mix-blend-multiply">{vibe.description}</p>
        <p className="font-editorial italic text-xl mt-3 mix-blend-multiply">"{vibe.felt_state}"</p>
      </div>
      <h2 className="font-display font-black text-3xl tracking-tighter mt-10 mb-4">tracks that live here</h2>
      <div className="divide-y-2 divide-[var(--ink)] border-2 border-[var(--ink)] brutal-shadow bg-white">
        {tracks.map((t) => (
          <Link key={t.id} to={`/track/${t.id}`} className="flex items-center gap-4 px-5 py-3 hover:bg-[var(--parchment-deep)]" data-testid={`vibe-track-${t.id}`}>
            <span className="font-display font-bold text-lg flex-1">{t.title}</span>
            <span className="meta-ink">{t.album_id}</span>
            <span className="meta-ink">{t.duration}</span>
          </Link>
        ))}
        {tracks.length === 0 && <div className="px-5 py-6 meta-ink">no tracks yet.</div>}
      </div>
    </div>
  );
}
