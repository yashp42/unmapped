from pydantic import BaseModel, Field, model_validator
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
    target_source: Optional[str] = None
    target_label: Optional[str] = Field(None, max_length=300)

    @model_validator(mode="after")
    def requires_work(self):
        if not self.album_id and not self.track_id:
            raise ValueError("Attach this theory to an album or track")
        return self


class TheoryUpdate(BaseModel):
    title: Optional[str] = None
    stance: Optional[str] = None
    abstract: Optional[str] = None
    album_id: Optional[str] = None
    track_id: Optional[str] = None
    supporters: Optional[int] = None
    challengers: Optional[int] = None
    citations: Optional[List[str]] = None
