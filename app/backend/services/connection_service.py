from typing import Any, Optional

from ..database.connection import db


async def build_connection_graph(track_id: Optional[str] = None) -> dict[str, list[dict[str, Any]]]:
    query: dict[str, Any] = {}
    if track_id:
        query = {"$or": [{"source": track_id}, {"target": track_id}]}

    edges = await db.connections.find(query, {"_id": 0}).to_list(length=500)
    if not edges:
        return {"nodes": [], "edges": []}

    track_ids: set[str] = set()
    for edge in edges:
        track_ids.add(edge["source"])
        track_ids.add(edge["target"])

    tracks = await db.tracks.find({"id": {"$in": list(track_ids)}}, {"_id": 0}).to_list(length=500)
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

    return {"nodes": nodes, "edges": graph_edges}
