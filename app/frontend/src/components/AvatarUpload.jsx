import { useRef, useState } from "react";
import { Camera } from "lucide-react";
import { toast } from "sonner";
import { uploadAvatar } from "../api/users";
import { formatApiError } from "../lib/api";
import LoadingSpinner from "./LoadingSpinner";

export default function AvatarUpload({ user, onUploaded }) {
  const inputRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const preview = user?.avatar_url;
  const initial = (user?.display_name || user?.handle || "?")[0]?.toUpperCase();

  const onPick = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (!file.type.startsWith("image/")) {
      toast.error("Please choose an image file");
      return;
    }
    setLoading(true);
    try {
      const r = await uploadAvatar(file);
      onUploaded?.(r.data);
      toast.success("avatar updated");
    } catch (err) {
      toast.error(formatApiError(err.response?.data?.detail));
    } finally {
      setLoading(false);
      e.target.value = "";
    }
  };

  return (
    <div className="flex items-start gap-4">
      <button
        type="button"
        className="relative group shrink-0"
        onClick={() => inputRef.current?.click()}
        disabled={loading}
        data-testid="avatar-upload-trigger"
      >
        {preview ? (
          <img src={preview} alt="" className="w-24 h-24 object-cover border-2 border-[var(--ink)]" />
        ) : (
          <div className="w-24 h-24 border-2 border-[var(--ink)] bg-[var(--acid)] flex items-center justify-center font-display font-black text-5xl">
            {initial}
          </div>
        )}
        <span className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center text-white transition-opacity">
          {loading ? <LoadingSpinner size={22} /> : <Camera size={22} />}
        </span>
      </button>
      <div>
        <div className="meta-ink mb-1">profile photo</div>
        <p className="font-editorial italic text-sm max-w-xs">
          JPEG, PNG, or WebP up to 5MB. Uses Cloudinary when configured, otherwise local server storage.
        </p>
        <button type="button" className="brutal-btn mt-3 !text-sm" onClick={() => inputRef.current?.click()} disabled={loading}>
          {loading ? "uploadingâ€¦" : "upload image"}
        </button>
      </div>
      <input ref={inputRef} type="file" accept="image/jpeg,image/png,image/webp,image/gif" className="hidden" onChange={onPick} />
    </div>
  );
}

