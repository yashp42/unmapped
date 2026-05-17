import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, formatApiError } from "../lib/api";
import { useAuth } from "../lib/auth";
import { toast } from "sonner";

export default function MyWorld() {
  const { user } = useAuth();
  const nav = useNavigate();
  const [collections, setCollections] = useState([]);
  const [title, setTitle] = useState("");
  const [note, setNote] = useState("");

  useEffect(() => { if (user === false) nav("/login"); }, [user, nav]);
  useEffect(() => { if (user && user !== false) api.get("/collections/mine").then((r) => setCollections(r.data)); }, [user]);

  const create = async (e) => {
    e.preventDefault();
    try {
      const r = await api.post("/collections", { title, note, item_ids: [] });
      setCollections([r.data, ...collections]); setTitle(""); setNote("");
      toast.success("collection started");
    } catch (e) { toast.error(formatApiError(e.response?.data?.detail)); }
  };

  if (!user || user === false) return <div className="px-6 py-20 meta-ink">redirecting…</div>;

  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="meta-ink mb-3">your room in the archive</div>
      <h1 className="font-display font-black text-5xl md:text-7xl tracking-tighter">My World.</h1>
      <p className="font-editorial italic text-xl mt-3 max-w-2xl">a personal space. not a profile. not a feed. your collections, your saved holes, your notes.</p>

      <div className="grid lg:grid-cols-12 gap-8 mt-10">
        <aside className="lg:col-span-4">
          <div className="brutal-card-static p-6">
            <div className="meta-ink">signed in as</div>
            <div className="font-display font-black text-3xl tracking-tighter">@{user.handle}</div>
            <p className="font-editorial italic mt-2">{user.bio || "no bio yet."}</p>
            <div className="grid grid-cols-2 gap-2 mt-4">
              <div className="border-2 border-[var(--ink)] p-3"><div className="meta-ink">depth</div><div className="font-display font-black text-2xl">{user.depth_score || 0}</div></div>
              <div className="border-2 border-[var(--ink)] p-3 bg-[var(--acid)]"><div className="meta-ink">collections</div><div className="font-display font-black text-2xl">{collections.length}</div></div>
            </div>
            <Link to={`/c/${user.handle}`} className="brutal-btn invert !w-full mt-4 justify-center" data-testid="my-public-profile">view public profile</Link>
          </div>
        </aside>

        <div className="lg:col-span-8">
          <h2 className="font-display font-black text-3xl tracking-tighter mb-4">start a collection.</h2>
          <form onSubmit={create} className="brutal-card-static p-6 space-y-3" data-testid="new-collection-form">
            <input className="brutal-input" placeholder="title (e.g., songs to drive at 3am)" value={title} onChange={(e) => setTitle(e.target.value)} required data-testid="collection-title" />
            <textarea className="brutal-input" placeholder="a note for your future self" value={note} onChange={(e) => setNote(e.target.value)} rows={2} data-testid="collection-note" />
            <button className="brutal-btn accent" data-testid="create-collection">create</button>
          </form>

          <h2 className="font-display font-black text-3xl tracking-tighter mt-10 mb-4">your collections.</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {collections.map((c) => (
              <div key={c.id} className="brutal-card-static p-5" data-testid={`my-collection-${c.id}`}>
                <div className="meta-ink">{new Date(c.created_at).toLocaleDateString()}</div>
                <div className="font-display font-bold text-xl mt-1">{c.title}</div>
                <p className="font-editorial italic mt-2">{c.note || "—"}</p>
                <div className="meta-ink mt-3">{c.item_ids.length} items</div>
              </div>
            ))}
            {collections.length === 0 && <p className="meta-ink">empty room. fill it slowly.</p>}
          </div>
        </div>
      </div>
    </div>
  );
}
