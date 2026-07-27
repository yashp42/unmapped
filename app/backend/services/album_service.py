from typing import Any, Optional

from ..database.connection import get_database
from .music_catalog_service import enrich_album


async def get_album_universe(album_id: str) -> Optional[dict[str, Any]]:
    album = await get_database().albums.find_one({"id": album_id}, {"_id": 0})
    if not album:
        return None

    artist = await get_database().artists.find_one({"id": album.get("artist_id")}, {"_id": 0})
    album = await enrich_album(album, (artist or {}).get("name"))

    track_ids = album.get("tracks") or []
    if track_ids:
        tracks_cursor = get_database().tracks.find({"id": {"$in": track_ids}}, {"_id": 0})
        tracks_by_id = {t["id"]: t async for t in tracks_cursor}
        tracks = [tracks_by_id[tid] for tid in track_ids if tid in tracks_by_id]
    else:
        tracks = await get_database().tracks.find({"album_id": album_id}, {"_id": 0}).sort("title", 1).to_list(length=100)

    lore = await get_database().lore.find({"album_id": album_id}, {"_id": 0}).sort("votes", -1).to_list(length=30)
    theories = await get_database().theories.find({"album_id": album_id}, {"_id": 0}).sort("supporters", -1).to_list(length=20)
    transitions = await get_database().transitions.find({"album_id": album_id}, {"_id": 0}).to_list(length=50)

    return {
        "album": album,
        "artist": artist,
        "tracks": tracks,
        "lore": lore,
        "theories": theories,
        "transitions": transitions,
    }
