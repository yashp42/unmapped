import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchProfile } from "../api/users";
import { useAuth } from "../lib/auth";
import LoadingSpinner from "../components/LoadingSpinner";

export default function ContributorProfile() {
  const { handle } = useParams();
  const { user } = useAuth();
  const [d, setD] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    setD(null);
    setError(false);
    fetchProfile(handle)
      .then((r) => setD(r.data))
      .catch(() => setError(true));
  }, [handle]);

  if (!d && !error) {
    return (
      <div className="px-6 py-20 meta-ink flex items-center gap-2">
        <LoadingSpinner size={18} /> loading profile…
      </div>
    );
  }
  if (error || !d) return <div className="px-6 py-20 meta-ink">profile not found.</div>;

  const c = d.profile || d.contributor;
  const isOwner = d.is_owner || (user && user.handle === c.handle);
  const initial = (c.display_name || c.handle || "?")[0]?.toUpperCase();
  const favoriteArtists = c.favorite_artists || [];

  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="grid lg:grid-cols-12 gap-8">
        <aside className="lg:col-span-4">
          <div className="brutal-card-static p-7">
            {c.avatar_url ? (
              <img src={c.avatar_url} alt="" className="w-24 h-24 object-cover border-2 border-[var(--ink)]" />
            ) : (
              <div className="w-24 h-24 border-2 border-[var(--ink)] bg-[var(--acid)] flex items-center justify-center font-display font-black text-5xl">
                {initial}
              </div>
            )}
            <div className="meta-ink mt-4">
              {d.type === "contributor" ? "curator" : "member"} · joined {c.joined || c.created_at?.slice?.(0, 10) || "—"}
            </div>
            <h1 className="font-display font-black text-3xl tracking-tighter mt-1">@{c.handle}</h1>
            {c.display_name && c.display_name !== c.handle && (
              <p className="font-display font-bold text-xl mt-1">{c.display_name}</p>
            )}
            <p className="font-editorial italic text-xl mt-3">{c.bio || "—"}</p>
            <div className="flex flex-wrap gap-2 mt-4">
              {(c.scenes || c.favorite_genres || []).map((s) => (
                <span key={s} className="tag-chip">{s}</span>
              ))}
            </div>
            {favoriteArtists.length > 0 && (
              <div className="mt-4">
                <div className="meta-ink mb-1">favorite artists</div>
                <div className="flex flex-wrap gap-2">
                  {favoriteArtists.map((a) => (
                    <span key={a.id} className="tag-chip">{a.name}</span>
                  ))}
                </div>
              </div>
            )}
            <div className="mt-6 grid grid-cols-3 gap-2">
              <div className="border-2 border-[var(--ink)] p-3 text-center">
                <div className="meta-ink">depth</div>
                <div className="font-display font-black text-2xl">{c.depth_score || 0}</div>
              </div>
              <div className="border-2 border-[var(--ink)] p-3 text-center bg-[var(--hyperpop)] text-white">
                <div className="meta-ink !text-white/80">lore</div>
                <div className="font-display font-black text-2xl">{c.lore_count || 0}</div>
              </div>
              <div className="border-2 border-[var(--ink)] p-3 text-center">
                <div className="meta-ink">theory</div>
                <div className="font-display font-black text-2xl">{c.theory_count || 0}</div>
              </div>
            </div>
            {c.patron_album_id && (
              <div className="mt-4">
                <div className="meta-ink mb-1">patron album</div>
                <Link to={`/album/${c.patron_album_id}`} className="brutal-btn invert !w-full justify-center">
                  {c.patron_album_id}
                </Link>
              </div>
            )}
            {isOwner && (
              <div className="mt-4 space-y-2">
                <Link to="/my-world" className="brutal-btn !w-full justify-center block text-center">
                  edit your profile
                </Link>
                <Link to="/my-world" state={{ tab: "write" }} className="brutal-btn accent !w-full justify-center block text-center">
                  write lore
                </Link>
              </div>
            )}
          </div>
        </aside>
        <div className="lg:col-span-8">
          {isOwner && (d.saved_albums?.length > 0 || d.saved_tracks?.length > 0) && (
            <section className="mb-10">
              <div className="meta-ink mb-2">private · only you see this</div>
              <h2 className="font-display font-black text-3xl tracking-tighter">saved.</h2>
              <div className="grid md:grid-cols-2 gap-3 mt-4">
                {(d.saved_albums || []).slice(0, 4).map((a) => (
                  <Link key={a.id} to={`/album/${a.id}`} className="brutal-card-static p-4 block">
                    {a.title}
                  </Link>
                ))}
              </div>
            </section>
          )}
          <div className="meta-ink mb-2">musical autobiography</div>
          <h2 className="font-display font-black text-4xl tracking-tighter">contributions.</h2>
          <div className="mt-6 space-y-4">
            {(d.lore || []).map((l) => (
              <Link key={l.id} to={`/lore/${l.id}`} className="brutal-card-static p-5 block">
                <div className="meta-ink">lore · {l.depth}</div>
                <div className="font-display font-bold text-xl mt-1">{l.title}</div>
                <p className="font-editorial italic mt-2">{l.excerpt}</p>
              </Link>
            ))}
            {(d.theories || []).map((t) => (
              <Link key={t.id} to={`/theory/${t.id}`} className="brutal-card-static p-5 block bg-[var(--parchment-deep)]">
                <div className="meta-ink">theory · {t.stance}</div>
                <div className="font-display font-bold text-xl mt-1">{t.title}</div>
                <p className="font-editorial italic mt-2">{t.abstract}</p>
              </Link>
            ))}
            {(d.lore || []).length === 0 && (d.theories || []).length === 0 && (
              <p className="meta-ink">no contributions yet.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

