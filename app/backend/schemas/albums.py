from pydantic import BaseModel
from typing import List, Optional


class Album(BaseModel):
    id: str
    title: str
    artist_id: Optional[str] = None
    artist_name: Optional[str] = None
    year: Optional[int] = None
    featured: Optional[bool] = False
    motifs: List[str] = []
    color: Optional[str] = None
    universe_tagline: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = {"from_attributes": True}


class AlbumIn(BaseModel):
    title: str
    artist_id: Optional[str] = None
    artist_name: Optional[str] = None
    year: Optional[int] = None
    featured: Optional[bool] = False
    motifs: List[str] = []
    color: Optional[str] = None
    universe_tagline: Optional[str] = None


class AlbumUpdate(BaseModel):
    title: Optional[str] = None
    artist_id: Optional[str] = None
    artist_name: Optional[str] = None
    year: Optional[int] = None
    featured: Optional[bool] = None
    motifs: Optional[List[str]] = None
    color: Optional[str] = None
    universe_tagline: Optional[str] = None

    model_config = {"from_attributes": True}
