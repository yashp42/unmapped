from pydantic import BaseModel
from typing import Any


class StandardResponse(BaseModel):
    data: Any
    message: str = "success"
