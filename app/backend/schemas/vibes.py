from pydantic import BaseModel
from typing import Optional


class Vibe(BaseModel):
    id: str
    name: str
    felt_state: Optional[str] = None
    color: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = {"from_attributes": True}
