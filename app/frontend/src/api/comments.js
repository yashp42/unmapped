import { api } from "./client";

export const fetchComments = (targetType, targetId) =>
  api.get("/comments", { params: { target_type: targetType, target_id: targetId } });

export const postComment = (payload) => api.post("/comments", payload);
