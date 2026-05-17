import { api } from "./client";

export const fetchMe = () => api.get("/users/me");
export const updateProfile = (payload) => api.patch("/users/me", payload);
export const fetchProfile = (handle) => api.get(`/users/profile/${handle}`);
export const fetchMySaves = () => api.get("/users/me/saves");
export const toggleSaveAlbum = (albumId) => api.post(`/users/me/saves/albums/${albumId}`);
export const toggleSaveTrack = (trackId) => api.post(`/users/me/saves/tracks/${trackId}`);

export const uploadAvatar = (file) => {
  const form = new FormData();
  form.append("file", file);
  return api.post("/users/me/avatar", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};
