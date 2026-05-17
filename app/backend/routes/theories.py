from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status, Query
from ..dependencies import get_current_user
from typing import List
from ..database.connection import db
from ..schemas.theories import Theory

router = APIRouter()


@router.get("", response_model=List[Theory])
async def list_theories(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    cursor = db.theories.find({}, {"_id": 0}).sort("supporters", -1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


@router.get("/{theory_id}", response_model=Theory)
async def get_theory(theory_id: str):
    theory = await db.theories.find_one({"id": theory_id}, {"_id": 0})
    if not theory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theory not found")
    comment_count = await db.comments.count_documents(
        {"target_type": "theory", "target_id": theory_id}
    )
    theory["replies"] = max(theory.get("replies", 0), comment_count)
    theory["comments"] = theory["replies"]
    return theory


@router.post("", response_model=Theory, status_code=201)
async def create_theory(payload: Theory, current_user: dict = Depends(get_current_user)):
    now = datetime.utcnow().isoformat()
    theory = payload.model_dump()
    theory.update({"id": str(uuid4()), "created_at": now, "updated_at": now})
    await db.theories.insert_one(theory)
    return theory
