from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List

from database.connection import get_database
from ..dependencies import get_current_user
from ..schemas.lore import LoreCreate, LoreOut
from ..services.lore_service import create_lore_entry, get_lore_with_meta

router = APIRouter()


@router.get("", response_model=List[LoreOut])
async def list_lore(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    cursor = get_database().lore.find({}, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


@router.get("/{lore_id}", response_model=LoreOut)
async def get_lore(lore_id: str):
    lore = await get_lore_with_meta(lore_id)
    if not lore:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lore entry not found")
    return lore


@router.post("", response_model=LoreOut, status_code=201)
async def create_lore(payload: LoreCreate, current_user: dict = Depends(get_current_user)):
    return await create_lore_entry(payload, current_user)
