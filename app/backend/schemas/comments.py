from typing import Literal

from pydantic import BaseModel, Field


TargetType = Literal["lore", "theory"]


class CommentCreate(BaseModel):
    target_type: TargetType
    target_id: str = Field(..., min_length=1, max_length=128)
    body: str = Field(..., min_length=1, max_length=2000)


class CommentOut(BaseModel):
    id: str
    target_type: TargetType
    target_id: str
    user_id: str
    author_handle: str
    author_display_name: str | None = None
    author_avatar_url: str | None = None
    body: str
    created_at: str
