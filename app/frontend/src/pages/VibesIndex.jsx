import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";

export default function VibesIndex() {
  const [vibes, setVibes] = useState([]);
  useEffect(() => { api.get("/vibes").then((r) => setVibes(r.data)); }, []);
  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="meta-ink mb-3">section 03 · semantic discovery</div>
      <h1 className="font-display font-black text-5xl md:text-7xl tracking-tighter">vibes have names.</h1>
      <p className="font-editorial italic text-xl md:text-2xl mt-3 max-w-2xl">we wrote them down. the community keeps adding more. search by feeling, not genre.</p>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5 mt-10">
        {vibes.map((v) => (
          <Link key={v.id} to={`/vibe/${v.id}`} className="brutal-card p-7 relative grain" style={{ background: v.color }} data-testid={`vibes-index-${v.id}`}>
            <div className="font-display font-black text-3xl lowercase tracking-tighter mix-blend-multiply">{v.name}</div>
            <p className="font-editorial italic text-xl mt-3 mix-blend-multiply">{v.description}</p>
            <p className="font-editorial italic mt-3 mix-blend-multiply">"{v.felt_state}"</p>
            <div className="meta-ink mt-5 mix-blend-multiply">{v.track_count} tracks · {v.curator_count} curators</div>
          </Link>
        ))}
      </div>
    </div>
  );
}
