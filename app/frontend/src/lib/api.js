import axios from "axios";

const BASE = process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:8000";
export const api = axios.create({
  baseURL: `${BASE}/api`,
  withCredentials: true,
});

export function setAuthToken(token) {
  if (token) api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  else delete api.defaults.headers.common["Authorization"];
}

export const formatApiError = (detail) => {
  if (detail == null) return "Something went wrong.";
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return detail.map((e) => (e?.msg ? e.msg : JSON.stringify(e))).join(" ");
  if (detail?.msg) return detail.msg;
  return String(detail);
};
