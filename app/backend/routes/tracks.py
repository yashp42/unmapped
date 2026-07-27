from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from typing import List

from dependencies import require_admin
from schemas.tracks import Track, TrackIn, TrackUpdate
from services.track_service import get_track_detail

router = APIRouter()


@router.get("", response_model=List[Track])
async def list_tracks(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    cursor = get_database().tracks.find({}, {"_id": 0}).sort("title", 1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


@router.get("/{track_id}")
async def get_track(track_id: str):
    detail = await get_track_detail(track_id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return detail


@router.post("", response_model=Track, status_code=201)
async def create_track(payload: TrackIn, current_user: dict = Depends(require_admin)):
    now = datetime.utcnow().isoformat()
    track = payload.model_dump()
    track.update({"id": str(uuid4()), "created_at": now, "updated_at": now})
    await get_database().tracks.insert_one(track)
    return await get_database().tracks.find_one({"id": track["id"]}, {"_id": 0})


@router.put("/{track_id}", response_model=Track)
async def update_track(
    track_id: str,
    payload: TrackUpdate,
    current_user: dict = Depends(require_admin),
):
    track = await get_database().tracks.find_one({"id": track_id}, {"_id": 0})
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")

    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        return track

    update_data["updated_at"] = datetime.utcnow().isoformat()
    await get_database().tracks.update_one({"id": track_id}, {"$set": update_data})
    return await get_database().tracks.find_one({"id": track_id}, {"_id": 0})


@router.delete("/{track_id}", status_code=204)
async def delete_track(track_id: str, current_user: dict = Depends(require_admin)):
    res = await get_database().tracks.delete_one({"id": track_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
