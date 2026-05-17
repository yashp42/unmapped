from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status, Query, Depends, Response
from typing import List
from database.connection import get_database
from ..schemas.artists import Artist, ArtistIn, ArtistUpdate
from ..dependencies import get_current_user

router = APIRouter()


@router.get("", response_model=List[Artist])
async def list_artists(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    cursor = get_database().artists.find({}, {"_id": 0}).sort("name", 1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


@router.get("/{artist_id}", response_model=Artist)
async def get_artist(artist_id: str):
    artist = await get_database().artists.find_one({"id": artist_id}, {"_id": 0})
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return artist


@router.post("", response_model=Artist, status_code=201)
async def create_artist(payload: ArtistIn, current_user: dict = Depends(get_current_user)):
    now = datetime.utcnow().isoformat()
    artist = payload.model_dump()
    artist.update({"id": str(uuid4()), "created_at": now, "updated_at": now})
    await get_database().artists.insert_one(artist)
    return await get_database().artists.find_one({"id": artist["id"]}, {"_id": 0})


@router.put("/{artist_id}", response_model=Artist)
async def update_artist(artist_id: str, payload: ArtistUpdate, current_user: dict = Depends(get_current_user)):
    artist = await get_database().artists.find_one({"id": artist_id}, {"_id": 0})
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")

    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        return artist

    update_data["updated_at"] = datetime.utcnow().isoformat()
    await get_database().artists.update_one({"id": artist_id}, {"$set": update_data})
    return await get_database().artists.find_one({"id": artist_id}, {"_id": 0})


@router.delete("/{artist_id}", status_code=204)
async def delete_artist(artist_id: str, current_user: dict = Depends(get_current_user)):
    res = await get_database().artists.delete_one({"id": artist_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
