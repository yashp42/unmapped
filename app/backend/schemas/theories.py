from pydantic import BaseModel
from typing import Optional, List


class Theory(BaseModel):
    id: str
    title: str
    stance: Optional[str] = None
    abstract: Optional[str] = None
    supporters: Optional[int] = 0
    challengers: Optional[int] = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    citations: List[str] = []

    model_config = {"from_attributes": True}


class TheoryCreate(BaseModel):
    title: str
    stance: Optional[str] = None
    abstract: Optional[str] = None
    album_id: Optional[str] = None
    track_id: Optional[str] = None
    citations: List[str] = []


class TheoryUpdate(BaseModel):
    title: Optional[str] = None
    stance: Optional[str] = None
    abstract: Optional[str] = None
    album_id: Optional[str] = None
    track_id: Optional[str] = None
    supporters: Optional[int] = None
    challengers: Optional[int] = None
    citations: Optional[List[str]] = None
