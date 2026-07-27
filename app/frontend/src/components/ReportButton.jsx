import { Flag } from "lucide-react";
import { api } from "../lib/api";
import { useAuth } from "../lib/auth";
import { toast } from "sonner";
export default function ReportButton({ targetType, targetId }) {
  const { user } = useAuth();
  const report = async () => { if (!user) return toast.error("Sign in to report content."); const reason = window.prompt("Briefly describe the issue"); if (!reason) return; try { await api.post("/reports", { target_type: targetType, target_id: targetId, reason }); toast.success("Report received"); } catch { toast.error("Could not send the report"); } };
  return <button className="tag-chip" onClick={report}><Flag size={13} /> report</button>;
}
