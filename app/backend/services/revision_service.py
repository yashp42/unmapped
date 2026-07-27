from datetime import datetime, timezone
from ..database.connection import get_database

async def snapshot(content_type: str, document: dict, actor_id: str | None, reason: str) -> str:
    revision_id = f"{document['id']}:{datetime.now(timezone.utc).timestamp():.6f}"
    await get_database().content_revisions.insert_one({"id": revision_id, "content_type": content_type, "content_id": document["id"], "snapshot": {k: v for k, v in document.items() if k != "_id"}, "actor_id": actor_id, "reason": reason, "created_at": datetime.now(timezone.utc).isoformat()})
    return revision_id
