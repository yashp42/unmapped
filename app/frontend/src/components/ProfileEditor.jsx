import { useEffect, useState } from "react";
import { toast } from "sonner";
import { updateProfile } from "../api/users";
import { formatApiError } from "../lib/api";
import LoadingSpinner from "./LoadingSpinner";
import AvatarUpload from "./AvatarUpload";

const GENRE_SUGGESTIONS = [
  "alt-r&b",
  "art-rock",
  "hyperpop",
  "indie",
  "conscious-hip-hop",
  "experimental",
  "indie folk",
  "abstract-hip-hop",
];

export default function ProfileEditor({ user, artists = [], onSaved }) {
  const [form, setForm] = useState({
    display_name: "",
    bio: "",
    avatar_url: "",
    favorite_genres: [],
    favorite_artist_ids: [],
    patron_album_id: "",
    scenes: [],
  });
  const [genreInput, setGenreInput] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!user) return;
    setForm({
      display_name: user.display_name || "",
      bio: user.bio || "",
      avatar_url: user.avatar_url || "",
      favorite_genres: user.favorite_genres || [],
      favorite_artist_ids: user.favorite_artist_ids || [],
      patron_album_id: user.patron_album_id || "",
      scenes: user.scenes || [],
    });
  }, [user]);

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const addGenre = (g) => {
    const value = (g || genreInput).trim().toLowerCase();
    if (!value || form.favorite_genres.includes(value)) return;
    setForm((f) => ({ ...f, favorite_genres: [...f.favorite_genres, value] }));
    setGenreInput("");
  };

  const removeGenre = (g) => {
    setForm((f) => ({ ...f, favorite_genres: f.favorite_genres.filter((x) => x !== g) }));
  };

  const toggleArtist = (id) => {
    setForm((f) => ({
      ...f,
      favorite_artist_ids: f.favorite_artist_ids.includes(id)
        ? f.favorite_artist_ids.filter((x) => x !== id)
        : [...f.favorite_artist_ids, id],
    }));
  };

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        display_name: form.display_name || null,
        bio: form.bio,
        avatar_url: form.avatar_url || null,
        favorite_genres: form.favorite_genres,
        favorite_artist_ids: form.favorite_artist_ids,
        patron_album_id: form.patron_album_id || null,
        scenes: form.scenes.length ? form.scenes : form.favorite_genres,
      };
      const r = await updateProfile(payload);
      onSaved?.(r.data);
      toast.success("profile updated");
    } catch (err) {
      toast.error(formatApiError(err.response?.data?.detail));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <AvatarUpload user={user} onUploaded={onSaved} />
    <form onSubmit={submit} className="brutal-card-static p-6 space-y-4" data-testid="profile-editor">
      <div>
        <label className="meta-ink block mb-1">display name</label>
        <input className="brutal-input" value={form.display_name} onChange={set("display_name")} placeholder="how you appear in the archive" />
      </div>
      <div>
        <label className="meta-ink block mb-1">bio</label>
        <textarea className="brutal-input" rows={3} value={form.bio} onChange={set("bio")} placeholder="your musical autobiography in a few lines" />
      </div>
      <div>
        <label className="meta-ink block mb-1">avatar url</label>
        <input className="brutal-input" value={form.avatar_url} onChange={set("avatar_url")} placeholder="https://…" />
      </div>
      <div>
        <label className="meta-ink block mb-1">favorite genres / scenes</label>
        <div className="flex flex-wrap gap-2 mb-2">
          {form.favorite_genres.map((g) => (
            <button key={g} type="button" className="tag-chip" onClick={() => removeGenre(g)}>
              {g} ×
            </button>
          ))}
        </div>
        <div className="flex gap-2">
          <input className="brutal-input flex-1" value={genreInput} onChange={(e) => setGenreInput(e.target.value)} placeholder="add a genre" onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), addGenre())} />
          <button type="button" className="brutal-btn" onClick={() => addGenre()}>add</button>
        </div>
        <div className="flex flex-wrap gap-2 mt-2">
          {GENRE_SUGGESTIONS.filter((g) => !form.favorite_genres.includes(g)).map((g) => (
            <button key={g} type="button" className="tag-chip opacity-70" onClick={() => addGenre(g)}>+ {g}</button>
          ))}
        </div>
      </div>
      {artists.length > 0 && (
        <div>
          <label className="meta-ink block mb-2">favorite artists</label>
          <div className="flex flex-wrap gap-2">
            {artists.map((a) => (
              <button
                key={a.id}
                type="button"
                className={`tag-chip ${form.favorite_artist_ids.includes(a.id) ? "bg-[var(--hyperpop)] text-white" : ""}`}
                onClick={() => toggleArtist(a.id)}
              >
                {a.name}
              </button>
            ))}
          </div>
        </div>
      )}
      <div>
        <label className="meta-ink block mb-1">patron album id</label>
        <input className="brutal-input" value={form.patron_album_id} onChange={set("patron_album_id")} placeholder="e.g. blonde" />
      </div>
      <button type="submit" className="brutal-btn accent" disabled={loading}>
        {loading ? <><LoadingSpinner size={16} /> <span className="ml-2">saving</span></> : "save profile"}
      </button>
    </form>
    </div>
  );
}
