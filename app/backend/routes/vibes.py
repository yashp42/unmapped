from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from ..database.connection import db

router = APIRouter()


@router.get("")
async def list_vibes(skip: int = 0, limit: int = 20):
    return await db.vibes.find({}, skip=skip, limit=limit).sort("name", 1).to_list(length=limit)


@router.get("/{vibe_id}")
async def get_vibe(vibe_id: str):
    vibe = await db.vibes.find_one({"id": vibe_id})
    if not vibe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vibe not found")
    return vibe


@router.post("")
async def create_vibe(payload: dict):
    now = datetime.utcnow().isoformat()
    vibe = {"id": str(uuid4()), "created_at": now, "updated_at": now, **payload}
    await db.vibes.insert_one(vibe)
    return vibe
