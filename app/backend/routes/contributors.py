from fastapi import APIRouter, HTTPException, status, Query, Depends, Response
from typing import List

from dependencies import require_admin, require_contributor
from repositories.contributors import contributors_repository
from schemas.contributors import Contributor, ContributorIn, ContributorUpdate

router = APIRouter()


@router.get("", response_model=List[Contributor])
async def list_contributors(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    return await contributors_repository.list(skip=skip, limit=limit, sort=("depth_score", -1))


@router.get("/{contributor_id}", response_model=Contributor)
async def get_contributor(contributor_id: str):
    contributor = await contributors_repository.get_by_id(contributor_id)
    if not contributor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contributor not found")
    return contributor


@router.post("", response_model=Contributor, status_code=201)
async def create_contributor(payload: ContributorIn, current_user: dict = Depends(require_contributor)):
    return await contributors_repository.create(payload.model_dump())


@router.put("/{contributor_id}", response_model=Contributor)
async def update_contributor(contributor_id: str, payload: ContributorUpdate, current_user: dict = Depends(require_admin)):
    contributor = await contributors_repository.get_by_id(contributor_id)
    if not contributor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contributor not found")

    return await contributors_repository.update(contributor_id, payload.model_dump())


@router.delete("/{contributor_id}", status_code=204)
async def delete_contributor(contributor_id: str, current_user: dict = Depends(require_admin)):
    deleted = await contributors_repository.delete(contributor_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contributor not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
