import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";

export default function TheoriesIndex() {
  const [theories, setT] = useState([]);
  const { user } = useAuth(); const [open, setOpen] = useState(false); const [form, setForm] = useState({ title: "", abstract: "", stance: "close reading", track_id: "", album_id: "", target_source: "", target_label: "" }); const [workQuery, setWorkQuery] = useState(""); const [workResults, setWorkResults] = useState([]);
  useEffect(() => { api.get("/theories").then((r) => setT(r.data)); }, []);
  useEffect(() => { if (workQuery.trim().length < 2) { setWorkResults([]); return; } const timer = setTimeout(() => api.get("/explore/search", { params: { q: workQuery } }).then((r) => setWorkResults([...(r.data.tracks || []), ...(r.data.albums || [])].slice(0, 8))).catch(() => setWorkResults([])), 300); return () => clearTimeout(timer); }, [workQuery]);
  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="meta-ink mb-3">section 05 · contested terrain</div>
      <h1 className="font-display font-black text-5xl md:text-7xl tracking-tighter">theories.</h1>
      <p className="font-editorial italic text-xl mt-3 max-w-2xl">arguments worth having, with citations. co-sign, push back, or open your own.</p>
      {user && <><button className="brutal-btn mt-6" onClick={() => setOpen((x) => !x)}>{open ? "close draft" : "open a theory"}</button>{open && <form className="brutal-card-static p-5 mt-4 grid gap-3" onSubmit={async (e) => { e.preventDefault(); const r = await api.post("/theories", form); setT((items) => [r.data, ...items]); setOpen(false); setForm({ title: "", abstract: "", stance: "close reading", track_id: "", album_id: "", target_source: "", target_label: "" }); }}><input className="brutal-input" required minLength="3" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} placeholder="the claim" /><textarea className="brutal-input min-h-28" required value={form.abstract} onChange={(e) => setForm({ ...form, abstract: e.target.value })} placeholder="make the case" /><div><input className="brutal-input" required value={workQuery} onChange={(e) => setWorkQuery(e.target.value)} placeholder="attach a song or album" />{workResults.length > 0 && <div className="border-2 border-t-0 border-[var(--ink)] bg-white">{workResults.map((item) => { const track = Boolean(item.album_title); return <button type="button" key={item.id} className="block w-full text-left px-3 py-2 border-b border-[var(--ink)] hover:bg-[var(--parchment-deep)]" onClick={() => { setForm({ ...form, track_id: track ? item.id : "", album_id: track ? "" : item.id, target_source: "itunes", target_label: `${item.title} — ${item.artist_name}` }); setWorkQuery(`${item.title} — ${item.artist_name}`); setWorkResults([]); }}>{item.title} <span className="meta-ink">{item.artist_name}</span></button>; })}</div>} {form.target_label && <div className="meta-ink mt-2">attached: {form.target_label}</div>}</div><button className="brutal-btn accent">publish theory</button></form>}</>}
      <div className="grid md:grid-cols-2 gap-5 mt-10">
        {theories.map((t) => (
          <Link key={t.id} to={`/theory/${t.id}`} className="brutal-card p-7" data-testid={`theory-index-${t.id}`}>
            <div className="meta-ink">{t.stance} · by {t.author}</div>
            <h3 className="font-display font-bold text-2xl mt-1">{t.title}</h3>
            <p className="font-editorial italic text-lg mt-2">{t.abstract}</p>
            <div className="flex gap-2 mt-4">
              <span className="tag-chip" style={{background: 'var(--acid)'}}>{t.supporters} co-sign</span>
              <span className="tag-chip" style={{background: '#FFD479'}}>{t.challengers} push back</span>
              <span className="tag-chip">{t.replies} replies</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
