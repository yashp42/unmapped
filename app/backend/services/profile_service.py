from typing import Any, Optional

from ..database.connection import get_database
from .user_service import enrich_user, find_user_by_handle


async def find_contributor_by_handle(handle: str) -> Optional[dict]:
    return await get_database().contributors.find_one({"handle": handle}, {"_id": 0})


async def find_contributor_by_id(contributor_id: str) -> Optional[dict]:
    return await get_database().contributors.find_one({"id": contributor_id}, {"_id": 0})


async def _fetch_contributions(author_keys: set[str]) -> tuple[list[dict], list[dict]]:
    if not author_keys:
        return [], []
    query = {"$or": [{"author": {"$in": list(author_keys)}}, {"user_id": {"$in": list(author_keys)}}]}
    lore = await get_database().lore.find(query, {"_id": 0}).sort("votes", -1).limit(30).to_list(length=30)
    theories = await get_database().theories.find(query, {"_id": 0}).sort("supporters", -1).limit(30).to_list(length=30)
    return lore, theories


async def _resolve_artists(artist_ids: list[str]) -> list[dict]:
    if not artist_ids:
        return []
    return await get_database().artists.find({"id": {"$in": artist_ids}}, {"_id": 0}).to_list(length=50)


async def _resolve_saved(user: dict) -> dict[str, list[dict]]:
    album_ids = user.get("saved_album_ids") or []
    track_ids = user.get("saved_track_ids") or []
    albums = []
    tracks = []
    if album_ids:
        albums = await get_database().albums.find({"id": {"$in": album_ids}}, {"_id": 0}).to_list(length=100)
    if track_ids:
        tracks = await get_database().tracks.find({"id": {"$in": track_ids}}, {"_id": 0}).to_list(length=100)
    return {"saved_albums": albums, "saved_tracks": tracks}


def _contributor_card(contributor: dict) -> dict[str, Any]:
    return {
        "id": contributor["id"],
        "handle": contributor.get("handle", ""),
        "display_name": contributor.get("name") or contributor.get("handle", ""),
        "bio": contributor.get("bio", ""),
        "avatar_url": contributor.get("avatar_url"),
        "depth_score": contributor.get("depth_score", 0),
        "lore_count": contributor.get("lore_count", 0),
        "theory_count": contributor.get("theory_count", 0),
        "contributions_count": (contributor.get("lore_count") or 0) + (contributor.get("theory_count") or 0),
        "favorite_genres": contributor.get("scenes", []),
        "favorite_artist_ids": [],
        "patron_album_id": contributor.get("patron_album"),
        "scenes": contributor.get("scenes", []),
        "joined": contributor.get("joined"),
        "created_at": contributor.get("joined") or contributor.get("created_at", ""),
    }


async def get_profile_by_handle(handle: str, viewer_id: Optional[str] = None) -> Optional[dict[str, Any]]:
    handle = handle.strip().lower()

    user = await find_user_by_handle(handle)
    if user:
        profile = await enrich_user(user, include_private=False)
        author_keys = {user["id"], user["handle"]}
        lore, theories = await _fetch_contributions(author_keys)
        favorite_artists = await _resolve_artists(profile.get("favorite_artist_ids", []))

        payload: dict[str, Any] = {
            "type": "user",
            "profile": {
                **profile,
                "patron_album_id": user.get("patron_album_id"),
                "scenes": user.get("scenes", []),
                "joined": user.get("created_at", "")[:10] if user.get("created_at") else None,
                "favorite_artists": favorite_artists,
            },
            "lore": lore,
            "theories": theories,
            "is_owner": viewer_id == user["id"] if viewer_id else False,
        }

        if payload["is_owner"]:
            private = await enrich_user(user, include_private=True)
            saves = await _resolve_saved(private)  # type: ignore[arg-type]
            payload["saved_albums"] = saves["saved_albums"]
            payload["saved_tracks"] = saves["saved_tracks"]
            payload["saved_album_ids"] = private.get("saved_album_ids", [])
            payload["saved_track_ids"] = private.get("saved_track_ids", [])

        return payload

    contributor = await find_contributor_by_handle(handle)
    if not contributor:
        contributor = await find_contributor_by_id(handle)

    if not contributor:
        return None

    card = _contributor_card(contributor)
    author_keys = {contributor["id"], contributor.get("handle", "")}
    lore, theories = await _fetch_contributions(author_keys)

    return {
        "type": "contributor",
        "profile": card,
        "contributor": card,
        "lore": lore,
        "theories": theories,
        "is_owner": False,
    }
