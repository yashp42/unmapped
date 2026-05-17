import { useEffect, useMemo, useState } from "react";
import { toast } from "sonner";
import {
  createAdminResource,
  deleteAdminResource,
  listAdminResource,
  updateAdminResource,
} from "../api/admin";
import { formatApiError } from "../lib/api";
import LoadingSpinner from "../components/LoadingSpinner";

const RESOURCES = [
  {
    id: "artists",
    label: "Artists",
    titleField: "name",
    fields: [
      { name: "name", label: "Name", required: true },
      { name: "bio", label: "Bio", type: "textarea" },
      { name: "aliases", label: "Aliases", type: "csv" },
    ],
  },
  {
    id: "albums",
    label: "Albums",
    titleField: "title",
    fields: [
      { name: "title", label: "Title", required: true },
      { name: "artist_id", label: "Artist ID" },
      { name: "artist_name", label: "Artist name" },
      { name: "year", label: "Year", type: "number" },
      { name: "motifs", label: "Motifs", type: "csv" },
      { name: "color", label: "Cover color" },
      { name: "universe_tagline", label: "Universe tagline" },
    ],
  },
  {
    id: "tracks",
    label: "Tracks",
    titleField: "title",
    fields: [
      { name: "title", label: "Title", required: true },
      { name: "artist_id", label: "Artist ID" },
      { name: "artist_name", label: "Artist name" },
      { name: "album_id", label: "Album ID" },
      { name: "duration_seconds", label: "Duration seconds", type: "number" },
    ],
  },
  {
    id: "lore",
    label: "Lore",
    titleField: "title",
    fields: [
      { name: "title", label: "Title", required: true },
      { name: "body", label: "Body", type: "textarea", required: true },
      { name: "excerpt", label: "Excerpt", type: "textarea" },
      { name: "album_id", label: "Album ID" },
      { name: "track_id", label: "Track ID" },
      { name: "depth", label: "Depth" },
    ],
    createOnly: true,
  },
  {
    id: "theories",
    label: "Theories",
    titleField: "title",
    fields: [
      { name: "title", label: "Title", required: true },
      { name: "stance", label: "Stance" },
      { name: "abstract", label: "Abstract", type: "textarea" },
      { name: "album_id", label: "Album ID" },
      { name: "track_id", label: "Track ID" },
      { name: "citations", label: "Citations", type: "csv" },
    ],
  },
  {
    id: "relationships",
    label: "Relationships",
    titleField: "label",
    fields: [
      { name: "source_type", label: "Source type", required: true },
      { name: "source_id", label: "Source ID", required: true },
      { name: "target_type", label: "Target type", required: true },
      { name: "target_id", label: "Target ID", required: true },
      { name: "type", label: "Relationship type", required: true },
      { name: "label", label: "Label" },
      { name: "description", label: "Description", type: "textarea" },
      { name: "weight", label: "Weight", type: "number" },
      { name: "tags", label: "Tags", type: "csv" },
    ],
  },
];

const emptyForm = (fields) =>
  fields.reduce((acc, field) => {
    acc[field.name] = field.type === "csv" ? [] : "";
    return acc;
  }, {});

const toInputValue = (value, field) => {
  if (field.type === "csv") return Array.isArray(value) ? value.join(", ") : "";
  return value ?? "";
};

const normalizeValue = (value, field) => {
  if (field.type === "csv") {
    return value
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);
  }
  if (field.type === "number") {
    return value === "" ? null : Number(value);
  }
  return value === "" ? null : value;
};

export default function AdminCMS() {
  const [activeId, setActiveId] = useState("artists");
  const active = useMemo(() => RESOURCES.find((resource) => resource.id === activeId), [activeId]);
  const [items, setItems] = useState([]);
  const [form, setForm] = useState(() => emptyForm(RESOURCES[0].fields));
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setForm(emptyForm(active.fields));
    setEditingId(null);
    setLoading(true);
    listAdminResource(active.id, { limit: 50 })
      .then((response) => setItems(response.data))
      .catch((error) => toast.error(formatApiError(error.response?.data?.detail)))
      .finally(() => setLoading(false));
  }, [active]);

  const payload = () =>
    active.fields.reduce((acc, field) => {
      const value = normalizeValue(String(form[field.name] ?? ""), field);
      if (value !== null) acc[field.name] = value;
      return acc;
    }, {});

  const reset = () => {
    setForm(emptyForm(active.fields));
    setEditingId(null);
  };

  const refresh = async () => {
    const response = await listAdminResource(active.id, { limit: 50 });
    setItems(response.data);
  };

  const submit = async (event) => {
    event.preventDefault();
    setSaving(true);
    try {
      if (editingId && !active.createOnly) {
        await updateAdminResource(active.id, editingId, payload());
        toast.success(`${active.label} updated`);
      } else {
        await createAdminResource(active.id, payload());
        toast.success(`${active.label} created`);
      }
      reset();
      await refresh();
    } catch (error) {
      toast.error(formatApiError(error.response?.data?.detail));
    } finally {
      setSaving(false);
    }
  };

  const edit = (item) => {
    setEditingId(item.id);
    setForm(
      active.fields.reduce((acc, field) => {
        acc[field.name] = toInputValue(item[field.name], field);
        return acc;
      }, {})
    );
  };

  const remove = async (item) => {
    if (!confirm(`Delete ${item[active.titleField] || item.id}?`)) return;
    setSaving(true);
    try {
      await deleteAdminResource(active.id, item.id);
      setItems((current) => current.filter((candidate) => candidate.id !== item.id));
      toast.success(`${active.label} deleted`);
      if (editingId === item.id) reset();
    } catch (error) {
      toast.error(formatApiError(error.response?.data?.detail));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-[1480px] mx-auto px-6 py-12">
      <div className="meta-ink mb-3">internal archive operations</div>
      <h1 className="font-display font-black text-5xl md:text-7xl tracking-tighter">Admin CMS.</h1>
      <p className="font-editorial italic text-xl mt-3 max-w-2xl">
        Create and maintain canonical music culture records before they enter the public graph.
      </p>

      <div className="flex flex-wrap gap-2 mt-8">
        {RESOURCES.map((resource) => (
          <button
            key={resource.id}
            className={`brutal-btn ${activeId === resource.id ? "accent" : ""}`}
            type="button"
            onClick={() => setActiveId(resource.id)}
          >
            {resource.label}
          </button>
        ))}
      </div>

      <div className="grid lg:grid-cols-12 gap-8 mt-8">
        <section className="lg:col-span-5">
          <form onSubmit={submit} className="brutal-card-static p-6 space-y-3">
            <div>
              <div className="meta-ink">{editingId ? `editing ${editingId}` : `new ${active.label.toLowerCase()}`}</div>
              <h2 className="font-display font-black text-3xl tracking-tighter">{active.label}</h2>
            </div>

            {active.fields.map((field) => (
              <label key={field.name} className="block">
                <span className="meta-ink block mb-1">{field.label}</span>
                {field.type === "textarea" ? (
                  <textarea
                    className="brutal-input"
                    rows={4}
                    value={form[field.name] ?? ""}
                    required={field.required}
                    onChange={(event) => setForm({ ...form, [field.name]: event.target.value })}
                  />
                ) : (
                  <input
                    className="brutal-input"
                    type={field.type === "number" ? "number" : "text"}
                    step={field.name === "weight" ? "0.1" : undefined}
                    value={form[field.name] ?? ""}
                    required={field.required}
                    onChange={(event) => setForm({ ...form, [field.name]: event.target.value })}
                  />
                )}
              </label>
            ))}

            <div className="flex gap-2 pt-2">
              <button className="brutal-btn accent" type="submit" disabled={saving}>
                {saving ? <><LoadingSpinner size={16} /> <span className="ml-2">Saving</span></> : editingId ? "save" : "create"}
              </button>
              <button className="brutal-btn" type="button" onClick={reset} disabled={saving}>
                clear
              </button>
            </div>
          </form>
        </section>

        <section className="lg:col-span-7">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-display font-black text-3xl tracking-tighter">records.</h2>
            {loading && <LoadingSpinner size={18} />}
          </div>
          <div className="space-y-3">
            {items.map((item) => (
              <article key={item.id} className="brutal-card-static p-5">
                <div className="flex items-start gap-4">
                  <div className="flex-1">
                    <div className="meta-ink">{item.id}</div>
                    <h3 className="font-display font-bold text-xl">
                      {item[active.titleField] || item.title || item.name || item.type}
                    </h3>
                    <p className="font-editorial italic mt-1 line-clamp-2">
                      {item.bio || item.abstract || item.excerpt || item.description || item.artist_name || "No description yet."}
                    </p>
                  </div>
                  <div className="flex gap-2">
                    {!active.createOnly && (
                      <button className="brutal-btn" type="button" onClick={() => edit(item)} disabled={saving}>
                        edit
                      </button>
                    )}
                    <button className="brutal-btn" type="button" onClick={() => remove(item)} disabled={saving}>
                      delete
                    </button>
                  </div>
                </div>
              </article>
            ))}
            {!loading && items.length === 0 && <p className="meta-ink">No records yet.</p>}
          </div>
        </section>
      </div>
    </div>
  );
}
