import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../lib/auth";

export default function AdminRoute({ children }) {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return <div className="max-w-3xl mx-auto px-6 py-20 meta-ink">loading session...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  if (user.role !== "admin") {
    return (
      <div className="max-w-3xl mx-auto px-6 py-20">
        <div className="meta-ink mb-3">restricted archive</div>
        <h1 className="font-display font-black text-5xl tracking-tighter">Admin access required.</h1>
        <p className="font-editorial italic text-xl mt-3">This workspace is reserved for content operations and moderation.</p>
      </div>
    );
  }

  return children;
}
