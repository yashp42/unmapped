from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from dependencies import require_admin
from database.connection import get_database
from services.audit_service import audit
from services.revision_service import snapshot

router = APIRouter(dependencies=[Depends(require_admin)])
COLLECTIONS = {"lore": "lore", "theory": "theories"}

class Decision(BaseModel):
    status: str = Field(..., pattern="^(published|needs_revision|rejected|removed)$")
    note: str | None = Field(None, max_length=1000)

@router.get("/queue")
async def queue():
    db = get_database()
    lore = await db.lore.find({"status": "pending"}, {"_id": 0, "body": 0}).sort("created_at", 1).to_list(length=100)
    theories = await db.theories.find({"status": "pending"}, {"_id": 0}).sort("created_at", 1).to_list(length=100)
    return {"lore": lore, "theories": theories}

@router.post("/{content_type}/{content_id}")
async def decide(content_type: str, content_id: str, payload: Decision, admin: dict = Depends(require_admin)):
    collection_name = COLLECTIONS.get(content_type)
    if not collection_name: raise HTTPException(404, "Unsupported content type")
    db = get_database(); existing = await db[collection_name].find_one({"id": content_id})
    if not existing: raise HTTPException(404, "Content not found")
    now = datetime.now(timezone.utc).isoformat()
    await snapshot(content_type, existing, admin["id"], f"before_moderation.{payload.status}")
    await db[collection_name].update_one({"id": content_id}, {"$set": {"status": payload.status, "moderation_note": payload.note, "reviewed_by": admin["id"], "reviewed_at": now, "updated_at": now}})
    await audit(admin["id"], f"moderation.{payload.status}", content_type, content_id, {"note": payload.note})
    return {"status": payload.status}

@router.get("/{content_type}/{content_id}/history")
async def history(content_type: str, content_id: str):
    if content_type not in COLLECTIONS: raise HTTPException(404, "Unsupported content type")
    return await get_database().content_revisions.find({"content_type": content_type, "content_id": content_id}, {"_id": 0}).sort("created_at", -1).to_list(length=100)

@router.post("/{content_type}/{content_id}/restore/{revision_id}")
async def restore(content_type: str, content_id: str, revision_id: str, admin: dict = Depends(require_admin)):
    collection_name = COLLECTIONS.get(content_type)
    if not collection_name: raise HTTPException(404, "Unsupported content type")
    db = get_database(); revision = await db.content_revisions.find_one({"id": revision_id, "content_type": content_type, "content_id": content_id})
    current = await db[collection_name].find_one({"id": content_id})
    if not revision or not current: raise HTTPException(404, "Revision not found")
    await snapshot(content_type, current, admin["id"], f"before_restore.{revision_id}")
    restored = revision["snapshot"]; restored["updated_at"] = datetime.now(timezone.utc).isoformat()
    await db[collection_name].replace_one({"id": content_id}, restored)
    await audit(admin["id"], "content.restored", content_type, content_id, {"revision_id": revision_id})
    return {"status": "restored"}
