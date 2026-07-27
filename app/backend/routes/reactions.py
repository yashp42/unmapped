from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from ..database.connection import get_database
from ..dependencies import get_current_user, get_optional_user

router = APIRouter()
VALID_TARGETS = {"lore", "theory", "connection"}

@router.get("/{target_type}/{target_id}")
async def reaction_summary(target_type: str, target_id: str, user: dict | None = Depends(get_optional_user)):
    if target_type not in VALID_TARGETS: raise HTTPException(404, "Unsupported reaction target")
    db = get_database(); query = {"target_type": target_type, "target_id": target_id, "kind": "like"}
    count = await db.reactions.count_documents(query)
    liked = bool(user and await db.reactions.find_one({**query, "user_id": user["id"]}))
    return {"count": count, "liked": liked}

@router.post("/{target_type}/{target_id}")
async def toggle_like(target_type: str, target_id: str, user: dict = Depends(get_current_user)):
    if target_type not in VALID_TARGETS: raise HTTPException(404, "Unsupported reaction target")
    db = get_database(); query = {"target_type": target_type, "target_id": target_id, "kind": "like"}; key = {**query, "user_id": user["id"]}
    if await db.reactions.find_one(key):
        await db.reactions.delete_one(key); return {"count": await db.reactions.count_documents(query), "liked": False}
    await db.reactions.insert_one({**key, "created_at": datetime.now(timezone.utc).isoformat()})
    return {"count": await db.reactions.count_documents(query), "liked": True}
