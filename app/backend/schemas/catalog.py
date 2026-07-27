"""Canonical contracts for provider-backed music works stored by Unmapped."""
from typing import Literal, Optional
from pydantic import BaseModel, Field

CatalogKind = Literal["artist", "album", "track"]

class CatalogEntity(BaseModel):
    id: str = Field(..., description="Stable Unmapped/provider identity")
    kind: CatalogKind
    provider: str
    provider_id: str
    title: str
    artist_name: Optional[str] = None
    album_title: Optional[str] = None
    artwork_url: Optional[str] = None
    external_url: Optional[str] = None
    release_year: Optional[int] = None
    metadata_confidence: float = Field(0.7, ge=0, le=1)
    last_synced_at: Optional[str] = None

class WorkContext(BaseModel):
    work: CatalogEntity | dict
    lore_count: int = 0
    theory_count: int = 0
    connection_count: int = 0
