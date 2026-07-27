"""Small database-backed posting guard; replace with Redis when traffic warrants it."""
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from database.connection import get_database

MAX_POSTS_PER_HOUR = 10

async def allow_submission(user_id: str, kind: str) -> None:
    db = get_database(); now = datetime.now(timezone.utc); since = now - timedelta(hours=1)
    count = await db.submission_events.count_documents({"user_id": user_id, "kind": kind, "created_at": {"$gte": since.isoformat()}})
    if count >= MAX_POSTS_PER_HOUR:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "You have reached the hourly publishing limit. Please come back shortly.")
    await db.submission_events.insert_one({"user_id": user_id, "kind": kind, "created_at": now.isoformat(), "expires_at": now + timedelta(days=2)})
