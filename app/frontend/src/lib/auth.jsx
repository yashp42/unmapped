import { createContext, useContext, useEffect, useState } from "react";
import { api, setAuthToken, getStoredToken } from "../api/client";
import { fetchMe } from "../api/users";

const AuthCtx = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadSession = async () => {
    const token = getStoredToken();
    if (token) setAuthToken(token);
    try {
      const r = await fetchMe();
      setUser(r.data);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSession();
  }, []);

  const login = async (email, password) => {
    const r = await api.post("/auth/login", { email, password });
    const token = r.data?.access_token;
    if (token) setAuthToken(token);
    if (token) {
      const me = await fetchMe();
      setUser(me.data);
    } else {
      setUser(r.data?.user || null);
    }
    return r.data;
  };

  const register = async (email, password, handle) => {
    await api.post("/auth/register", { email, password, handle });
    return login(email, password);
  };

  const logout = async () => {
    await api.post("/auth/logout");
    setAuthToken(null);
    setUser(null);
  };

  const refreshUser = async () => {
    const r = await fetchMe();
    setUser(r.data);
    return r.data;
  };

  return (
    <AuthCtx.Provider value={{ user, loading, login, register, logout, setUser, refreshUser }}>
      {children}
    </AuthCtx.Provider>
  );
};

export const useAuth = () => useContext(AuthCtx);
