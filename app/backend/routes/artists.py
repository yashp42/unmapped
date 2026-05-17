from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from ..database.connection import db

router = APIRouter()


@router.get("")
async def list_artists(skip: int = 0, limit: int = 20):
    return await db.artists.find({}, skip=skip, limit=limit).sort("name", 1).to_list(length=limit)


@router.get("/{artist_id}")
async def get_artist(artist_id: str):
    artist = await db.artists.find_one({"id": artist_id})
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return artist


@router.post("")
async def create_artist(payload: dict):
    now = datetime.utcnow().isoformat()
    artist = {"id": str(uuid4()), "created_at": now, "updated_at": now, **payload}
    await db.artists.insert_one(artist)
    return artist
