from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorCollection

from database.connection import get_database
from core.collections import CollectionName


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_sort(sort: list[tuple[str, int]] | tuple[str, int] | None) -> list[tuple[str, int]] | None:
    if sort is None:
        return None
    if isinstance(sort, tuple):
        return [sort]
    return sort


class MongoRepository:
    def __init__(self, collection_name: CollectionName | str):
        self.collection_name = str(collection_name)

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return get_database()[self.collection_name]

    async def list(
        self,
        query: dict[str, Any] | None = None,
        *,
        skip: int = 0,
        limit: int = 20,
        sort: list[tuple[str, int]] | tuple[str, int] | None = None,
        projection: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        cursor = self.collection.find(query or {}, projection or {"_id": 0}).skip(skip).limit(limit)
        if sort:
            cursor = cursor.sort(normalize_sort(sort))
        return await cursor.to_list(length=limit)

    async def get_by_id(self, entity_id: str, projection: dict[str, Any] | None = None) -> dict[str, Any] | None:
        return await self.collection.find_one({"id": entity_id}, projection or {"_id": 0})

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        now = utc_now_iso()
        document = {
            **data,
            "id": data.get("id") or str(uuid4()),
            "created_at": data.get("created_at") or now,
            "updated_at": data.get("updated_at") or now,
        }
        await self.collection.insert_one(document)
        return await self.get_by_id(document["id"]) or document

    async def update(self, entity_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        clean_updates = {key: value for key, value in updates.items() if value is not None}
        if not clean_updates:
            return await self.get_by_id(entity_id)

        clean_updates["updated_at"] = utc_now_iso()
        await self.collection.update_one({"id": entity_id}, {"$set": clean_updates})
        return await self.get_by_id(entity_id)

    async def delete(self, entity_id: str) -> bool:
        result = await self.collection.delete_one({"id": entity_id})
        return result.deleted_count > 0
