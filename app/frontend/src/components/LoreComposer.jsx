import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { api } from "../lib/api";
import { createLore } from "../api/lore";
import { formatApiError } from "../lib/api";
import LoadingSpinner from "./LoadingSpinner";

const DEPTHS = [
  { id: "casual", label: "casual read" },
  { id: "community", label: "community" },
  { id: "deep", label: "deep read" },
];

export default function LoreComposer({ onCreated }) {
  const nav = useNavigate();
  const [albums, setAlbums] = useState([]);
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [targetSearch, setTargetSearch] = useState("");
  const [targetResults, setTargetResults] = useState([]);
  const [form, setForm] = useState(() => { try { return JSON.parse(localStorage.getItem("unmapped_lore_draft")) || { title: "", body: "", excerpt: "", album_id: "", track_id: "", depth: "community" }; } catch { return { title: "", body: "", excerpt: "", album_id: "", track_id: "", depth: "community" }; } });

  useEffect(() => {
    api.get("/albums?limit=50").then((r) => setAlbums(r.data)).catch(() => {});
    api.get("/tracks?limit=80").then((r) => setTracks(r.data)).catch(() => {});
  }, []);
  useEffect(() => {
    if (targetSearch.trim().length < 2) { setTargetResults([]); return; }
    const timer = setTimeout(() => api.get("/explore/search", { params: { q: targetSearch } }).then((r) => setTargetResults([...(r.data.tracks || []), ...(r.data.albums || [])].slice(0, 8))).catch(() => {}), 300);
    return () => clearTimeout(timer);
  }, [targetSearch]);
  useEffect(() => { if (form.title || form.body) localStorage.setItem("unmapped_lore_draft", JSON.stringify(form)); }, [form]);

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        title: form.title,
        body: form.body,
        depth: form.depth,
        excerpt: form.excerpt || undefined,
        album_id: form.album_id || undefined,
        track_id: form.track_id || undefined,
        target_source: form.target_source || undefined,
        target_label: form.target_label || undefined,
      };
      const r = await createLore(payload);
      localStorage.removeItem("unmapped_lore_draft");
      toast.success("lore published");
      onCreated?.(r.data);
      nav(`/lore/${r.data.id}`);
    } catch (err) {
      toast.error(formatApiError(err.response?.data?.detail));
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={submit} className="brutal-card-static p-6 space-y-4" data-testid="lore-composer">
      <div>
        <label className="meta-ink block mb-1">title</label>
        <input className="brutal-input" value={form.title} onChange={set("title")} required minLength={3} placeholder="the thesis in one line" />
      </div>
      <div>
        <label className="meta-ink block mb-1">body</label>
        <textarea
          className="brutal-input min-h-[200px]"
          value={form.body}
          onChange={set("body")}
          required
          minLength={20}
          placeholder="write the lore. paragraphs separated by blank lines."
        />
      </div>
      <div>
        <label className="meta-ink block mb-1">excerpt (optional)</label>
        <input className="brutal-input" value={form.excerpt} onChange={set("excerpt")} placeholder="hook for the index — auto-generated if empty" />
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <label className="meta-ink block mb-1">link album</label>
          <select className="brutal-input" value={form.album_id} onChange={set("album_id")}>
            <option value="">— none —</option>
            {albums.map((a) => (
              <option key={a.id} value={a.id}>{a.title}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="meta-ink block mb-1">link track</label>
          <select className="brutal-input" value={form.track_id} onChange={set("track_id")}>
            <option value="">— none —</option>
            {tracks.map((t) => (
              <option key={t.id} value={t.id}>{t.title}</option>
            ))}
          </select>
        </div>
      </div>
      <div>
        <label className="meta-ink block mb-1">or find any release</label>
        <input className="brutal-input" value={targetSearch} onChange={(e) => setTargetSearch(e.target.value)} placeholder="search the live music catalogue" />
        {targetResults.length > 0 && <div className="border-2 border-t-0 border-[var(--ink)] bg-white">{targetResults.map((item) => { const isTrack = Boolean(item.album_title); return <button key={item.id} type="button" className="w-full text-left px-3 py-2 border-b border-[var(--ink)] last:border-0 hover:bg-[var(--parchment-deep)]" onClick={() => { setForm((f) => ({ ...f, album_id: isTrack ? "" : item.id, track_id: isTrack ? item.id : "", target_source: "itunes", target_label: `${item.title} — ${item.artist_name}` })); setTargetSearch(`${item.title} — ${item.artist_name}`); setTargetResults([]); }}><span className="font-display font-bold">{item.title}</span> <span className="meta-ink">{item.artist_name} · {isTrack ? "track" : "album"}</span></button>; })}</div>}
        {form.target_label && <p className="meta-ink mt-2">attached: {form.target_label}</p>}
      </div>
      <div>
        <label className="meta-ink block mb-2">depth</label>
        <div className="flex flex-wrap gap-2">
          {DEPTHS.map((d) => (
            <button
              key={d.id}
              type="button"
              className={`tag-chip ${form.depth === d.id ? "bg-[var(--hyperpop)] text-white" : ""}`}
              onClick={() => setForm((f) => ({ ...f, depth: d.id }))}
            >
              {d.label}
            </button>
          ))}
        </div>
      </div>
      <button type="submit" className="brutal-btn accent" disabled={loading}>
        {loading ? <><LoadingSpinner size={16} /> <span className="ml-2">publishing</span></> : "publish lore"}
      </button>
    </form>
  );
}

