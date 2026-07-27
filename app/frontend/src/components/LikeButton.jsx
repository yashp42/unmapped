import { useEffect, useState } from "react";
import { Heart } from "lucide-react";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";
export default function LikeButton({ targetType, targetId, initialCount = 0 }) {
  const { user } = useAuth(); const [state, setState] = useState({ count: initialCount, liked: false });
  useEffect(() => { api.get(`/reactions/${targetType}/${targetId}`).then((r) => setState(r.data)).catch(() => {}); }, [targetType, targetId]);
  const toggle = async (e) => { e.preventDefault(); e.stopPropagation(); if (!user) return; const r = await api.post(`/reactions/${targetType}/${targetId}`); setState(r.data); };
  return <button onClick={toggle} className={`tag-chip ${state.liked ? "bg-[var(--hyperpop)] text-white" : ""}`}><Heart size={13} fill={state.liked ? "currentColor" : "none"} /> {state.count}</button>;
}
