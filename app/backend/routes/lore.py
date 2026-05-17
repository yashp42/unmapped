from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from ..database.connection import db

router = APIRouter()


@router.get("")
async def list_lore(skip: int = 0, limit: int = 20):
    return await db.lore.find({}, skip=skip, limit=limit).sort("created_at", -1).to_list(length=limit)


@router.get("/{lore_id}")
async def get_lore(lore_id: str):
    lore = await db.lore.find_one({"id": lore_id})
    if not lore:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lore entry not found")
    return lore


@router.post("")
async def create_lore(payload: dict):
    now = datetime.utcnow().isoformat()
    lore = {"id": str(uuid4()), "created_at": now, "updated_at": now, **payload}
    await db.lore.insert_one(lore)
    return lore
