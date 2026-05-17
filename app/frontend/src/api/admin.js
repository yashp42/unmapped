import { api } from "./client";

const adminPath = (resource, id) => `/admin/${resource}${id ? `/${id}` : ""}`;

export const listAdminResource = (resource, params = {}) => api.get(adminPath(resource), { params });
export const createAdminResource = (resource, payload) => api.post(adminPath(resource), payload);
export const updateAdminResource = (resource, id, payload) => api.put(adminPath(resource, id), payload);
export const deleteAdminResource = (resource, id) => api.delete(adminPath(resource, id));
