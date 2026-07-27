from datetime import datetime, timezone
from typing import Any
from database.connection import get_database
from utils.catalog import catalog_id

async def persist_catalog_entities(items: list[dict[str, Any]], kind: str, provider: str = "itunes") -> None:
    """Persist only normalized metadata, never a provider's complete response."""
    collection = get_database().catalog_entities
    now = datetime.now(timezone.utc).isoformat()
    for item in items:
        provider_id = item.get("id", "").removeprefix(f"external-{kind}-")
        if not provider_id:
            continue
        document = {
            "id": item["id"], "kind": kind, "provider": provider, "provider_id": str(provider_id),
            "title": item.get("title") or item.get("name"), "artist_name": item.get("artist_name"),
            "album_title": item.get("album_title"), "artwork_url": item.get("artwork_url"),
            "external_url": item.get("external_url"), "release_year": int(item["year"]) if str(item.get("year", "")).isdigit() else None,
            "metadata_confidence": item.get("metadata_confidence", 0.9), "last_synced_at": now,
        }
        await collection.update_one({"id": item["id"]}, {"$set": document, "$setOnInsert": {"created_at": now}}, upsert=True)
