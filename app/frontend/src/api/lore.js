import { api } from "./client";

export const createLore = (payload) => api.post("/lore", payload);
export const fetchLore = (id) => api.get(`/lore/${id}`);
export const listLore = (params) => api.get("/lore", { params });
