import certifi
import os
import sys
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from backend.config import settings

load_dotenv()

sys.modules.setdefault("backend.database.connection", sys.modules[__name__])
sys.modules.setdefault("database.connection", sys.modules[__name__])

MONGO_URL = os.getenv("MONGO_URL", settings.MONGO_URL)
DATABASE_NAME = os.getenv("DATABASE_NAME") or os.getenv("DB_NAME", settings.DB_NAME)

client = None
database = None


async def connect_database():
    global client, database

    client_options = {"serverSelectionTimeoutMS": 5000}
    if MONGO_URL.startswith("mongodb+srv://"):
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
