from pydantic import BaseModel, Field
from typing import List


class CollectionCreate(BaseModel):
    title: str = Field(..., min_length=1)
    note: str | None = None
    item_ids: List[str] = Field(default_factory=list)


class CollectionOut(BaseModel):
    id: str
    owner_id: str
    title: str
    note: str | None = None
    item_ids: List[str]
    created_at: str
    updated_at: str
