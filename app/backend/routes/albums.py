from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from typing import List

from database.connection import get_database
from dependencies import require_admin
from schemas.albums import Album, AlbumIn, AlbumUpdate
from services.album_service import get_album_universe

router = APIRouter()


@router.get("", response_model=List[Album])
async def list_albums(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    cursor = get_database().albums.find({}, {"_id": 0}).sort("year", -1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


@router.get("/{album_id}")
async def get_album(album_id: str):
    universe = await get_album_universe(album_id)
    if not universe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return universe


@router.post("", response_model=Album, status_code=201)
async def create_album(payload: AlbumIn, current_user: dict = Depends(require_admin)):
    now = datetime.utcnow().isoformat()
    album = payload.model_dump()
    album.update({"id": str(uuid4()), "created_at": now, "updated_at": now})
    await get_database().albums.insert_one(album)
    return await get_database().albums.find_one({"id": album["id"]}, {"_id": 0})


@router.put("/{album_id}", response_model=Album)
async def update_album(
    album_id: str,
    payload: AlbumUpdate,
    current_user: dict = Depends(require_admin),
):
    album = await get_database().albums.find_one({"id": album_id}, {"_id": 0})
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")

    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        return album

    update_data["updated_at"] = datetime.utcnow().isoformat()
    await get_database().albums.update_one({"id": album_id}, {"$set": update_data})
    return await get_database().albums.find_one({"id": album_id}, {"_id": 0})


@router.delete("/{album_id}", status_code=204)
async def delete_album(album_id: str, current_user: dict = Depends(require_admin)):
    res = await get_database().albums.delete_one({"id": album_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
