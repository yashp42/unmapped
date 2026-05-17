import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../lib/auth";
import { formatApiError } from "../lib/api";

export default function Register() {
  const { register } = useAuth();
  const nav = useNavigate();
  const [form, setForm] = useState({ email: "", password: "", handle: "" });
  const [err, setErr] = useState("");
  const submit = async (e) => {
    e.preventDefault(); setErr("");
    try { await register(form.email, form.password, form.handle); nav("/my-world"); }
    catch (e) { setErr(formatApiError(e.response?.data?.detail)); }
  };
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });
  return (
    <div className="max-w-md mx-auto px-6 py-20">
      <div className="meta-ink mb-3">become a curator</div>
      <h1 className="font-display font-black text-5xl tracking-tighter">join.</h1>
      <p className="font-editorial italic text-xl mt-2">claim a handle. start a body of work.</p>
      <form onSubmit={submit} className="brutal-card-static p-7 mt-8 space-y-4">
        <input className="brutal-input" placeholder="handle (e.g., late.night.fm)" value={form.handle} onChange={set("handle")} required data-testid="register-handle" />
        <input className="brutal-input" placeholder="email" type="email" value={form.email} onChange={set("email")} required data-testid="register-email" />
        <input className="brutal-input" placeholder="password (6+ chars)" type="password" value={form.password} onChange={set("password")} required minLength={6} data-testid="register-password" />
        {err && <p className="font-mono text-xs bg-[var(--hyperpop)] text-white px-2 py-1" data-testid="register-error">{err}</p>}
        <button className="brutal-btn accent !w-full justify-center" data-testid="register-submit">claim your handle</button>
      </form>
      <p className="font-editorial italic mt-6">already inside? <Link to="/login" className="underline" data-testid="goto-login">log in</Link></p>
    </div>
  );
}
