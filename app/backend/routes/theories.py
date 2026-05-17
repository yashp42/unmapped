from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from ..database.connection import db

router = APIRouter()


@router.get("")
async def list_theories(skip: int = 0, limit: int = 20):
    return await db.theories.find({}, skip=skip, limit=limit).sort("supporters", -1).to_list(length=limit)


@router.get("/{theory_id}")
async def get_theory(theory_id: str):
    theory = await db.theories.find_one({"id": theory_id})
    if not theory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Theory not found")
    return theory


@router.post("")
async def create_theory(payload: dict):
    now = datetime.utcnow().isoformat()
    theory = {"id": str(uuid4()), "created_at": now, "updated_at": now, **payload}
    await db.theories.insert_one(theory)
    return theory
