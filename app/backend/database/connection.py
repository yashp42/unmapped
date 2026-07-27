import os

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from ..config import settings

MONGO_URL = os.getenv("MONGO_URL") or settings.MONGO_URL
DATABASE_NAME = os.getenv("DATABASE_NAME") or os.getenv("DB_NAME") or settings.DB_NAME

client = None
database = None


async def connect_database():
    global client, database

    client_options = {"serverSelectionTimeoutMS": 5000}
    if MONGO_URL.startswith("mongodb+srv://"):
        import certifi

        client_options.update(
            {
                "tls": True,
                "tlsCAFile": certifi.where(),
                "server_api": ServerApi("1"),
            }
        )

    client = AsyncIOMotorClient(MONGO_URL, **client_options)

    await client.admin.command("ping")

    database = client[DATABASE_NAME]

    print("MongoDB connected successfully")


async def close_database():
    global client

    if client:
        client.close()


def get_database():
    return database
