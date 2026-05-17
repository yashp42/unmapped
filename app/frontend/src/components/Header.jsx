import { Link, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../lib/auth";
import { Search, LogOut, User } from "lucide-react";
import { useState } from "react";

const navItems = [
  { to: "/explore", label: "Explore" },
  { to: "/vibes", label: "Vibes" },
  { to: "/connections", label: "Connection Map" },
  { to: "/lore", label: "Lore" },
  { to: "/theories", label: "Theories" },
  { to: "/contributors", label: "Curators" },
];

export default function Header() {
  const { user, logout } = useAuth();
  const nav = useNavigate();
  const [q, setQ] = useState("");
  const onSubmit = (e) => { e.preventDefault(); if (q.trim()) nav(`/search?q=${encodeURIComponent(q.trim())}`); };

  return (
    <header className="sticky top-0 z-40 border-b-2 border-[var(--ink)] backdrop-blur-xl bg-[var(--parchment)]/85" data-testid="site-header">
      <div className="max-w-[1480px] mx-auto px-6 py-3 flex items-center gap-6">
        <Link to="/" className="flex items-center gap-2 group" data-testid="logo-link">
          <span className="font-display font-black text-2xl tracking-tighter">unmapped</span>
          <span className="meta-ink hidden md:inline">/ music culture</span>
        </Link>
        <nav className="hidden lg:flex items-center gap-1 ml-2">
          {navItems.map((it) => (
            <NavLink key={it.to} to={it.to} data-testid={`nav-${it.label.toLowerCase().replace(/ /g, '-')}`}
              className={({ isActive }) =>
                `px-3 py-1.5 font-display font-medium text-sm tracking-tight border-2 border-transparent ${isActive ? 'bg-[var(--ink)] text-[var(--parchment)]' : 'hover:border-[var(--ink)]'}`}>
              {it.label}
            </NavLink>
          ))}
        </nav>
        <form onSubmit={onSubmit} className="flex-1 max-w-md ml-auto hidden md:block">
          <div className="flex items-stretch">
            <input data-testid="header-search-input" value={q} onChange={(e) => setQ(e.target.value)}
              placeholder="search the archive…" className="brutal-input !py-2 text-sm" />
            <button type="submit" className="brutal-btn !py-2 !px-3 -ml-[2px]" data-testid="header-search-submit"><Search size={16} /></button>
          </div>
        </form>
        {user ? (
          <div className="flex items-center gap-2">
            <Link to="/my-world" className="brutal-btn invert !py-1.5 !px-3 text-sm" data-testid="my-world-link"><User size={14} />{user.handle}</Link>
            <button onClick={logout} className="brutal-btn !py-1.5 !px-3 text-sm" data-testid="logout-btn"><LogOut size={14} /></button>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <Link to="/login" className="brutal-btn invert !py-1.5 !px-3 text-sm" data-testid="login-link">login</Link>
            <Link to="/register" className="brutal-btn accent !py-1.5 !px-3 text-sm" data-testid="register-link">join</Link>
          </div>
        )}
      </div>
    </header>
  );
}
