from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import certifi
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.modules.setdefault("backend.database.connection", sys.modules[__name__])
sys.modules.setdefault("database.connection", sys.modules[__name__])

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME") or os.getenv("DB_NAME", "unmapped")

client = None
database = None


async def connect_database():
    global client, database

    client = AsyncIOMotorClient(
        MONGO_URL,
        tls=True,
        tlsCAFile=certifi.where(),
        server_api=ServerApi("1")
    )

    await client.admin.command("ping")

    database = client[DATABASE_NAME]

    print("MongoDB connected successfully")


async def close_database():
    global client

    if client:
        client.close()


def get_database():
    return database
