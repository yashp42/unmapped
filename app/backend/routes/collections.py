from fastapi import APIRouter, Depends, HTTPException, status
from uuid import uuid4

from ..schemas.collections import CollectionCreate, CollectionOut
from ..dependencies import get_current_user
from ..database.connection import db

router = APIRouter()


@router.post("", response_model=CollectionOut)
async def create_collection(payload: CollectionCreate, current_user: dict = Depends(get_current_user)):
    now = datetime.utcnow().isoformat()
    collection = {
        "id": str(uuid4()),
        "owner_id": current_user["id"],
        "title": payload.title,
        "note": payload.note or "",
        "item_ids": payload.item_ids,
        "created_at": now,
        "updated_at": now,
    }
    await db.collections.insert_one(collection)
    return collection


@router.get("/mine", response_model=list[CollectionOut])
async def get_my_collections(current_user: dict = Depends(get_current_user)):
    collections = await db.collections.find({"owner_id": current_user["id"]}).sort("created_at", -1).to_list(length=100)
    return collections
