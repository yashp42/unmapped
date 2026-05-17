from datetime import datetime
from typing import Optional

from ..database.connection import db
from ..utils.security import hash_password, verify_password


async def find_user_by_email(email: str) -> Optional[dict]:
    return await db.users.find_one({"email": email})


async def find_user_by_handle(handle: str) -> Optional[dict]:
    return await db.users.find_one({"handle": handle})


async def find_user_by_id(user_id: str) -> Optional[dict]:
    return await db.users.find_one({"id": user_id})


async def create_user(data: dict) -> dict:
    now = datetime.utcnow().isoformat()
    payload = {
        "id": data["id"],
        "email": data["email"],
        "handle": data["handle"],
        "bio": data.get("bio", ""),
        "depth_score": data.get("depth_score", 0),
        "created_at": now,
        "updated_at": now,
        "password_hash": hash_password(data["password"]),
    }
    await db.users.insert_one(payload)
    payload.pop("password_hash")
    return payload


async def authenticate_user(email: str, password: str) -> Optional[dict]:
    user = await find_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.get("password_hash", "")):
        return None
    user.pop("password_hash", None)
    return user


async def update_user(user_id: str, updates: dict) -> Optional[dict]:
    updates["updated_at"] = datetime.utcnow().isoformat()
    await db.users.update_one({"id": user_id}, {"$set": updates})
    return await find_user_by_id(user_id)


async def list_users(skip: int = 0, limit: int = 20) -> list[dict]:
    cursor = db.users.find({}, skip=skip, limit=limit).sort("created_at", -1)
    return await cursor.to_list(length=limit)
