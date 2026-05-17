from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status, Query, Depends, Response
from typing import List
from database.connection import get_database
from ..schemas.contributors import Contributor, ContributorIn, ContributorUpdate
from ..dependencies import get_current_user

router = APIRouter()


@router.get("", response_model=List[Contributor])
async def list_contributors(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    cursor = get_database().contributors.find({}, {"_id": 0}).sort("depth_score", -1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


@router.get("/{contributor_id}", response_model=Contributor)
async def get_contributor(contributor_id: str):
    contributor = await get_database().contributors.find_one({"id": contributor_id}, {"_id": 0})
    if not contributor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contributor not found")
    return contributor


@router.post("", response_model=Contributor, status_code=201)
async def create_contributor(payload: ContributorIn, current_user: dict = Depends(get_current_user)):
    now = datetime.utcnow().isoformat()
    contributor = payload.model_dump()
    contributor.update({"id": str(uuid4()), "created_at": now, "updated_at": now})
    await get_database().contributors.insert_one(contributor)
    return await get_database().contributors.find_one({"id": contributor["id"]}, {"_id": 0})


@router.put("/{contributor_id}", response_model=Contributor)
async def update_contributor(contributor_id: str, payload: ContributorUpdate, current_user: dict = Depends(get_current_user)):
    contributor = await get_database().contributors.find_one({"id": contributor_id}, {"_id": 0})
    if not contributor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contributor not found")

    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        return contributor

    update_data["updated_at"] = datetime.utcnow().isoformat()
    await get_database().contributors.update_one({"id": contributor_id}, {"$set": update_data})
    return await get_database().contributors.find_one({"id": contributor_id}, {"_id": 0})


@router.delete("/{contributor_id}", status_code=204)
async def delete_contributor(contributor_id: str, current_user: dict = Depends(get_current_user)):
    res = await get_database().contributors.delete_one({"id": contributor_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contributor not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
