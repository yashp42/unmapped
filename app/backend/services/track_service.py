from typing import Any, Optional

from ..database.connection import get_database
from .music_catalog_service import enrich_track


async def get_track_detail(track_id: str) -> Optional[dict[str, Any]]:
    track = await get_database().tracks.find_one({"id": track_id}, {"_id": 0})
    if not track:
        return None

    artist = await get_database().artists.find_one({"id": track.get("artist_id")}, {"_id": 0})
    album = await get_database().albums.find_one({"id": track.get("album_id")}, {"_id": 0})
    track = await enrich_track(track, (artist or {}).get("name"), album)

    lore = await get_database().lore.find({"track_id": track_id}, {"_id": 0}).sort("votes", -1).to_list(length=20)
    samples = await get_database().sample_chains.find({"track_id": track_id}, {"_id": 0}).to_list(length=20)

    edges = await get_database().connections.find(
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
        connected_tracks = await get_database().tracks.find({"id": {"$in": connected_ids}}, {"_id": 0}).to_list(length=20)

    return {
        "track": track,
        "artist": artist,
        "album": album,
        "lore": lore,
        "samples": samples,
        "connected_tracks": connected_tracks,
    }
