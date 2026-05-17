from pydantic import BaseModel
from typing import Optional, List


class Artist(BaseModel):
    id: str
    name: str
    bio: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    aliases: List[str] = []

    model_config = {"from_attributes": True}


class ArtistIn(BaseModel):
    name: str
    bio: Optional[str] = None
    aliases: List[str] = []


class ArtistUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    aliases: Optional[List[str]] = None

    model_config = {"from_attributes": True}
