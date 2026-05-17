import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";

export default function ContributorsIndex() {
  const [c, setC] = useState([]);
  useEffect(() => { api.get("/contributors").then((r) => setC(r.data)); }, []);
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
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
