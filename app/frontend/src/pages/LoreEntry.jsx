import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../lib/api";

export default function LoreEntry() {
  const { id } = useParams();
  const [l, setL] = useState(null);
  useEffect(() => { api.get(`/lore/${id}`).then((r) => setL(r.data)); }, [id]);
  if (!l) return <div className="px-6 py-20 meta-ink">loading…</div>;

  return (
    <article className="max-w-3xl mx-auto px-6 py-16">
      <div className="meta-ink mb-3">lore entry · {l.depth} read · by {l.author}</div>
      <h1 className="font-display font-black text-4xl md:text-6xl tracking-tighter leading-[0.95]" data-testid="lore-title">{l.title}</h1>
      <div className="flex flex-wrap gap-3 mt-5">
        {l.track_id && <Link to={`/track/${l.track_id}`} className="tag-chip">track · {l.track_id}</Link>}
        {l.album_id && <Link to={`/album/${l.album_id}`} className="tag-chip">album · {l.album_id}</Link>}
        <span className="tag-chip">{l.votes}↑</span>
      </div>
      <div className="mt-10 editorial-prose dropcap" data-testid="lore-body">
        {(l.body || l.excerpt).split("\n\n").map((p, i) => <p key={i}>{p}</p>)}
      </div>
      <div className="mt-12 border-t-2 border-[var(--ink)] pt-6">
        <div className="meta-ink mb-2">comment count</div>
        <p className="font-editorial italic">{l.comments} replies — discussion is held in the contributor circle. log in to join.</p>
      </div>
    </article>
  );
}
