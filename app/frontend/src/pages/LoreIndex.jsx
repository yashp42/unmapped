import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";

export default function LoreIndex() {
  const [lore, setLore] = useState([]);
  useEffect(() => { api.get("/lore").then((r) => setLore(r.data)); }, []);
  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="meta-ink mb-3">section 04 · the deep archive</div>
      <h1 className="font-display font-black text-5xl md:text-7xl tracking-tighter">Lore.</h1>
      <p className="font-editorial italic text-xl md:text-2xl mt-3 max-w-2xl">the long footnotes. the second listen. the hidden context. read carefully.</p>
      <div className="grid md:grid-cols-2 gap-5 mt-10">
        {lore.map((l, i) => (
          <Link key={l.id} to={`/lore/${l.id}`} className="brutal-card p-7 block" data-testid={`lore-index-${l.id}`}>
            <div className="meta-ink mb-2">entry · {String(i+1).padStart(3,'0')} · {l.depth}</div>
            <h3 className="font-display font-bold text-2xl tracking-tight">{l.title}</h3>
            <p className="font-editorial italic text-lg mt-3 line-clamp-3">{l.excerpt}</p>
            <div className="flex items-center justify-between mt-4">
              <span className="meta-ink">by {l.author}</span>
              <span className="tag-chip">{l.votes}↑ · {l.comments} replies</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
