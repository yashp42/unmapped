from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from ..database.connection import db

router = APIRouter()


@router.get("")
async def list_contributors(skip: int = 0, limit: int = 20):
    return await db.contributors.find({}, skip=skip, limit=limit).sort("depth_score", -1).to_list(length=limit)


@router.get("/{contributor_id}")
async def get_contributor(contributor_id: str):
    contributor = await db.contributors.find_one({"id": contributor_id})
    if not contributor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contributor not found")
    return contributor


@router.post("")
async def create_contributor(payload: dict):
    now = datetime.utcnow().isoformat()
    contributor = {"id": str(uuid4()), "created_at": now, "updated_at": now, **payload}
    await db.contributors.insert_one(contributor)
    return contributor
