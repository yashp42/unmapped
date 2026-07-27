import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../lib/api";
import CommentThread from "../components/CommentThread";
import LikeButton from "../components/LikeButton";
import ReportButton from "../components/ReportButton";

export default function TheoryPage() {
  const { id } = useParams();
  const [t, setT] = useState(null);
  useEffect(() => {
    api.get(`/theories/${id}`).then((r) => setT(r.data));
  }, [id]);
  if (!t) return <div className="px-6 py-20 meta-ink">loading...</div>;

  return (
    <article className="max-w-3xl mx-auto px-6 py-16">
      <div className="meta-ink mb-3">
        theory / {t.stance} / by{" "}
        {t.author ? (
          <Link to={`/c/${t.author}`} className="underline">
            @{t.author}
          </Link>
        ) : (
          "anonymous"
        )}
      </div>
      <h1 className="font-display font-black text-4xl md:text-6xl tracking-tighter leading-[0.95]">{t.title}</h1>
      <div className="flex flex-wrap gap-3 mt-5">
        {t.album_id && <Link to={`/album/${t.album_id}`} className="tag-chip">album / {t.album_id}</Link>}
        <LikeButton targetType="theory" targetId={t.id} initialCount={t.supporters} />
        <ReportButton targetType="theory" targetId={t.id} />
        <span className="tag-chip" style={{ background: "#FFD479" }}>
          {t.challengers} push back
        </span>
      </div>
      <div className="mt-10 editorial-prose dropcap">
        <p>{t.abstract}</p>
      </div>
      <CommentThread
        targetType="theory"
        targetId={t.id}
        initialCount={t.replies || t.comments || 0}
      />
    </article>
  );
}
