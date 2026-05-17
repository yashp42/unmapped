from fastapi import APIRouter

from ..database.connection import db

router = APIRouter()


@router.get("")
async def portal():
    rabbit_holes = (
        await db.lore.find({}, {"_id": 0}).sort("created_at", -1).limit(5).to_list(length=5)
    )
    vibes = await db.vibes.find({}, {"_id": 0}).sort("name", 1).limit(8).to_list(length=8)
    featured_album = await db.albums.find_one({"featured": True}, {"_id": 0})
    theories = await db.theories.find({}, {"_id": 0}).sort("supporters", -1).limit(3).to_list(length=3)
    contributors = (
        await db.contributors.find({}, {"_id": 0}).sort("depth_score", -1).limit(4).to_list(length=4)
    )
    return {
        "rabbit_holes": rabbit_holes,
        "vibes": vibes,
        "featured_album": featured_album,
        "theories": theories,
        "contributors": contributors,
    }
