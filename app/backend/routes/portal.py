from fastapi import APIRouter
from ..database.connection import db

router = APIRouter()


@router.get("")
async def portal():
    rabbit_holes = await db.lore.find({}, limit=5).sort("created_at", -1).to_list(length=5)
    vibes = await db.vibes.find({}, limit=8).sort("name", 1).to_list(length=8)
    featured_album = await db.albums.find_one({"featured": True})
    theories = await db.theories.find({}, limit=3).sort("supporters", -1).to_list(length=3)
    contributors = await db.contributors.find({}, limit=4).sort("depth_score", -1).to_list(length=4)
    return {
        "rabbit_holes": rabbit_holes,
        "vibes": vibes,
        "featured_album": featured_album,
        "theories": theories,
        "contributors": contributors,
    }
