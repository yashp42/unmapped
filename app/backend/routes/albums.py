from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from ..database.connection import db

router = APIRouter()


@router.get("")
async def list_albums(skip: int = 0, limit: int = 20):
    return await db.albums.find({}, skip=skip, limit=limit).sort("year", -1).to_list(length=limit)


@router.get("/{album_id}")
async def get_album(album_id: str):
    album = await db.albums.find_one({"id": album_id})
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return album


@router.post("")
async def create_album(payload: dict):
    now = datetime.utcnow().isoformat()
    album = {"id": str(uuid4()), "created_at": now, "updated_at": now, **payload}
    await db.albums.insert_one(album)
    return album
