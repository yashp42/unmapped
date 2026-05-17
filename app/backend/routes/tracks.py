from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from ..database.connection import db

router = APIRouter()


@router.get("")
async def list_tracks(skip: int = 0, limit: int = 20):
    return await db.tracks.find({}, skip=skip, limit=limit).sort("title", 1).to_list(length=limit)


@router.get("/{track_id}")
async def get_track(track_id: str):
    track = await db.tracks.find_one({"id": track_id})
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return track


@router.post("")
async def create_track(payload: dict):
    now = datetime.utcnow().isoformat()
    track = {"id": str(uuid4()), "created_at": now, "updated_at": now, **payload}
    await db.tracks.insert_one(track)
    return track
