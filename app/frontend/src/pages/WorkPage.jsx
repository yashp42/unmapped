import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../lib/api";

export default function WorkPage() {
  const { id } = useParams(); const [data, setData] = useState(null);
  useEffect(() => { api.get(`/explore/works/${id}`).then((r) => setData(r.data)).catch(() => setData({ missing: true })); }, [id]);
  if (!data) return <div className="max-w-4xl mx-auto px-6 py-20 meta-ink">opening work file…</div>;
  if (data.missing) return <div className="max-w-4xl mx-auto px-6 py-20 font-editorial italic text-2xl">This work needs to be searched again before it can be opened.</div>;
  const { work, lore_count, theory_count, connection_count } = data;
  return <main className="max-w-4xl mx-auto px-6 py-12"><Link to="/explore" className="meta-ink underline underline-offset-4">back to explore</Link><div className="grid md:grid-cols-[280px_1fr] gap-8 mt-6"><div className="aspect-square brutal-card-static overflow-hidden bg-[var(--parchment-deep)]">{work.artwork_url && <img src={work.artwork_url} alt={`${work.title} cover`} className="w-full h-full object-cover" />}</div><div><div className="meta-ink">{work.kind} · {work.artist_name || "music archive"}</div><h1 className="font-display font-black text-5xl md:text-7xl tracking-tighter mt-2">{work.title}</h1>{work.album_title && <p className="font-editorial italic text-2xl mt-3">from {work.album_title}</p>}<div className="flex flex-wrap gap-2 mt-7"><span className="tag-chip">{lore_count} lore</span><span className="tag-chip">{theory_count} theories</span><span className="tag-chip">{connection_count} connections</span></div>{work.external_url && <a href={work.external_url} target="_blank" rel="noreferrer" className="brutal-btn invert mt-7">open release</a>}</div></div><section className="mt-12 brutal-card-static p-6"><div className="meta-ink">unmapped around this work</div><p className="font-editorial italic text-2xl mt-2">{lore_count || theory_count || connection_count ? "This work already has a trail through the archive." : "No one has mapped this work yet. Be the first to add a reading, theory, or relationship."}</p><div className="flex gap-3 mt-5"><Link to="/lore" className="brutal-btn">read lore</Link><Link to="/theories" className="brutal-btn invert">read theories</Link></div></section></main>;
}
