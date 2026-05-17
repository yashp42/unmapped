import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";
import { toast } from "sonner";
import LoadingSpinner from "../components/LoadingSpinner";

export default function ContributorsIndex() {
  const [c, setC] = useState([]);
  const { user } = useAuth();
  const [loadingId, setLoadingId] = useState(null);
  useEffect(() => { api.get("/contributors").then((r) => setC(r.data)); }, []);

  const remove = async (id) => {
    if (!confirm('Delete contributor?')) return;
    setLoadingId(id);
    try {
      await api.delete(`/contributors/${id}`);
      setC((s)=>s.filter(x=>x.id!==id));
      toast.success('deleted');
    } catch(e) {
      toast.error('delete failed');
    } finally {
      setLoadingId(null);
    }
  };
  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="meta-ink mb-3">section 06 · the keepers</div>
      <h1 className="font-display font-black text-5xl md:text-7xl tracking-tighter">curators.</h1>
      <p className="font-editorial italic text-xl mt-3 max-w-2xl">people who know things. their taste is the algorithm. follow generously.</p>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5 mt-10">
        {c.map((x) => (
          <Link key={x.handle} to={`/c/${x.handle}`} className="brutal-card p-6" data-testid={`contrib-${x.handle}`}>
            <div className="flex items-center gap-3">
              <div className="w-14 h-14 border-2 border-[var(--ink)] bg-[var(--hyperpop)] text-white flex items-center justify-center font-display font-black text-2xl">{x.name[0]?.toUpperCase()}</div>
              <div>
                <div className="font-display font-bold text-lg">@{x.handle}</div>
                <div className="meta-ink">depth {x.depth_score} · {x.scenes.join(", ")}</div>
              </div>
            </div>
            <p className="font-editorial italic mt-3 text-lg">{x.bio}</p>
            <div className="flex gap-2 mt-4">
              <span className="tag-chip">{x.lore_count} lore</span>
              <span className="tag-chip">{x.theory_count} theories</span>
              {user && (
                <div className="ml-auto flex gap-2">
                  <button className="brutal-btn" onClick={async (e)=>{ e.preventDefault(); const name = prompt('name', x.name); if (!name) return; setLoadingId(x.id); try { await api.put(`/contributors/${x.id}`, { name }); setC((s)=>s.map(it=>it.id===x.id?{...it,name}:it)); toast.success('updated'); } catch(e){ toast.error('update failed'); } finally { setLoadingId(null); } }} disabled={loadingId!==null && loadingId!==x.id}>
                    {loadingId===x.id ? <><LoadingSpinner size={16} /> <span className="ml-2">Saving</span></> : 'Edit'}
                  </button>
                  <button className="brutal-btn" onClick={async (e)=>{ e.preventDefault(); await remove(x.id); }} disabled={loadingId!==null && loadingId!==x.id}>
                    {loadingId===x.id ? <><LoadingSpinner size={16} /> <span className="ml-2">Deleting</span></> : 'Delete'}
                  </button>
                </div>
              )}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
