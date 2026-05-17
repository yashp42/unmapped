from typing import Any, Optional

from ..database.connection import db


async def get_track_detail(track_id: str) -> Optional[dict[str, Any]]:
    track = await db.tracks.find_one({"id": track_id}, {"_id": 0})
    if not track:
        return None

    artist = await db.artists.find_one({"id": track.get("artist_id")}, {"_id": 0})
    album = await db.albums.find_one({"id": track.get("album_id")}, {"_id": 0})

    lore = await db.lore.find({"track_id": track_id}, {"_id": 0}).sort("votes", -1).to_list(length=20)
    samples = await db.sample_chains.find({"track_id": track_id}, {"_id": 0}).to_list(length=20)

    vibe_ids = track.get("vibe_ids") or []
    vibes = []
    if vibe_ids:
        vibes = await db.vibes.find({"id": {"$in": vibe_ids}}, {"_id": 0}).to_list(length=20)

    edges = await db.connections.find(
        {"$or": [{"source": track_id}, {"target": track_id}]},
        {"_id": 0},
    ).to_list(length=50)

    connected_ids: list[str] = []
    for edge in edges:
        other = edge["target"] if edge["source"] == track_id else edge["source"]
        if other != track_id:
            connected_ids.append(other)

    connected_tracks = []
    if connected_ids:
        connected_tracks = await db.tracks.find({"id": {"$in": connected_ids}}, {"_id": 0}).to_list(length=20)

    return {
        "track": track,
        "artist": artist,
        "album": album,
        "lore": lore,
        "samples": samples,
        "vibes": vibes,
        "connected_tracks": connected_tracks,
    }
