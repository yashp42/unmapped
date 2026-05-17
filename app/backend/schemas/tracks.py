from pydantic import BaseModel
from typing import Optional


class Track(BaseModel):
    id: str
    title: str
    artist_id: Optional[str] = None
    artist_name: Optional[str] = None
    album_id: Optional[str] = None
    duration_seconds: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = {"from_attributes": True}


class TrackIn(BaseModel):
    title: str
    artist_id: Optional[str] = None
    artist_name: Optional[str] = None
    album_id: Optional[str] = None
    duration_seconds: Optional[int] = None


class TrackUpdate(BaseModel):
    title: Optional[str] = None
    artist_id: Optional[str] = None
    artist_name: Optional[str] = None
    album_id: Optional[str] = None
    duration_seconds: Optional[int] = None

    model_config = {"from_attributes": True}
