import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { api } from "../lib/api";
import { ArrowRight, Quote } from "lucide-react";
import { useAuth } from "../lib/auth";
import { toast } from "sonner";
import LoadingSpinner from "../components/LoadingSpinner";
import SaveButton from "../components/SaveButton";

export default function TrackPage() {
  const { id } = useParams();
  const { user, refreshUser } = useAuth();
  const navigate = useNavigate();
  const [depth, setDepth] = useState("casual");
  const [data, setData] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState("");
  useEffect(() => { api.get(`/tracks/${id}`).then((r) => setData(r.data)); }, [id]);
  useEffect(() => {
    if (data?.track?.title) setTitle(data.track.title);
  }, [data]);
  if (!data) return <div className="max-w-3xl mx-auto px-6 py-20 meta-ink">loading…</div>;
  const { track, artist, album, lore, samples, connected_tracks } = data;

  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="grid lg:grid-cols-12 gap-8">
        <div className="lg:col-span-8">
          <div className="meta-ink mb-2">track · {String(album?.tracks?.indexOf(track.id)+1 || 1).padStart(2,'0')} / {album?.tracks?.length || 1}</div>
          <h1 className="font-display font-black text-5xl md:text-7xl tracking-tighter">{track.title}</h1>
          {user && (
            <div className="mt-3 flex flex-wrap gap-2">
              <SaveButton
                type="track"
                id={track.id}
                saved={user.saved_track_ids?.includes(track.id)}
                onToggle={() => refreshUser()}
              />
              <button className="brutal-btn" onClick={()=>setEditing((s)=>!s)} disabled={actionLoading}>{editing ? 'Cancel' : 'Edit'}</button>
              <button className="brutal-btn" onClick={async ()=>{ if(!confirm('Delete this track?')) return; setActionLoading(true); try { await api.delete(`/tracks/${track.id}`); toast.success('deleted'); navigate(`/album/${album.id}`); } catch(e){ toast.error('delete failed'); } finally { setActionLoading(false); } }} disabled={actionLoading}>
                {actionLoading ? <><LoadingSpinner size={16} /> <span className="ml-2">Deleting</span></> : 'Delete'}
              </button>
            </div>
          )}
          {editing && (
            <div className="mt-3 flex gap-2">
              <input className="input" value={title} onChange={(e)=>setTitle(e.target.value)} />
              <button className="brutal-btn" onClick={async ()=>{ setActionLoading(true); try { await api.put(`/tracks/${track.id}`, { title }); const r = await api.get(`/tracks/${track.id}`); setData(r.data); setEditing(false); toast.success('saved'); } catch(e){ toast.error('save failed'); } finally { setActionLoading(false); } }} disabled={actionLoading}>
                {actionLoading ? <><LoadingSpinner size={16} /> <span className="ml-2">Saving</span></> : 'Save'}
              </button>
            </div>
          )}
          <div className="mt-3 flex flex-wrap items-center gap-3">
            <Link to={`/album/${album.id}`} className="font-editorial italic text-2xl underline underline-offset-4">{album.title}</Link>
            <span className="meta-ink">/</span>
            <span className="font-display font-bold text-xl">{artist.name}</span>
            <span className="meta-ink">· {track.duration}</span>
          </div>
          {track.key_line && (
            <div className="mt-8 brutal-card-static p-6 bg-[var(--acid)]">
              <Quote className="mb-2" />
              <p className="font-editorial italic text-3xl leading-tight">"{track.key_line}"</p>
            </div>
          )}

          {/* DEPTH SELECTOR */}
          <div className="mt-10 flex items-center gap-2 border-b-2 border-[var(--ink)] pb-3">
            <span className="meta-ink mr-2">read depth →</span>
            {["casual", "community", "deep"].map((d) => (
              <button key={d} onClick={() => setDepth(d)} data-testid={`depth-${d}`}
                className={`px-3 py-1 font-mono text-xs uppercase tracking-widest border-2 border-[var(--ink)] ${depth===d?'bg-[var(--ink)] text-[var(--parchment)]':''}`}>{d}</button>
            ))}
          </div>

          {depth === "casual" && (
            <div className="mt-6 font-editorial text-xl leading-relaxed">
              <p>a song that's haunted a generation. {track.lore_count} pieces of lore have been written about it. you can listen and like — but if you stay, you'll learn things that change how you hear it.</p>
            </div>
          )}
          {depth === "community" && (
            <div className="mt-6 space-y-4">
              <p className="font-editorial italic text-xl">notes the community keeps coming back to:</p>
              {lore.filter((l) => l.depth === "community").map((l) => (
                <Link key={l.id} to={`/lore/${l.id}`} className="brutal-card p-5 block" data-testid={`lore-community-${l.id}`}>
                  <div className="meta-ink">by {l.author}</div>
                  <div className="font-display font-bold text-lg mt-1">{l.title}</div>
                  <p className="font-editorial italic mt-2">{l.excerpt}</p>
                </Link>
              ))}
              {lore.filter((l) => l.depth === "community").length === 0 && <p className="meta-ink">no community notes yet. be the first.</p>}
            </div>
          )}
          {depth === "deep" && (
            <div className="mt-6 space-y-4">
              <p className="font-editorial italic text-xl">deep readings · for the second and third listens:</p>
              {lore.filter((l) => l.depth === "deep").map((l) => (
                <Link key={l.id} to={`/lore/${l.id}`} className="brutal-card p-5 block bg-[var(--parchment-deep)]" data-testid={`lore-deep-${l.id}`}>
                  <div className="meta-ink">by {l.author} · DEEP</div>
                  <div className="font-display font-bold text-xl mt-1">{l.title}</div>
                  <p className="font-editorial italic text-lg mt-2">{l.excerpt}</p>
                </Link>
              ))}
              {lore.filter((l) => l.depth === "deep").length === 0 && <p className="meta-ink">no deep entries yet.</p>}
            </div>
          )}
        </div>

        <aside className="lg:col-span-4 space-y-5">
          {samples.length > 0 && (
            <div className="brutal-card-static p-5">
              <div className="meta-ink mb-2">sample genealogy</div>
              {samples.map((s) => (
                <div key={s.id} className="border-l-2 border-[var(--ink)] pl-3 mb-2">
                  <div className="font-display font-bold">{s.source_artist}</div>
                  <div className="font-editorial italic">{s.source_track} · {s.year}</div>
                  <div className="meta-ink mt-1">{s.notes}</div>
                </div>
              ))}
            </div>
          )}
          <div className="brutal-card-static p-5">
            <div className="meta-ink mb-3 flex items-center gap-2">rabbit hole → <span className="font-display font-bold normal-case">connected tracks</span></div>
            <div className="space-y-2">
              {connected_tracks.map((c) => (
                <Link key={c.id} to={`/track/${c.id}`} className="flex items-center justify-between px-3 py-2 border-2 border-[var(--ink)] hover:bg-[var(--acid)]" data-testid={`connected-${c.id}`}>
                  <div>
                    <div className="font-display font-bold">{c.title}</div>
                    <div className="meta-ink">{c.album_id}</div>
                  </div>
                  <ArrowRight size={14}/>
                </Link>
              ))}
              {connected_tracks.length === 0 && <p className="meta-ink">no public connections yet.</p>}
            </div>
            <Link to={`/connections?track=${track.id}`} className="brutal-btn !w-full mt-4 justify-center" data-testid="open-map-track">open in connection map</Link>
          </div>
        </aside>
      </div>
    </div>
  );
}
