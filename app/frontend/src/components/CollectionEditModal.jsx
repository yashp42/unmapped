import React, { useState, useEffect } from "react";
import LoadingSpinner from "./LoadingSpinner";

export default function CollectionEditModal({ open, onClose, collection, onSave, loading }) {
  const [title, setTitle] = useState("");
  const [note, setNote] = useState("");

  useEffect(() => {
    if (collection) {
      setTitle(collection.title || "");
      setNote(collection.note || "");
    }
  }, [collection]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/50" onClick={() => !loading && onClose()} />
      <div className="brutal-card-static p-6 z-10 w-full max-w-xl">
        <h3 className="font-display font-black text-2xl">Edit collection</h3>
        <div className="mt-4 space-y-2">
          <input className="brutal-input" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="title" />
          <textarea className="brutal-input" value={note} onChange={(e) => setNote(e.target.value)} rows={4} placeholder="note" />
        </div>
        <div className="mt-4 flex gap-2 justify-end">
          <button className="brutal-btn" onClick={() => onClose()} disabled={loading}>Cancel</button>
          <button className="brutal-btn accent" onClick={() => onSave({ ...collection, title, note })} disabled={loading}>
            {loading ? <><LoadingSpinner size={18} /> <span className="ml-2">Saving</span></> : "Save"}
          </button>
        </div>
      </div>
    </div>
  );
}
