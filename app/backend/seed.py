import logging
from datetime import datetime

from config import settings
from database.connection import get_database
from services.user_service import create_user, find_user_by_email
from seed_data import (
    ARTISTS,
    ALBUMS,
    TRACKS,
    LORE,
    THEORIES,
    CONTRIBUTORS,
    CONNECTIONS,
    SAMPLE_CHAINS,
    TRANSITIONS,
)

logger = logging.getLogger("unmapped.seed")


async def seed_collection(name: str, documents: list[dict]):
    count = await get_database()[name].count_documents({})
    if count > 0:
        return
    if documents:
        await get_database()[name].insert_many(documents)
        logger.info("Seeded %s with %d documents", name, len(documents))


async def seed_database() -> None:
    await seed_collection("artists", ARTISTS)
    await seed_collection("albums", ALBUMS)
    await seed_collection("tracks", TRACKS)
    await seed_collection("lore", LORE)
    await seed_collection("theories", THEORIES)
    await seed_collection("contributors", CONTRIBUTORS)
    await seed_collection("connections", CONNECTIONS)
    await seed_collection("sample_chains", SAMPLE_CHAINS)
    await seed_collection("transitions", TRANSITIONS)

    admin_email = settings.ADMIN_EMAIL.lower().strip()
    existing_admin = await find_user_by_email(admin_email)
    if not existing_admin:
        await create_user({
            "id": "admin",
            "email": admin_email,
            "handle": settings.ADMIN_HANDLE,
            "password": settings.ADMIN_PASSWORD,
            "role": "admin",
            "bio": "Platform administrator.",
            "depth_score": 9999,
        })
        logger.info("Created default admin user %s", admin_email)
    elif existing_admin.get("role") != "admin":
        db = get_database()
        users_collection = db["users"]
        await users_collection.update_one({"email": admin_email}, {"$set": {"role": "admin"}})
        logger.info("Promoted default admin user %s", admin_email)
