import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "sonner";
import { useAuth } from "../lib/auth";
import { fetchComments, postComment } from "../api/comments";
import { formatApiError } from "../lib/api";
import LoadingSpinner from "./LoadingSpinner";

export default function CommentThread({ targetType, targetId, initialCount = 0 }) {
  const { user } = useAuth();
  const [comments, setComments] = useState([]);
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(true);
  const [posting, setPosting] = useState(false);

  const load = () => {
    setLoading(true);
    fetchComments(targetType, targetId)
      .then((r) => setComments(r.data))
      .catch(() => setComments([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, [targetType, targetId]);

  const submit = async (e) => {
    e.preventDefault();
    if (!body.trim()) return;
    setPosting(true);
    try {
      const r = await postComment({ target_type: targetType, target_id: targetId, body: body.trim() });
      setComments((c) => [...c, r.data]);
      setBody("");
      toast.success("comment posted");
    } catch (err) {
      toast.error(formatApiError(err.response?.data?.detail));
    } finally {
      setPosting(false);
    }
  };

  const count = Math.max(initialCount, comments.length);

  return (
    <section className="mt-12 border-t-2 border-[var(--ink)] pt-8" data-testid="comment-thread">
      <div className="meta-ink mb-2">discussion</div>
      <h2 className="font-display font-black text-3xl tracking-tighter">{count} {count === 1 ? "reply" : "replies"}</h2>

      {user ? (
        <form onSubmit={submit} className="mt-6 brutal-card-static p-4 space-y-3">
          <textarea
            className="brutal-input min-h-[100px]"
            placeholder="add to the circle…"
            value={body}
            onChange={(e) => setBody(e.target.value)}
            required
            data-testid="comment-input"
          />
          <button type="submit" className="brutal-btn accent" disabled={posting}>
            {posting ? <><LoadingSpinner size={16} /> posting</> : "post comment"}
          </button>
        </form>
      ) : (
        <p className="font-editorial italic mt-4">
          <Link to="/login" className="underline">log in</Link> to join the discussion.
        </p>
      )}

      <div className="mt-8 space-y-4">
        {loading && <p className="meta-ink">loading comments…</p>}
        {!loading && comments.length === 0 && (
          <p className="meta-ink font-editorial italic">no replies yet. be the first.</p>
        )}
        {comments.map((c) => (
          <article key={c.id} className="brutal-card-static p-4 flex gap-4" data-testid={`comment-${c.id}`}>
            {c.author_avatar_url ? (
              <img src={c.author_avatar_url} alt="" className="w-10 h-10 object-cover border border-[var(--ink)] shrink-0" />
            ) : (
              <div className="w-10 h-10 border border-[var(--ink)] bg-[var(--acid)] flex items-center justify-center font-display font-bold shrink-0">
                {(c.author_display_name || c.author_handle || "?")[0]?.toUpperCase()}
              </div>
            )}
            <div className="flex-1 min-w-0">
              <div className="flex flex-wrap items-baseline gap-2">
                <Link to={`/c/${c.author_handle}`} className="font-display font-bold">
                  @{c.author_handle}
                </Link>
                <span className="meta-ink text-xs">{new Date(c.created_at).toLocaleString()}</span>
              </div>
              <p className="mt-2 font-editorial leading-relaxed whitespace-pre-wrap">{c.body}</p>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
