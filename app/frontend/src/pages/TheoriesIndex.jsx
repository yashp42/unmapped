import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";

export default function TheoriesIndex() {
  const [theories, setT] = useState([]);
  useEffect(() => { api.get("/theories").then((r) => setT(r.data)); }, []);
  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="meta-ink mb-3">section 05 · contested terrain</div>
      <h1 className="font-display font-black text-5xl md:text-7xl tracking-tighter">theories.</h1>
      <p className="font-editorial italic text-xl mt-3 max-w-2xl">arguments worth having, with citations. co-sign, push back, or open your own.</p>
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
