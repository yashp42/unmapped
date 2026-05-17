from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException, status

from ..database.connection import db
from ..schemas.lore import LoreCreate


def _excerpt_from_body(body: str, excerpt: str | None) -> str:
    if excerpt and excerpt.strip():
        return excerpt.strip()
    text = body.strip().replace("\n", " ")
    return text[:280] + ("…" if len(text) > 280 else "")


async def create_lore_entry(payload: LoreCreate, user: dict) -> dict:
    if payload.album_id:
        album = await db.albums.find_one({"id": payload.album_id}, {"_id": 0, "id": 1})
        if not album:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Album not found")
    if payload.track_id:
        track = await db.tracks.find_one({"id": payload.track_id}, {"_id": 0, "id": 1})
        if not track:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Track not found")

    now = datetime.utcnow().isoformat()
    doc = {
        "id": str(uuid4()),
        "title": payload.title.strip(),
        "body": payload.body.strip(),
        "excerpt": _excerpt_from_body(payload.body, payload.excerpt),
        "album_id": payload.album_id,
        "track_id": payload.track_id,
        "depth": payload.depth,
        "author": user["handle"],
        "user_id": user["id"],
        "votes": 0,
        "comments": 0,
        "created_at": now,
        "updated_at": now,
    }
    await db.lore.insert_one(doc)
    doc.pop("_id", None)
    return doc


async def get_lore_with_meta(lore_id: str) -> dict | None:
    lore = await db.lore.find_one({"id": lore_id}, {"_id": 0})
    if not lore:
        return None
    comment_count = await db.comments.count_documents({"target_type": "lore", "target_id": lore_id})
    lore["comments"] = max(lore.get("comments", 0), comment_count)
    return lore
