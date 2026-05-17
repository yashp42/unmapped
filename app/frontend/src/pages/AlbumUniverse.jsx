import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";
import { toast } from "sonner";
import LoadingSpinner from "../components/LoadingSpinner";
import SaveButton from "../components/SaveButton";

export default function AlbumUniverse() {
  const { id } = useParams();
  const { user, refreshUser } = useAuth();
  const navigate = useNavigate();
  const [d, setD] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({ title: "", universe_tagline: "" });
  useEffect(() => { api.get(`/albums/${id}`).then((r) => setD(r.data)); }, [id]);
  useEffect(() => {
    if (!d?.album) return;
    setForm({
      title: d.album.title || "",
      universe_tagline: d.album.universe_tagline || "",
    });
  }, [d]);
  if (!d) return <div className="max-w-3xl mx-auto px-6 py-20 meta-ink">opening universe…</div>;
  const { album, artist, tracks = [], lore = [], theories = [], transitions = [] } = d;
  const motifs = Array.isArray(album?.motifs) ? album.motifs : [];

  return (
    <div className="dark-universe min-h-screen">
      <div className="max-w-[1480px] mx-auto px-6 py-14">
        <div className="grid lg:grid-cols-12 gap-8 items-end">
          <div className="lg:col-span-7">
            <div className="meta mb-3" data-testid="album-universe-meta">universe · {album.year} · {artist?.name || album.artist_id}</div>
            {user && (
              <div className="mt-3 flex flex-wrap gap-2">
                <SaveButton
                  type="album"
                  id={album.id}
                  saved={user.saved_album_ids?.includes(album.id)}
                  onToggle={() => refreshUser()}
                />
                <button className="brutal-btn" onClick={() => setEditing((s) => !s)} disabled={actionLoading} data-testid="edit-album">{editing? 'Cancel':'Edit'}</button>
                <button className="brutal-btn" onClick={async () => { if (!confirm('Delete this album?')) return; setActionLoading(true); try { await api.delete(`/albums/${album.id}`); toast.success('deleted'); navigate('/'); } catch (e) { toast.error('delete failed'); } finally { setActionLoading(false); } }} disabled={actionLoading} data-testid="delete-album">
                  {actionLoading ? <><LoadingSpinner size={16} /> <span className="ml-2">Deleting</span></> : 'Delete'}
                </button>
              </div>
            )}
            {!editing ? (
              <>
                <h1 className="font-display font-black text-7xl md:text-9xl tracking-tighter leading-[0.85]">{album.title}</h1>
                <p className="font-editorial italic text-2xl md:text-3xl mt-5">{album.universe_tagline}</p>
              </>
            ) : (
              <div className="space-y-3">
                <input className="input" value={form.title} onChange={(e)=>setForm({...form, title:e.target.value})} />
                <input className="input" value={form.universe_tagline||''} onChange={(e)=>setForm({...form, universe_tagline:e.target.value})} />
                <div className="flex gap-2">
                  <button className="brutal-btn" onClick={async ()=>{ setActionLoading(true); try { await api.put(`/albums/${album.id}`, { title: form.title, universe_tagline: form.universe_tagline }); const r = await api.get(`/albums/${album.id}`); setD(r.data); setEditing(false); toast.success('saved'); } catch (e) { toast.error('save failed'); } finally { setActionLoading(false); } }} data-testid="save-album" disabled={actionLoading}>
                    {actionLoading ? <><LoadingSpinner size={16} /> <span className="ml-2">Saving</span></> : 'Save'}
                  </button>
                  <button className="brutal-btn" onClick={()=>setEditing(false)} disabled={actionLoading}>Cancel</button>
                </div>
              </div>
            )}
            <div className="flex flex-wrap gap-2 mt-6">
              {motifs.map((m) => <span key={m} className="tag-chip">{m}</span>)}
            </div>
          </div>
          <div className="lg:col-span-5">
            <div className="aspect-square w-full relative" style={{ background: album.color }}>
              <div className="absolute inset-0 grain" />
              <div className="absolute inset-6 border-2 border-[var(--ink)] flex flex-col justify-between p-6">
                <span className="meta-ink mix-blend-multiply">cover · stylized</span>
                <span className="font-display font-black text-5xl tracking-tighter text-[var(--ink)] mix-blend-multiply">{album.title.toLowerCase()}</span>
              </div>
            </div>
          </div>
        </div>

        {/* TRACKS */}
        <section className="mt-14">
          <div className="meta mb-3">tracklist · the inhabitable world</div>
          <h2 className="font-display font-black text-3xl tracking-tighter mb-6">walk through it.</h2>
          <div className="border-2 border-[var(--parchment)] divide-y-2 divide-[var(--parchment)]">
            {tracks.map((t, i) => (
              <Link key={t.id} to={`/track/${t.id}`} className="flex items-center gap-4 px-5 py-4 hover:bg-white/5" data-testid={`album-track-${t.id}`}>
                <span className="meta">{String(i+1).padStart(2,'0')}</span>
                <span className="font-display font-bold text-xl flex-1">{t.title}</span>
                <span className="meta hidden md:inline italic font-editorial !text-[var(--parchment)]/70 !text-sm normal-case tracking-normal">"{t.key_line}"</span>
                <span className="meta">{t.duration}</span>
              </Link>
            ))}
          </div>
        </section>

        {/* TRANSITIONS */}
        {transitions?.length > 0 && (
          <section className="mt-14">
            <div className="meta mb-3">transition culture</div>
            <h2 className="font-display font-black text-3xl tracking-tighter mb-4">the moments between songs.</h2>
            <div className="grid md:grid-cols-2 gap-4">
              {transitions.map((t) => (
                <div key={t.id} className="brutal-card-static p-5" data-testid={`transition-${t.id}`}>
                  <div className="meta-ink">{t.type}</div>
                  <div className="font-display font-bold text-lg mt-1">{t.from_track} → {t.to_track}</div>
                  <p className="font-editorial italic mt-2">{t.notes}</p>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* LORE + THEORIES */}
        <section className="mt-14 grid lg:grid-cols-2 gap-8">
          <div>
            <div className="meta mb-3">album lore</div>
            <h2 className="font-display font-black text-3xl tracking-tighter mb-4">what's been written.</h2>
            <div className="space-y-3">
              {lore.map((l) => (
                <Link key={l.id} to={`/lore/${l.id}`} className="brutal-card-static p-5 block" data-testid={`album-lore-${l.id}`}>
                  <div className="meta-ink">by {l.author} · {l.depth}</div>
                  <div className="font-display font-bold text-xl mt-1">{l.title}</div>
                  <p className="font-editorial italic mt-2">{l.excerpt}</p>
                </Link>
              ))}
              {lore.length === 0 && <p className="meta">no lore yet — start writing it.</p>}
            </div>
          </div>
          <div>
            <div className="meta mb-3">theories</div>
            <h2 className="font-display font-black text-3xl tracking-tighter mb-4">what's contested.</h2>
            <div className="space-y-3">
              {theories.map((t) => (
                <Link key={t.id} to={`/theory/${t.id}`} className="brutal-card-static p-5 block" data-testid={`album-theory-${t.id}`}>
                  <div className="meta-ink">{t.stance} · by {t.author}</div>
                  <div className="font-display font-bold text-xl mt-1">{t.title}</div>
                  <p className="font-editorial italic mt-2">{t.abstract}</p>
                </Link>
              ))}
              {theories.length === 0 && <p className="meta">no theories yet.</p>}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

