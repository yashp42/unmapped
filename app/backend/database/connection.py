import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from ..config import settings

logger = logging.getLogger("unmapped.db")

client = AsyncIOMotorClient(
    settings.MONGO_URL,
    serverSelectionTimeoutMS=10_000,
    connectTimeoutMS=10_000,
)
db: AsyncIOMotorDatabase = client[settings.DB_NAME]


async def connect_database() -> None:
    await client.admin.command("ping")
    logger.info("Connected to MongoDB database=%s", settings.DB_NAME)


async def close_database() -> None:
    client.close()
    logger.info("MongoDB connection closed")
