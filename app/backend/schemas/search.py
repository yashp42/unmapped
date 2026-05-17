from pydantic import BaseModel
from typing import List


class SearchResults(BaseModel):
    tracks: List[dict] = []
    albums: List[dict] = []
    artists: List[dict] = []
    lore: List[dict] = []
