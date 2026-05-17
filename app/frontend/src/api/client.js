import axios from "axios";

const BASE = process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:8001";
const TOKEN_KEY = "unmapped_access_token";

export const api = axios.create({
  baseURL: `${BASE}/api`,
  withCredentials: true,
});

export function getStoredToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setAuthToken(token) {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    localStorage.removeItem(TOKEN_KEY);
    delete api.defaults.headers.common.Authorization;
  }
}

const stored = getStoredToken();
if (stored) setAuthToken(stored);

let refreshPromise = null;

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (!original || original._retry || error.response?.status !== 401) {
      return Promise.reject(error);
    }
    if (original.url?.includes("/auth/login") || original.url?.includes("/auth/refresh")) {
      return Promise.reject(error);
    }

    original._retry = true;
    if (!refreshPromise) {
      refreshPromise = api.post("/auth/refresh").finally(() => {
        refreshPromise = null;
      });
    }

    try {
      const { data } = await refreshPromise;
      if (data?.access_token) setAuthToken(data.access_token);
      return api(original);
    } catch (refreshError) {
      setAuthToken(null);
      return Promise.reject(refreshError);
    }
  }
);

export const formatApiError = (detail) => {
  if (detail == null) return "Something went wrong.";
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return detail.map((e) => (e?.msg ? e.msg : JSON.stringify(e))).join(" ");
  if (detail?.msg) return detail.msg;
  return String(detail);
};
