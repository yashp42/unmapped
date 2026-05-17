from fastapi import APIRouter, Depends
from ..dependencies import get_current_user
from ..services.user_service import list_users, find_user_by_handle

router = APIRouter()


@router.get("/me")
async def get_current():
    return await get_current_user()


@router.get("/profile/{handle}")
async def get_profile(handle: str):
    user = await find_user_by_handle(handle)
    if not user:
        return {"detail": "User not found"}
    return {
        "id": user["id"],
        "handle": user["handle"],
        "bio": user.get("bio", ""),
        "depth_score": user.get("depth_score", 0),
        "created_at": user.get("created_at"),
    }


@router.get("", summary="List public users")
async def list_public_users(skip: int = 0, limit: int = 20):
    return await list_users(skip=skip, limit=limit)
