from fastapi import APIRouter, Depends, Query

from dependencies import get_current_user
from schemas.comments import CommentCreate, CommentOut
from services.comment_service import create_comment, list_comments

router = APIRouter()


@router.get("", response_model=list[CommentOut])
async def get_comments(
    target_type: str = Query(..., pattern="^(lore|theory)$"),
    target_id: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=100),
):
    return await list_comments(target_type, target_id, limit=limit)


@router.post("", response_model=CommentOut, status_code=201)
async def post_comment(
    payload: CommentCreate,
    current_user: dict = Depends(get_current_user),
):
    return await create_comment(payload, current_user)
