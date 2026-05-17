import { createContext, useContext, useEffect, useState } from "react";
import { api, setAuthToken } from "./api";

const AuthCtx = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // null = loading, false = anon
  useEffect(() => {
    api.get("/auth/me").then((r) => setUser(r.data)).catch(() => setUser(false));
  }, []);
  const login = async (email, password) => {
    const r = await api.post("/auth/login", { email, password });
    // backend returns { access_token, token_type, user }
    const token = r.data?.access_token;
    if (token) setAuthToken(token);
    setUser(r.data?.user || null);
    return r.data;
  };
  const register = async (email, password, handle) => {
    const r = await api.post("/auth/register", { email, password, handle });
    setUser(r.data);
    return r.data;
  };
  const logout = async () => { await api.post("/auth/logout"); setAuthToken(null); setUser(false); };
  return <AuthCtx.Provider value={{ user, login, register, logout, setUser }}>{children}</AuthCtx.Provider>;
};

export const useAuth = () => useContext(AuthCtx);
