from fastapi import APIRouter

from database.connection import get_database

router = APIRouter()


@router.get("")
async def portal():
    rabbit_holes = (
        await get_database().lore.find({}, {"_id": 0}).sort("created_at", -1).limit(5).to_list(length=5)
    )
    featured_album = await get_database().albums.find_one({"featured": True}, {"_id": 0})
    theories = await get_database().theories.find({}, {"_id": 0}).sort("supporters", -1).limit(3).to_list(length=3)
    contributors = (
        await get_database().contributors.find({}, {"_id": 0}).sort("depth_score", -1).limit(4).to_list(length=4)
    )
    return {
        "rabbit_holes": rabbit_holes,
        "featured_album": featured_album,
        "theories": theories,
        "contributors": contributors,
    }
