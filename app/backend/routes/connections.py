from typing import Optional

from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, Query, Depends, HTTPException

from ..services.connection_service import build_connection_graph, find_connection_path
from ..dependencies import require_admin, require_contributor
from ..schemas.relationships import RelationshipCreate
from ..database.connection import get_database

router = APIRouter()

@router.get("/path")
async def connection_path(from_id: str = Query(...), to_id: str = Query(...)):
    return await find_connection_path(from_id, to_id)

@router.post("/submissions", status_code=201)
async def submit_connection(payload: RelationshipCreate, user: dict = Depends(require_contributor)):
    if payload.source_type != "track" or payload.target_type != "track":
        raise HTTPException(400, "Connection submissions must link two tracks")
    doc = {**payload.model_dump(), "id": str(uuid4()), "author_id": user["id"], "status": "pending", "created_at": datetime.now(timezone.utc).isoformat()}
    await get_database().connection_submissions.insert_one(doc)
    doc.pop("_id", None)
    return doc

@router.get("/submissions")
async def review_queue(user: dict = Depends(require_admin)):
    return await get_database().connection_submissions.find({"status": "pending"}, {"_id": 0}).sort("created_at", -1).to_list(length=100)

@router.post("/submissions/{submission_id}/approve")
async def approve_submission(submission_id: str, user: dict = Depends(require_admin)):
    db = get_database(); item = await db.connection_submissions.find_one({"id": submission_id})
    if not item or item.get("status") != "pending": raise HTTPException(404, "Submission not found")
    await db.connections.insert_one({"source": item["source_id"], "target": item["target_id"], "type": item["type"], "weight": item["weight"], "label": item.get("label"), "description": item.get("description"), "created_at": datetime.now(timezone.utc).isoformat()})
    await db.connection_submissions.update_one({"id": submission_id}, {"$set": {"status": "approved", "reviewed_at": datetime.now(timezone.utc).isoformat(), "reviewed_by": user["id"]}})
    return {"status": "approved"}


@router.get("/graph")
async def connection_graph(track_id: Optional[str] = Query(None), types: Optional[str] = Query(None)):
    return await build_connection_graph(track_id, types.split(",") if types else None)
