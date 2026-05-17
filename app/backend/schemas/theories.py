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
