import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { api, formatApiError } from "../lib/api";
import { useAuth } from "../lib/auth";
import { fetchMySaves } from "../api/users";
import { toast } from "sonner";
import CollectionEditModal from "../components/CollectionEditModal";
import ProfileEditor from "../components/ProfileEditor";
import LoreComposer from "../components/LoreComposer";
import LoadingSpinner from "../components/LoadingSpinner";

const TABS = [
  { id: "collections", label: "collections" },
  { id: "saves", label: "saved" },
  { id: "write", label: "write lore" },
  { id: "profile", label: "edit profile" },
];

export default function MyWorld() {
  const { user, refreshUser } = useAuth();
  const location = useLocation();
  const [tab, setTab] = useState(location.state?.tab || "collections");
  const [collections, setCollections] = useState([]);
  const [saves, setSaves] = useState({ saved_albums: [], saved_tracks: [] });
  const [artists, setArtists] = useState([]);
  const [editing, setEditing] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [title, setTitle] = useState("");
  const [note, setNote] = useState("");

  useEffect(() => {
    if (location.state?.tab) setTab(location.state.tab);
  }, [location.state]);

  useEffect(() => {
    if (!user) return;
    api.get("/collections/mine").then((r) => setCollections(r.data));
    fetchMySaves().then((r) => setSaves(r.data));
    api.get("/artists?limit=50").then((r) => setArtists(r.data)).catch(() => {});
  }, [user]);

  const create = async (e) => {
    e.preventDefault();
    try {
      const r = await api.post("/collections", { title, note, item_ids: [] });
      setCollections([r.data, ...collections]);
      setTitle("");
      setNote("");
      toast.success("collection started");
    } catch (e) {
      toast.error(formatApiError(e.response?.data?.detail));
    }
  };

  const openEdit = (c) => {
    setEditing(c);
    setModalOpen(true);
  };

  const handleSave = async (updated) => {
    setActionLoading(true);
    try {
      await api.put(`/collections/${updated.id}`, {
        title: updated.title,
        note: updated.note,
        item_ids: updated.item_ids,
      });
      const r = await api.get("/collections/mine");
      setCollections(r.data);
      setModalOpen(false);
      toast.success("collection updated");
    } catch {
      toast.error("update failed");
    } finally {
      setActionLoading(false);
    }
  };

  const handleDelete = async (c) => {
    if (!confirm("Delete collection?")) return;
    setActionLoading(true);
    try {
      await api.delete(`/collections/${c.id}`);
      setCollections((s) => s.filter((x) => x.id !== c.id));
      toast.success("deleted");
    } catch {
      toast.error("delete failed");
    } finally {
      setActionLoading(false);
    }
  };

  if (!user) return <div className="px-6 py-20 meta-ink">loading…</div>;

  const p = user;
  const initial = (p.display_name || p.handle || "?")[0]?.toUpperCase();

  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="meta-ink mb-3">your room in the archive</div>
      <h1 className="font-display font-black text-5xl md:text-7xl tracking-tighter">My World.</h1>
      <p className="font-editorial italic text-xl mt-3 max-w-2xl">
        collections, saved albums and tracks, and the public face you show the archive.
      </p>

      <div className="flex flex-wrap gap-2 mt-8">
        {TABS.map((t) => (
          <button
            key={t.id}
            type="button"
            className={`brutal-btn ${tab === t.id ? "accent" : ""}`}
            onClick={() => setTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="grid lg:grid-cols-12 gap-8 mt-8">
        <aside className="lg:col-span-4">
          <div className="brutal-card-static p-6">
            {p.avatar_url ? (
              <img src={p.avatar_url} alt="" className="w-24 h-24 object-cover border-2 border-[var(--ink)]" />
            ) : (
              <div className="w-24 h-24 border-2 border-[var(--ink)] bg-[var(--acid)] flex items-center justify-center font-display font-black text-5xl">
                {initial}
              </div>
            )}
            <div className="meta-ink mt-4">@{p.handle}</div>
            <div className="font-display font-black text-3xl tracking-tighter">{p.display_name || p.handle}</div>
            <p className="font-editorial italic mt-2">{p.bio || "no bio yet."}</p>
            <div className="flex flex-wrap gap-2 mt-3">
              {(p.favorite_genres || []).map((g) => (
                <span key={g} className="tag-chip">{g}</span>
              ))}
            </div>
            <div className="grid grid-cols-2 gap-2 mt-4">
              <div className="border-2 border-[var(--ink)] p-3">
                <div className="meta-ink">contributions</div>
                <div className="font-display font-black text-2xl">{p.contributions_count || 0}</div>
              </div>
              <div className="border-2 border-[var(--ink)] p-3 bg-[var(--acid)]">
                <div className="meta-ink">saved</div>
                <div className="font-display font-black text-2xl">
                  {(p.saved_album_ids?.length || 0) + (p.saved_track_ids?.length || 0)}
                </div>
              </div>
            </div>
            <Link
              to={`/c/${p.handle}`}
              className="brutal-btn invert !w-full mt-4 justify-center"
              data-testid="my-public-profile"
            >
              view public profile
            </Link>
          </div>
        </aside>

        <div className="lg:col-span-8">
          {tab === "collections" && (
            <>
              <h2 className="font-display font-black text-3xl tracking-tighter mb-4">start a collection.</h2>
              <form onSubmit={create} className="brutal-card-static p-6 space-y-3" data-testid="new-collection-form">
                <input
                  className="brutal-input"
                  placeholder="title (e.g., songs to drive at 3am)"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
                <textarea
                  className="brutal-input"
                  placeholder="a note for your future self"
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                  rows={2}
                />
                <button className="brutal-btn accent" type="submit">
                  create
                </button>
              </form>
              <h2 className="font-display font-black text-3xl tracking-tighter mt-10 mb-4">your collections.</h2>
              <div className="grid md:grid-cols-2 gap-4">
                {collections.map((c) => (
                  <div key={c.id} className="brutal-card-static p-5">
                    <div className="meta-ink">{new Date(c.created_at).toLocaleDateString()}</div>
                    <div className="font-display font-bold text-xl mt-1">{c.title}</div>
                    <p className="font-editorial italic mt-2">{c.note || "—"}</p>
                    <div className="mt-3 flex gap-2">
                      <button className="brutal-btn" type="button" onClick={() => openEdit(c)} disabled={actionLoading}>
                        edit
                      </button>
                      <button className="brutal-btn" type="button" onClick={() => handleDelete(c)} disabled={actionLoading}>
                        delete
                      </button>
                    </div>
                  </div>
                ))}
                {collections.length === 0 && <p className="meta-ink">empty room. fill it slowly.</p>}
              </div>
            </>
          )}

          {tab === "saves" && (
            <>
              <h2 className="font-display font-black text-3xl tracking-tighter mb-4">saved albums.</h2>
              <div className="grid md:grid-cols-2 gap-4 mb-10">
                {(saves.saved_albums || []).map((a) => (
                  <Link key={a.id} to={`/album/${a.id}`} className="brutal-card-static p-5 block">
                    <div className="meta-ink">{a.year}</div>
                    <div className="font-display font-bold text-xl">{a.title}</div>
                  </Link>
                ))}
                {!saves.saved_albums?.length && <p className="meta-ink">no saved albums yet.</p>}
              </div>
              <h2 className="font-display font-black text-3xl tracking-tighter mb-4">saved tracks.</h2>
              <div className="space-y-3">
                {(saves.saved_tracks || []).map((t) => (
                  <Link key={t.id} to={`/track/${t.id}`} className="brutal-card-static p-4 block flex justify-between">
                    <span className="font-display font-bold">{t.title}</span>
                    <span className="meta-ink">{t.duration}</span>
                  </Link>
                ))}
                {!saves.saved_tracks?.length && <p className="meta-ink">no saved tracks yet.</p>}
              </div>
            </>
          )}

          {tab === "write" && (
            <>
              <h2 className="font-display font-black text-3xl tracking-tighter mb-4">write lore.</h2>
              <p className="font-editorial italic mb-6 max-w-xl">
                publish an essay, footnote, or rabbit hole. it will appear on your public profile and in the archive.
              </p>
              <LoreComposer
                onCreated={async () => {
                  await refreshUser();
                }}
              />
            </>
          )}

          {tab === "profile" && (
            <ProfileEditor
              user={user}
              artists={artists}
              onSaved={async () => {
                await refreshUser();
                setSaves(await fetchMySaves().then((r) => r.data));
              }}
            />
          )}
        </div>
      </div>

      <CollectionEditModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        collection={editing}
        onSave={handleSave}
        loading={actionLoading}
      />
    </div>
  );
}


