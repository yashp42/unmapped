import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";
import { toast } from "sonner";
import LoadingSpinner from "../components/LoadingSpinner";

export default function Explore() {
  const [tab, setTab] = useState("albums");
  const [albums, setAlbums] = useState([]);
  const [artists, setArtists] = useState([]);
  const [vibes, setVibes] = useState([]);
  const [tracks, setTracks] = useState([]);
  const { user } = useAuth();
  const [actionLoadingId, setActionLoadingId] = useState(null);
  useEffect(() => {
    Promise.all([api.get("/albums"), api.get("/artists"), api.get("/vibes"), api.get("/tracks")])
      .then(([a, ar, v, t]) => { setAlbums(a.data); setArtists(ar.data); setVibes(v.data); setTracks(t.data); });
  }, []);

  const tabs = [{ id: "albums", label: "Album Universes" }, { id: "artists", label: "Artists" }, { id: "vibes", label: "Vibe Clusters" }, { id: "tracks", label: "Tracks" }];

  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="meta-ink mb-3">section 02 · the index</div>
      <h1 className="font-display font-black text-5xl md:text-7xl tracking-tighter">Explore.</h1>
      <p className="font-editorial italic text-xl md:text-2xl mt-3 max-w-2xl">no algorithm. no feed. choose a door.</p>

      <div className="mt-8 flex flex-wrap gap-2 border-b-2 border-[var(--ink)] pb-3">
        {tabs.map((t) => (
          <button key={t.id} onClick={() => setTab(t.id)} data-testid={`explore-tab-${t.id}`}
            className={`px-4 py-2 font-display font-bold text-sm border-2 border-[var(--ink)] ${tab===t.id?'bg-[var(--ink)] text-[var(--parchment)]':'bg-white hover:bg-[var(--parchment-deep)]'}`}>
            {t.label}
          </button>
        ))}
      </div>

      {tab === "albums" && (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5 mt-8">
          {albums.map((a) => (
            <Link key={a.id} to={`/album/${a.id}`} className="brutal-card p-0 overflow-hidden" data-testid={`album-card-${a.id}`}>
              <div className="aspect-[5/4] relative grain" style={{ background: a.color }}>
                <div className="absolute inset-4 border-2 border-[var(--ink)] p-4 flex flex-col justify-between">
                  <span className="meta-ink mix-blend-multiply">{a.year}</span>
                  <span className="font-display font-black text-3xl tracking-tighter text-[var(--ink)] mix-blend-multiply">{a.title.toLowerCase()}</span>
                </div>
              </div>
              <div className="p-5 border-t-2 border-[var(--ink)]">
                <div className="meta-ink">{a.artist_id}</div>
                <p className="font-editorial italic text-lg mt-1">{a.universe_tagline}</p>
              </div>
            </Link>
          ))}
        </div>
      )}

      {tab === "artists" && (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5 mt-8">
              {artists.map((a) => (
            <div key={a.id} className="brutal-card-static p-6" data-testid={`artist-card-${a.id}`}>
              <div className="meta-ink">{a.scene} · {a.era}</div>
              <div className="font-display font-black text-3xl tracking-tighter mt-2">{a.name}</div>
              <p className="font-editorial italic text-lg mt-2">{a.tagline}</p>
              {user && (
                <div className="mt-3 flex gap-2">
                      <button className="brutal-btn" onClick={async ()=>{ const newName = prompt('name', a.name); if(!newName) return; setActionLoadingId(a.id); try{ await api.put(`/artists/${a.id}`, { name: newName }); const r = await api.get('/artists'); setArtists(r.data); toast.success('updated'); } catch(e){ toast.error('update failed'); } finally { setActionLoadingId(null); } }} disabled={actionLoadingId!==null && actionLoadingId!==a.id}>{actionLoadingId===a.id ? <><LoadingSpinner size={16} className="inline-block"/> <span className="ml-2">Saving</span></> : 'Edit'}</button>
                      <button className="brutal-btn" onClick={async ()=>{ if(!confirm('Delete artist?')) return; setActionLoadingId(a.id); try{ await api.delete(`/artists/${a.id}`); setArtists((s)=>s.filter(x=>x.id!==a.id)); toast.success('deleted'); } catch(e){ toast.error('delete failed'); } finally { setActionLoadingId(null); } }} disabled={actionLoadingId!==null && actionLoadingId!==a.id}>{actionLoadingId===a.id ? <><LoadingSpinner size={16} className="inline-block"/> <span className="ml-2">Deleting</span></> : 'Delete'}</button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {tab === "vibes" && (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 mt-8">
          {vibes.map((v) => (
            <Link key={v.id} to={`/vibe/${v.id}`} className="brutal-card p-6 relative" style={{ background: v.color }} data-testid={`vibe-card-${v.id}`}>
              <div className="font-display font-black text-2xl lowercase tracking-tighter mix-blend-multiply">{v.name}</div>
              <p className="font-editorial italic text-lg mt-2 mix-blend-multiply">{v.description}</p>
              <div className="meta-ink mt-4 mix-blend-multiply">{v.track_count} tracks · {v.curator_count} curators</div>
            </Link>
          ))}
        </div>
      )}

      {tab === "tracks" && (
        <div className="divide-y-2 divide-[var(--ink)] border-2 border-[var(--ink)] mt-8 brutal-shadow bg-white">
          {tracks.map((t, i) => (
            <Link key={t.id} to={`/track/${t.id}`} className="flex items-center gap-4 px-5 py-3 hover:bg-[var(--parchment-deep)]" data-testid={`track-row-${t.id}`}>
              <span className="meta-ink w-10">{String(i+1).padStart(2,'0')}</span>
              <span className="font-display font-bold text-lg flex-1">{t.title}</span>
              <span className="meta-ink">{t.album_id}</span>
              <span className="meta-ink">{t.duration}</span>
              <span className="tag-chip">{t.lore_count} lore</span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
