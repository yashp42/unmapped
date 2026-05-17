from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException, status

from database.connection import get_database
from ..schemas.comments import CommentCreate
from .user_service import enrich_user


TARGET_COLLECTIONS = {
    "lore": ("lore", "comments"),
    "theory": ("theories", "replies"),
}


async def _ensure_target_exists(target_type: str, target_id: str) -> None:
    collection, _ = TARGET_COLLECTIONS[target_type]
    doc = await get_database()[collection].find_one({"id": target_id}, {"_id": 0, "id": 1})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contribution not found")


async def list_comments(target_type: str, target_id: str, limit: int = 50) -> list[dict]:
    await _ensure_target_exists(target_type, target_id)
    cursor = (
        get_database().comments.find({"target_type": target_type, "target_id": target_id}, {"_id": 0})
        .sort("created_at", 1)
        .limit(limit)
    )
    return await cursor.to_list(length=limit)


async def create_comment(payload: CommentCreate, user: dict) -> dict:
    await _ensure_target_exists(payload.target_type, payload.target_id)

    profile = await enrich_user(user, include_private=False) or user
    now = datetime.utcnow().isoformat()
    doc = {
        "id": str(uuid4()),
        "target_type": payload.target_type,
        "target_id": payload.target_id,
        "user_id": user["id"],
        "author_handle": user["handle"],
        "author_display_name": profile.get("display_name"),
        "author_avatar_url": profile.get("avatar_url"),
        "body": payload.body.strip(),
        "created_at": now,
    }
    await get_database().comments.insert_one(doc)

    collection, count_field = TARGET_COLLECTIONS[payload.target_type]
    await get_database()[collection].update_one(
        {"id": payload.target_id},
        {"$inc": {count_field: 1}},
    )

    doc.pop("_id", None)
    return doc


async def get_comment_count(target_type: str, target_id: str) -> int:
    return await get_database().comments.count_documents(
        {"target_type": target_type, "target_id": target_id}
    )
