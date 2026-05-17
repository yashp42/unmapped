from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status, Query
from ..dependencies import get_current_user
from typing import List
from database.connection import get_database
from ..schemas.vibes import Vibe

router = APIRouter()


@router.get("", response_model=List[Vibe])
async def list_vibes(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    cursor = get_database().vibes.find({}, {"_id": 0}).sort("name", 1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


@router.get("/{vibe_id}", response_model=Vibe)
async def get_vibe(vibe_id: str):
    vibe = await get_database().vibes.find_one({"id": vibe_id}, {"_id": 0})
    if not vibe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vibe not found")
    return vibe


@router.post("", response_model=Vibe, status_code=201)
async def create_vibe(payload: Vibe, current_user: dict = Depends(get_current_user)):
    now = datetime.utcnow().isoformat()
    vibe = payload.model_dump()
    vibe.update({"id": str(uuid4()), "created_at": now, "updated_at": now})
    await get_database().vibes.insert_one(vibe)
    return vibe
