import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../lib/api";

export default function TheoryPage() {
  const { id } = useParams();
  const [t, setT] = useState(null);
  useEffect(() => { api.get(`/theories/${id}`).then((r) => setT(r.data)); }, [id]);
  if (!t) return <div className="px-6 py-20 meta-ink">loading…</div>;
  return (
    <article className="max-w-3xl mx-auto px-6 py-16">
      <div className="meta-ink mb-3">theory · {t.stance} · by {t.author}</div>
      <h1 className="font-display font-black text-4xl md:text-6xl tracking-tighter leading-[0.95]">{t.title}</h1>
      <div className="flex flex-wrap gap-3 mt-5">
        {t.album_id && <Link to={`/album/${t.album_id}`} className="tag-chip">album · {t.album_id}</Link>}
        <span className="tag-chip" style={{background: 'var(--acid)'}}>{t.supporters} co-sign</span>
        <span className="tag-chip" style={{background: '#FFD479'}}>{t.challengers} push back</span>
      </div>
      <div className="mt-10 editorial-prose dropcap">
        <p>{t.abstract}</p>
        <p>open question to the community: bring receipts. cite the lyric, the interview, the timestamp. claim without evidence is just vibes — and we have a section for those.</p>
      </div>
      <div className="mt-12 flex gap-3">
        <button className="brutal-btn acid" data-testid="theory-cosign">co-sign</button>
        <button className="brutal-btn invert" data-testid="theory-pushback">push back</button>
        <button className="brutal-btn" data-testid="theory-reply">reply with evidence</button>
      </div>
    </article>
  );
}
