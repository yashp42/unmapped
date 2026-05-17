import { useEffect, useRef, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import ForceGraph2D from "react-force-graph-2d";
import { api } from "../lib/api";

export default function ConnectionMap() {
  const [params] = useSearchParams();
  const focus = params.get("track");
  const [data, setData] = useState({ nodes: [], links: [] });
  const [hover, setHover] = useState(null);
  const nav = useNavigate();
  const fgRef = useRef();

  useEffect(() => {
    const url = focus ? `/connections/graph?track_id=${focus}` : "/connections/graph";
    api.get(url).then((r) => {
      const links = r.data.edges.map((e) => ({ ...e, source: e.source, target: e.target }));
      setData({ nodes: r.data.nodes, links });
    });
  }, [focus]);

  const albumColor = (id) => ({ blonde: "#F5E6B3", "to-pimp-a-butterfly": "#3B2E1F", "in-rainbows": "#C45B2E", igor: "#E84C8A", ctrl: "#8FB89C", "1000-gecs": "#00E5FF" }[id] || "#FF1493");

  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="meta-ink mb-2">graph · the connection map</div>
      <div className="flex items-end justify-between flex-wrap gap-3">
        <h1 className="font-display font-black text-5xl md:text-7xl tracking-tighter">the map.</h1>
        <p className="font-editorial italic text-xl max-w-md">every line is a reason to listen to another song. drag, zoom, click a node.</p>
      </div>

      <div className="brutal-card-static mt-8 relative overflow-hidden" style={{ height: "640px", background: "#fffdf6" }} data-testid="connection-graph">
        <ForceGraph2D
          ref={fgRef}
          graphData={data}
          backgroundColor="#fffdf6"
          nodeRelSize={6}
          linkColor={() => "#111"}
          linkWidth={(l) => 1 + (l.weight || 0.5) * 2}
          nodeLabel="label"
          onNodeHover={setHover}
          onNodeClick={(n) => nav(`/track/${n.id}`)}
          nodeCanvasObject={(node, ctx, globalScale) => {
            const label = node.label;
            const fontSize = 13 / globalScale;
            ctx.font = `700 ${fontSize}px 'Cabinet Grotesk', sans-serif`;
            ctx.fillStyle = albumColor(node.album_id);
            ctx.beginPath();
            ctx.arc(node.x, node.y, 7, 0, 2 * Math.PI);
            ctx.fill();
            ctx.strokeStyle = "#111";
            ctx.lineWidth = 1.5;
            ctx.stroke();
            ctx.fillStyle = "#111";
            ctx.textAlign = "left";
            ctx.fillText(label, node.x + 10, node.y + 4);
          }}
          cooldownTicks={120}
        />
        {hover && (
          <div className="absolute top-3 right-3 brutal-card-static p-3 bg-white" style={{maxWidth: 240}}>
            <div className="meta-ink">{hover.album_id}</div>
            <div className="font-display font-bold text-lg">{hover.label}</div>
            <div className="meta-ink mt-1">click to enter</div>
          </div>
        )}
      </div>

      <div className="mt-6 flex flex-wrap gap-3">
        <div className="meta-ink mr-2">edge types →</div>
        {[["album-sibling", "track lives in same record"], ["mood-cousin", "shares an emotional texture"], ["lyrical-twin", "rhymes the same idea"], ["production-lineage", "shares producer DNA"], ["scene-overlap", "same room, different night"]].map(([t, d]) => (
          <span key={t} className="tag-chip"><strong>{t}</strong> · {d}</span>
        ))}
      </div>
    </div>
  );
}
