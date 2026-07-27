from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status, Query
from dependencies import get_current_user, get_optional_user
from database.connection import get_database
from typing import List
from schemas.theories import Theory, TheoryCreate
from services.submission_guard import allow_submission
from services.audit_service import audit
from services.revision_service import snapshot

router = APIRouter()


@router.get("", response_model=List[Theory])
async def list_theories(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    cursor = get_database().theories.find({"$or": [{"status": {"$exists": False}}, {"status": "published"}]}, {"_id": 0}).sort("supporters", -1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


@router.get("/{theory_id}", response_model=Theory)
async def get_theory(theory_id: str, current_user: dict | None = Depends(get_optional_user)):
    theory = await get_database().theories.find_one({"id": theory_id}, {"_id": 0})
    if not theory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theory not found")
    if theory.get("status") not in (None, "published") and not (current_user and (current_user.get("id") == theory.get("user_id") or current_user.get("role") == "admin")):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theory not found")
    comment_count = await get_database().comments.count_documents(
        {"target_type": "theory", "target_id": theory_id}
    )
    theory["replies"] = max(theory.get("replies", 0), comment_count)
    theory["comments"] = theory["replies"]
    return theory


@router.post("", response_model=Theory, status_code=201)
async def create_theory(payload: TheoryCreate, current_user: dict = Depends(get_current_user)):
    await allow_submission(current_user["id"], "theory")
    now = datetime.utcnow().isoformat()
    theory = payload.model_dump()
    theory.update({"id": str(uuid4()), "author": current_user["handle"], "user_id": current_user["id"], "supporters": 0, "challengers": 0, "status": "pending", "created_at": now, "updated_at": now})
    await get_database().theories.insert_one(theory)
    await snapshot("theory", theory, current_user["id"], "submitted")
    await audit(current_user["id"], "theory.submitted", "theory", theory["id"], {"track_id": theory.get("track_id"), "album_id": theory.get("album_id")})
    return theory
