from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from ..dependencies import get_current_user, get_optional_user
from ..schemas.users import ProfileUpdate, SaveToggleResponse, UserPrivate, UserPublic
from ..services.profile_service import get_profile_by_handle
from ..services.profile_service import _resolve_saved
from ..services.upload_service import upload_avatar
from ..services.user_service import (
    enrich_user,
    list_users,
    toggle_saved_album,
    toggle_saved_track,
    update_user,
)
from ..database.connection import db

router = APIRouter()


@router.get("/me", response_model=UserPrivate)
async def get_me(current_user: dict = Depends(get_current_user)):
    enriched = await enrich_user(current_user, include_private=True)
    if not enriched:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return enriched


@router.post("/me/avatar", response_model=UserPrivate)
async def upload_profile_avatar(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    avatar_url = await upload_avatar(file, current_user["id"])
    updated = await update_user(current_user["id"], {"avatar_url": avatar_url})
    return updated


@router.patch("/me", response_model=UserPrivate)
async def update_me(payload: ProfileUpdate, current_user: dict = Depends(get_current_user)):
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not updates:
        return await enrich_user(current_user, include_private=True)

    if updates.get("favorite_artist_ids"):
        artists = await db.artists.find(
            {"id": {"$in": updates["favorite_artist_ids"]}},
            {"_id": 0, "id": 1},
        ).to_list(length=100)
        valid_ids = {a["id"] for a in artists}
        updates["favorite_artist_ids"] = [i for i in updates["favorite_artist_ids"] if i in valid_ids]

    if updates.get("patron_album_id"):
        album = await db.albums.find_one({"id": updates["patron_album_id"]}, {"_id": 0, "id": 1})
        if not album:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Patron album not found")

    updated = await update_user(current_user["id"], updates)
    return updated


@router.get("/me/saves")
async def get_my_saves(current_user: dict = Depends(get_current_user)):
    user = await enrich_user(current_user, include_private=True)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    saves = await _resolve_saved(user)
    return {
        "saved_album_ids": user.get("saved_album_ids", []),
        "saved_track_ids": user.get("saved_track_ids", []),
        **saves,
    }


@router.post("/me/saves/albums/{album_id}", response_model=SaveToggleResponse)
async def toggle_album_save(album_id: str, current_user: dict = Depends(get_current_user)):
    album = await db.albums.find_one({"id": album_id}, {"_id": 0, "id": 1})
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    result = await toggle_saved_album(current_user["id"], album_id)
    return SaveToggleResponse(**result)


@router.post("/me/saves/tracks/{track_id}", response_model=SaveToggleResponse)
async def toggle_track_save(track_id: str, current_user: dict = Depends(get_current_user)):
    track = await db.tracks.find_one({"id": track_id}, {"_id": 0, "id": 1})
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    result = await toggle_saved_track(current_user["id"], track_id)
    return SaveToggleResponse(**result)


@router.get("/profile/{handle}")
async def get_public_profile(
    handle: str,
    viewer: dict | None = Depends(get_optional_user),
):
    viewer_id = viewer["id"] if viewer else None
    profile = await get_profile_by_handle(handle, viewer_id=viewer_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.get("", response_model=list[UserPublic])
async def list_public_users(skip: int = 0, limit: int = 20):
    return await list_users(skip=skip, limit=limit)
