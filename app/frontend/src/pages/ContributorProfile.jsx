import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../lib/api";

export default function ContributorProfile() {
  const { handle } = useParams();
  const [d, setD] = useState(null);
  useEffect(() => { api.get(`/contributors/${handle}`).then((r) => setD(r.data)).catch(() => setD({ error: true })); }, [handle]);
  if (!d) return <div className="px-6 py-20 meta-ink">loading…</div>;
  if (d.error) return <div className="px-6 py-20 meta-ink">contributor not found.</div>;
  const c = d.contributor;
  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="grid lg:grid-cols-12 gap-8">
        <aside className="lg:col-span-4">
          <div className="brutal-card-static p-7">
            <div className="w-24 h-24 border-2 border-[var(--ink)] bg-[var(--acid)] flex items-center justify-center font-display font-black text-5xl">{c.name[0]?.toUpperCase()}</div>
            <div className="meta-ink mt-4">curator · joined {c.joined || "—"}</div>
            <h1 className="font-display font-black text-3xl tracking-tighter mt-1">@{c.handle}</h1>
            <p className="font-editorial italic text-xl mt-3">{c.bio}</p>
            <div className="flex flex-wrap gap-2 mt-4">
              {(c.scenes || []).map((s) => <span key={s} className="tag-chip">{s}</span>)}
            </div>
            <div className="mt-6 grid grid-cols-3 gap-2">
              <div className="border-2 border-[var(--ink)] p-3 text-center"><div className="meta-ink">depth</div><div className="font-display font-black text-2xl">{c.depth_score || 0}</div></div>
              <div className="border-2 border-[var(--ink)] p-3 text-center bg-[var(--hyperpop)] text-white"><div className="meta-ink !text-white/80">lore</div><div className="font-display font-black text-2xl">{c.lore_count || 0}</div></div>
              <div className="border-2 border-[var(--ink)] p-3 text-center"><div className="meta-ink">theory</div><div className="font-display font-black text-2xl">{c.theory_count || 0}</div></div>
            </div>
            {c.patron_album && <div className="mt-4"><div className="meta-ink mb-1">patron album</div><Link to={`/album/${c.patron_album}`} className="brutal-btn invert !w-full justify-center">{c.patron_album}</Link></div>}
          </div>
        </aside>
        <div className="lg:col-span-8">
          <div className="meta-ink mb-2">musical autobiography</div>
          <h2 className="font-display font-black text-4xl tracking-tighter">contributions.</h2>
          <div className="mt-6 space-y-4">
            {(d.lore || []).map((l) => (
              <Link key={l.id} to={`/lore/${l.id}`} className="brutal-card-static p-5 block">
                <div className="meta-ink">lore · {l.depth}</div>
                <div className="font-display font-bold text-xl mt-1">{l.title}</div>
                <p className="font-editorial italic mt-2">{l.excerpt}</p>
              </Link>
            ))}
            {(d.theories || []).map((t) => (
              <Link key={t.id} to={`/theory/${t.id}`} className="brutal-card-static p-5 block bg-[var(--parchment-deep)]">
                <div className="meta-ink">theory · {t.stance}</div>
                <div className="font-display font-bold text-xl mt-1">{t.title}</div>
                <p className="font-editorial italic mt-2">{t.abstract}</p>
              </Link>
            ))}
            {(d.lore || []).length === 0 && (d.theories || []).length === 0 && <p className="meta-ink">no contributions yet.</p>}
          </div>
        </div>
      </div>
    </div>
  );
}
