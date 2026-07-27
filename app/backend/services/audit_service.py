from datetime import datetime, timezone
from typing import Any
from ..database.connection import get_database

async def audit(actor_id: str | None, action: str, target_type: str, target_id: str, metadata: dict[str, Any] | None = None) -> None:
    await get_database().audit_events.insert_one({"actor_id": actor_id, "action": action, "target_type": target_type, "target_id": target_id, "metadata": metadata or {}, "created_at": datetime.now(timezone.utc).isoformat()})
