from pydantic import BaseModel
from typing import Optional


class Contributor(BaseModel):
    id: str
    name: str
    handle: str
    bio: Optional[str] = None
    depth_score: Optional[int] = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = {"from_attributes": True}


class ContributorIn(BaseModel):
    name: str
    handle: str
    bio: Optional[str] = None


class ContributorUpdate(BaseModel):
    name: Optional[str] = None
    handle: Optional[str] = None
    bio: Optional[str] = None

    model_config = {"from_attributes": True}
