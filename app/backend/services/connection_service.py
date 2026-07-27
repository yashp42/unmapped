from typing import Any, Optional
from collections import deque

from database.connection import get_database


async def build_connection_graph(track_id: Optional[str] = None, edge_types: Optional[list[str]] = None) -> dict[str, list[dict[str, Any]]]:
    query: dict[str, Any] = {}
    if track_id:
        query = {"$or": [{"source": track_id}, {"target": track_id}]}
    if edge_types:
        query = {"$and": [query, {"type": {"$in": edge_types}}]} if query else {"type": {"$in": edge_types}}

    edges = await get_database().connections.find(query, {"_id": 0}).to_list(length=500)
    if not edges:
        return {"nodes": [], "edges": []}

    track_ids: set[str] = set()
    for edge in edges:
        track_ids.add(edge["source"])
        track_ids.add(edge["target"])

    tracks = await get_database().tracks.find({"id": {"$in": list(track_ids)}}, {"_id": 0}).to_list(length=500)
    track_map = {t["id"]: t for t in tracks}

    nodes = []
    for tid in track_ids:
        track = track_map.get(tid)
        if not track:
            continue
        nodes.append(
            {
                "id": tid,
                "label": track.get("title", tid),
                "album_id": track.get("album_id"),
                "node_type": "track",
                "artist_id": track.get("artist_id"),
            }
        )

    graph_edges = [
        {
            "source": edge["source"],
            "target": edge["target"],
            "type": edge.get("type"),
            "weight": edge.get("weight", 0.5),
        }
        for edge in edges
    ]

    album_ids = [node["album_id"] for node in nodes if node.get("album_id")]
    lore = await get_database().lore.find({"$or": [{"track_id": {"$in": list(track_ids)}}, {"album_id": {"$in": album_ids}}]}, {"_id": 0}).to_list(length=100)
    theories = await get_database().theories.find({"$or": [{"track_id": {"$in": list(track_ids)}}, {"album_id": {"$in": album_ids}}]}, {"_id": 0}).to_list(length=100)
    for entry in lore:
        entry_id = f"lore:{entry['id']}"
        nodes.append({"id": entry_id, "label": entry.get("title", "Lore entry"), "node_type": "lore", "album_id": entry.get("album_id"), "meta": entry.get("depth")})
        anchor = entry.get("track_id") or next((node["id"] for node in nodes if node.get("album_id") == entry.get("album_id") and node["node_type"] == "track"), None)
        if anchor: graph_edges.append({"source": anchor, "target": entry_id, "type": "lore-attached", "weight": 0.35})
    for entry in theories:
        entry_id = f"theory:{entry['id']}"
        nodes.append({"id": entry_id, "label": entry.get("title", "Theory"), "node_type": "theory", "album_id": entry.get("album_id"), "meta": entry.get("stance")})
        anchor = entry.get("track_id") or next((node["id"] for node in nodes if node.get("album_id") == entry.get("album_id") and node["node_type"] == "track"), None)
        if anchor: graph_edges.append({"source": anchor, "target": entry_id, "type": "theory-attached", "weight": 0.35})
    return {"nodes": nodes, "edges": graph_edges}


async def find_connection_path(from_id: str, to_id: str) -> dict[str, list[dict[str, Any]]]:
    """Shortest relationship path for the map's 'why are these connected?' flow."""
    edges = await get_database().connections.find({}, {"_id": 0}).to_list(length=1000)
    graph: dict[str, list[tuple[str, dict]]] = {}
    for edge in edges:
        graph.setdefault(edge["source"], []).append((edge["target"], edge))
        graph.setdefault(edge["target"], []).append((edge["source"], edge))
    queue = deque([from_id]); previous: dict[str, tuple[str, dict] | None] = {from_id: None}
    while queue:
        current = queue.popleft()
        if current == to_id: break
        for neighbour, edge in graph.get(current, []):
            if neighbour not in previous:
                previous[neighbour] = (current, edge); queue.append(neighbour)
    if to_id not in previous: return {"nodes": [], "edges": []}
    node_ids, path_edges = [to_id], []
    cursor = to_id
    while previous[cursor]:
        parent, edge = previous[cursor]
        path_edges.append(edge); node_ids.append(parent); cursor = parent
    tracks = await get_database().tracks.find({"id": {"$in": node_ids}}, {"_id": 0}).to_list(length=100)
    labels = {track["id"]: track.get("title", track["id"]) for track in tracks}
    return {"nodes": [{"id": node_id, "label": labels.get(node_id, node_id)} for node_id in reversed(node_ids)], "edges": list(reversed(path_edges))}
