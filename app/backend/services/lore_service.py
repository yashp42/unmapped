from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException, status

from ..database.connection import get_database
from ..schemas.lore import LoreCreate
from .submission_guard import allow_submission
from .audit_service import audit
from .revision_service import snapshot


def _excerpt_from_body(body: str, excerpt: str | None) -> str:
    if excerpt and excerpt.strip():
        return excerpt.strip()
    text = body.strip().replace("\n", " ")
    return text[:280] + ("…" if len(text) > 280 else "")


async def create_lore_entry(payload: LoreCreate, user: dict) -> dict:
    await allow_submission(user["id"], "lore")
    if payload.album_id and payload.target_source != "itunes":
        album = await get_database().albums.find_one({"id": payload.album_id}, {"_id": 0, "id": 1})
        if not album:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Album not found")
    if payload.track_id and payload.target_source != "itunes":
        track = await get_database().tracks.find_one({"id": payload.track_id}, {"_id": 0, "id": 1})
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
        "target_source": payload.target_source,
        "target_label": payload.target_label,
        "author": user["handle"],
        "user_id": user["id"],
        "votes": 0,
        "comments": 0,
        "status": "pending",
        "created_at": now,
        "updated_at": now,
    }
    await get_database().lore.insert_one(doc)
    await snapshot("lore", doc, user["id"], "submitted")
    await audit(user["id"], "lore.submitted", "lore", doc["id"], {"track_id": doc["track_id"], "album_id": doc["album_id"]})
    doc.pop("_id", None)
    return doc


async def get_lore_with_meta(lore_id: str) -> dict | None:
    lore = await get_database().lore.find_one({"id": lore_id}, {"_id": 0})
    if not lore:
        return None
    comment_count = await get_database().comments.count_documents({"target_type": "lore", "target_id": lore_id})
    lore["comments"] = max(lore.get("comments", 0), comment_count)
    return lore
