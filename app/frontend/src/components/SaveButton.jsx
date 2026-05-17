import { useState } from "react";
import { Bookmark } from "lucide-react";
import { toast } from "sonner";
import { useAuth } from "../lib/auth";
import { toggleSaveAlbum, toggleSaveTrack } from "../api/users";
import { formatApiError } from "../lib/api";
import LoadingSpinner from "./LoadingSpinner";

export default function SaveButton({ type, id, saved: savedProp, onToggle }) {
  const { user } = useAuth();
  const [saved, setSaved] = useState(!!savedProp);
  const [loading, setLoading] = useState(false);

  if (!user) return null;

  const toggle = async () => {
    setLoading(true);
    try {
      const fn = type === "album" ? toggleSaveAlbum : toggleSaveTrack;
      const r = await fn(id);
      const next = r.data.saved;
      setSaved(next);
      onToggle?.(next, r.data);
      toast.success(next ? "saved to your archive" : "removed from saves");
    } catch (e) {
      toast.error(formatApiError(e.response?.data?.detail));
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      type="button"
      className={`brutal-btn ${saved ? "accent" : ""}`}
      onClick={toggle}
      disabled={loading}
      data-testid={`save-${type}-${id}`}
    >
      {loading ? (
        <LoadingSpinner size={16} />
      ) : (
        <Bookmark size={16} fill={saved ? "currentColor" : "none"} />
      )}
      <span className="ml-2">{saved ? "saved" : "save"}</span>
    </button>
  );
}
