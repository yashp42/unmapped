from typing import Literal

from pydantic import BaseModel, Field


EntityType = Literal["artist", "album", "track", "lore", "theory", "user", "contributor"]


class RelationshipBase(BaseModel):
    source_type: EntityType
    source_id: str
    target_type: EntityType
    target_id: str
    type: str = Field(..., min_length=2, max_length=80)
    label: str | None = Field(None, max_length=120)
    description: str | None = Field(None, max_length=1000)
    weight: float = Field(0.5, ge=0, le=1)
    tags: list[str] = []


class RelationshipCreate(RelationshipBase):
    pass


class RelationshipUpdate(BaseModel):
    source_type: EntityType | None = None
    source_id: str | None = None
    target_type: EntityType | None = None
    target_id: str | None = None
    type: str | None = Field(None, min_length=2, max_length=80)
    label: str | None = Field(None, max_length=120)
    description: str | None = Field(None, max_length=1000)
    weight: float | None = Field(None, ge=0, le=1)
    tags: list[str] | None = None


class Relationship(RelationshipBase):
    id: str
    created_at: str | None = None
    updated_at: str | None = None

    model_config = {"from_attributes": True}
