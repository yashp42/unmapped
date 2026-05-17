from datetime import datetime
from typing import Any, Optional

from database.connection import get_database
from ..utils.security import hash_password, verify_password

DEFAULT_PROFILE_FIELDS = {
    "display_name": None,
    "bio": "",
    "avatar_url": None,
    "favorite_genres": [],
    "favorite_artist_ids": [],
    "saved_album_ids": [],
    "saved_track_ids": [],
    "patron_album_id": None,
    "scenes": [],
}


def _display_name(user: dict) -> str:
    if user.get("display_name"):
        return user["display_name"]
    handle = user.get("handle", "")
    return handle.replace(".", " ").replace("-", " ").title() if handle else "Curator"


async def count_user_contributions(user_id: str, handle: str) -> tuple[int, int]:
    author_keys = {user_id, handle}
    lore_count = await get_database().lore.count_documents({"author": {"$in": list(author_keys)}})
    theory_count = await get_database().theories.count_documents({"author": {"$in": list(author_keys)}})
    user_lore = await get_database().lore.count_documents({"user_id": user_id})
    user_theory = await get_database().theories.count_documents({"user_id": user_id})
    return max(lore_count, user_lore), max(theory_count, user_theory)


async def enrich_user(user: dict | None, include_private: bool = False) -> Optional[dict]:
    if not user:
        return None

    user = {**user}
    user.pop("password_hash", None)
    user.pop("_id", None)

    for key, default in DEFAULT_PROFILE_FIELDS.items():
        user.setdefault(key, default if not isinstance(default, list) else list(default))

    lore_count, theory_count = await count_user_contributions(user["id"], user["handle"])
    user["lore_count"] = lore_count
    user["theory_count"] = theory_count
    user["contributions_count"] = lore_count + theory_count
    user["display_name"] = _display_name(user)

    public = {
        "id": user["id"],
        "handle": user["handle"],
        "role": user.get("role", "user"),
        "display_name": user["display_name"],
        "bio": user.get("bio") or "",
        "avatar_url": user.get("avatar_url"),
        "depth_score": user.get("depth_score", 0),
        "favorite_genres": user.get("favorite_genres", []),
        "favorite_artist_ids": user.get("favorite_artist_ids", []),
        "lore_count": user["lore_count"],
        "theory_count": user["theory_count"],
        "contributions_count": user["contributions_count"],
        "created_at": user.get("created_at", ""),
    }

    if not include_private:
        return public

    return {
        **public,
        "email": user["email"],
        "saved_album_ids": user.get("saved_album_ids", []),
        "saved_track_ids": user.get("saved_track_ids", []),
        "patron_album_id": user.get("patron_album_id"),
        "scenes": user.get("scenes", []),
    }


async def find_user_by_email(email: str) -> Optional[dict]:
    db = get_database()
    users_collection = db["users"]
    return await users_collection.find_one({"email": email})


async def find_user_by_handle(handle: str) -> Optional[dict]:
    db = get_database()
    users_collection = db["users"]
    return await users_collection.find_one({"handle": handle.lower().strip()})


async def find_user_by_id(user_id: str) -> Optional[dict]:
    db = get_database()
    users_collection = db["users"]
    return await users_collection.find_one({"id": user_id})


async def create_user(data: dict) -> dict:
    now = datetime.utcnow().isoformat()
    payload = {
        "id": data["id"],
        "email": data["email"],
        "handle": data["handle"],
        "password_hash": hash_password(data["password"]),
        "role": data.get("role", "user"),
        "depth_score": data.get("depth_score", 0),
        "created_at": now,
        "updated_at": now,
        **DEFAULT_PROFILE_FIELDS,
        "display_name": data.get("display_name"),
        "bio": data.get("bio", ""),
    }
    db = get_database()
    users_collection = db["users"]
    await users_collection.insert_one(payload)
    return await enrich_user(payload, include_private=True)  # type: ignore[return-value]


async def authenticate_user(email: str, password: str) -> Optional[dict]:
    user = await find_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.get("password_hash", "")):
        return None
    return await enrich_user(user, include_private=True)


async def update_user(user_id: str, updates: dict) -> Optional[dict]:
    updates["updated_at"] = datetime.utcnow().isoformat()
    db = get_database()
    users_collection = db["users"]
    await users_collection.update_one({"id": user_id}, {"$set": updates})
    user = await find_user_by_id(user_id)
    return await enrich_user(user, include_private=True)


async def list_users(skip: int = 0, limit: int = 20) -> list[dict]:
    db = get_database()
    users_collection = db["users"]
    cursor = users_collection.find({}, {"_id": 0, "password_hash": 0}).skip(skip).limit(limit).sort("created_at", -1)
    users = await cursor.to_list(length=limit)
    result = []
    for user in users:
        enriched = await enrich_user(user, include_private=False)
        if enriched:
            result.append(enriched)
    return result


async def toggle_saved_album(user_id: str, album_id: str) -> dict[str, Any]:
    user = await find_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")
    saved = list(user.get("saved_album_ids") or [])
    if album_id in saved:
        saved.remove(album_id)
        is_saved = False
    else:
        saved.append(album_id)
        is_saved = True
    await update_user(user_id, {"saved_album_ids": saved})
    return {"saved": is_saved, "saved_album_ids": saved, "saved_track_ids": user.get("saved_track_ids", [])}


async def toggle_saved_track(user_id: str, track_id: str) -> dict[str, Any]:
    user = await find_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")
    saved = list(user.get("saved_track_ids") or [])
    if track_id in saved:
        saved.remove(track_id)
        is_saved = False
    else:
        saved.append(track_id)
        is_saved = True
    await update_user(user_id, {"saved_track_ids": saved})
    return {
        "saved": is_saved,
        "saved_album_ids": user.get("saved_album_ids", []),
        "saved_track_ids": saved,
    }
