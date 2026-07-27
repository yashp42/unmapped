import asyncio
from fastapi import APIRouter, HTTPException, Query

from ..database.connection import get_database
from ..services.music_catalog_service import enrich_album, enrich_artist, enrich_track, explore_catalog, live_search

router = APIRouter()


@router.get("")
async def catalog():
    return await explore_catalog()


@router.get("/artists/{artist_id}")
async def artist_detail(artist_id: str):
    db = get_database()
    artist = await db.artists.find_one({"id": artist_id}, {"_id": 0})
    if not artist:
        raise HTTPException(404, "Artist not found")
    albums = await db.albums.find({"artist_id": artist_id}, {"_id": 0}).sort("year", -1).to_list(length=100)
    return {"artist": await enrich_artist(artist), "albums": [await enrich_album(album, artist["name"]) for album in albums]}


@router.get("/search")
async def catalog_search(q: str = Query(..., min_length=2)):
    """One search surface for albums, artists and tracks (no separate provider tab)."""
    return await live_search(q.strip())

@router.get("/works/{work_id}")
async def work_context(work_id: str):
    """A stable entry point for catalogue results, whether or not community content exists."""
    db = get_database()
    work = await db.catalog_entities.find_one({"id": work_id}, {"_id": 0})
    if not work:
        work = await db.tracks.find_one({"id": work_id}, {"_id": 0}) or await db.albums.find_one({"id": work_id}, {"_id": 0})
    if not work:
        raise HTTPException(404, "Work not found. Search for it again to refresh its catalogue record.")
    track_match = {"track_id": work_id}; album_match = {"album_id": work_id}
    lore_count, theory_count, connection_count = await asyncio.gather(
        db.lore.count_documents({"$or": [track_match, album_match]}),
        db.theories.count_documents({"$or": [track_match, album_match]}),
        db.connections.count_documents({"$or": [{"source": work_id}, {"target": work_id}]}),
    )
    return {"work": work, "lore_count": lore_count, "theory_count": theory_count, "connection_count": connection_count}
