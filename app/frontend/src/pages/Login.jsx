import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../lib/auth";
import { formatApiError } from "../lib/api";

export default function Login() {
  const { login } = useAuth();
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");
  const [err, setErr] = useState("");
  const submit = async (e) => {
    e.preventDefault(); setErr("");
    try { await login(email, pw); nav("/my-world"); }
    catch (e) { setErr(formatApiError(e.response?.data?.detail)); }
  };
  return (
    <div className="max-w-md mx-auto px-6 py-20">
      <div className="meta-ink mb-3">return to the archive</div>
      <h1 className="font-display font-black text-5xl tracking-tighter">log in.</h1>
      <p className="font-editorial italic text-xl mt-2">your annotations missed you.</p>
      <form onSubmit={submit} className="brutal-card-static p-7 mt-8 space-y-4">
        <input className="brutal-input" placeholder="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required data-testid="login-email" />
        <input className="brutal-input" placeholder="password" type="password" value={pw} onChange={(e) => setPw(e.target.value)} required data-testid="login-password" />
        {err && <p className="font-mono text-xs bg-[var(--hyperpop)] text-white px-2 py-1" data-testid="login-error">{err}</p>}
        <button className="brutal-btn accent !w-full justify-center" data-testid="login-submit">enter</button>
      </form>
      <p className="font-editorial italic mt-6">new here? <Link to="/register" className="underline" data-testid="goto-register">join the archive</Link></p>
    </div>
  );
}
