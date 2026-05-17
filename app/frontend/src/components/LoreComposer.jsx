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
  const [form, setForm] = useState({
    title: "",
    body: "",
    excerpt: "",
    album_id: "",
    track_id: "",
    depth: "community",
  });

  useEffect(() => {
    api.get("/albums?limit=50").then((r) => setAlbums(r.data)).catch(() => {});
    api.get("/tracks?limit=80").then((r) => setTracks(r.data)).catch(() => {});
  }, []);

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
      };
      const r = await createLore(payload);
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

