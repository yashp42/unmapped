from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from dependencies import get_current_user, require_admin
from database.connection import get_database
from services.audit_service import audit

router = APIRouter()
class ReportIn(BaseModel):
    target_type: str
    target_id: str
    reason: str = Field(..., min_length=5, max_length=600)

@router.post("", status_code=201)
async def create_report(payload: ReportIn, user: dict = Depends(get_current_user)):
    if payload.target_type not in {"lore", "theory", "comment", "connection"}: raise HTTPException(400, "Unsupported report target")
    await get_database().reports.update_one({"target_type": payload.target_type, "target_id": payload.target_id, "reporter_id": user["id"]}, {"$setOnInsert": {"id": str(uuid4()), **payload.model_dump(), "reporter_id": user["id"], "status": "open", "created_at": datetime.now(timezone.utc).isoformat()}}, upsert=True)
    return {"status": "received"}

@router.get("")
async def list_reports(user: dict = Depends(require_admin)):
    return await get_database().reports.find({"status": "open"}, {"_id": 0}).sort("created_at", -1).to_list(length=100)

@router.post("/{report_id}/resolve")
async def resolve_report(report_id: str, admin: dict = Depends(require_admin)):
    db = get_database(); report = await db.reports.find_one({"id": report_id})
    if not report: raise HTTPException(404, "Report not found")
    await db.reports.update_one({"id": report_id}, {"$set": {"status": "resolved", "reviewed_by": admin["id"], "reviewed_at": datetime.now(timezone.utc).isoformat()}})
    await audit(admin["id"], "report.resolved", report["target_type"], report["target_id"], {"report_id": report_id})
    return {"status": "resolved"}
