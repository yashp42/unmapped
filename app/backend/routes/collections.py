from fastapi import APIRouter, Depends, HTTPException, status, Response
from uuid import uuid4
from datetime import datetime

from ..schemas.collections import CollectionCreate, CollectionOut
from ..dependencies import get_current_user
from ..database.connection import get_database

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
    await get_database().collections.insert_one(collection)
    return collection


@router.get("/mine", response_model=list[CollectionOut])
async def get_my_collections(current_user: dict = Depends(get_current_user)):
    collections = await get_database().collections.find({"owner_id": current_user["id"]}).sort("created_at", -1).to_list(length=100)
    return collections


@router.put("/{collection_id}", response_model=CollectionOut)
async def update_collection(collection_id: str, payload: CollectionCreate, current_user: dict = Depends(get_current_user)):
    coll = await get_database().collections.find_one({"id": collection_id}, {"_id": 0})
    if not coll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    if coll["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    update_data = {"title": payload.title, "note": payload.note or "", "item_ids": payload.item_ids, "updated_at": datetime.utcnow().isoformat()}
    await get_database().collections.update_one({"id": collection_id}, {"$set": update_data})
    return await get_database().collections.find_one({"id": collection_id}, {"_id": 0})


@router.delete("/{collection_id}", status_code=204)
async def delete_collection(collection_id: str, current_user: dict = Depends(get_current_user)):
    coll = await get_database().collections.find_one({"id": collection_id}, {"_id": 0})
    if not coll:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    if coll["owner_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    res = await get_database().collections.delete_one({"id": collection_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
