from fastapi import APIRouter, Query
from database.connection import get_database
from ..schemas.search import SearchResults

router = APIRouter()


async def lookup(collection_name: str, term: str, fields: list[str]) -> list[dict]:
    query = {"$or": [{field: {"$regex": term, "$options": "i"}} for field in fields]}
    return await get_database()[collection_name].find(query, {"_id": 0}).limit(20).to_list(length=20)


@router.get("", response_model=SearchResults)
async def search(q: str = Query(..., min_length=1)):
    term = q.strip()
    return SearchResults(
        tracks=await lookup("tracks", term, ["title", "artist_name"]),
        albums=await lookup("albums", term, ["title", "artist_name"]),
        artists=await lookup("artists", term, ["name"]),
        lore=await lookup("lore", term, ["title", "excerpt", "body"]),
    )
