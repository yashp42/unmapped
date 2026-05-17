from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class LoreCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    body: str = Field(..., min_length=20, max_length=20000)
    excerpt: Optional[str] = Field(None, max_length=500)
    album_id: Optional[str] = None
    track_id: Optional[str] = None
    depth: Literal["casual", "community", "deep"] = "community"


class LoreOut(BaseModel):
    id: str
    title: str
    excerpt: Optional[str] = None
    body: Optional[str] = None
    author: Optional[str] = None
    user_id: Optional[str] = None
    track_id: Optional[str] = None
    album_id: Optional[str] = None
    depth: Optional[str] = None
    votes: int = 0
    comments: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = {"extra": "allow"}



# Backward-compatible alias for list routes
LoreEntry = LoreOut
