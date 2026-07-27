from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from ..dependencies import require_admin
from ..repositories.albums import albums_repository
from ..repositories.artists import artists_repository
from ..repositories.lore import lore_repository
from ..repositories.relationships import relationships_repository
from ..repositories.theories import theories_repository
from ..repositories.tracks import tracks_repository
from ..schemas.albums import Album, AlbumIn, AlbumUpdate
from ..schemas.artists import Artist, ArtistIn, ArtistUpdate
from ..schemas.lore import LoreCreate, LoreOut
from ..schemas.relationships import Relationship, RelationshipCreate, RelationshipUpdate
from ..schemas.theories import Theory, TheoryCreate, TheoryUpdate
from ..schemas.tracks import Track, TrackIn, TrackUpdate
from ..services.lore_service import create_lore_entry

router = APIRouter(dependencies=[Depends(require_admin)])


def _updates(payload: Any) -> dict[str, Any]:
    return {key: value for key, value in payload.model_dump().items() if value is not None}


async def _delete_or_404(repository, entity_id: str, label: str) -> Response:
    if not await repository.delete(entity_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{label} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def _update_or_404(repository, entity_id: str, payload: Any, label: str) -> dict:
    existing = await repository.get_by_id(entity_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{label} not found")
    return await repository.update(entity_id, _updates(payload)) or existing


@router.get("/artists", response_model=list[Artist])
async def list_artists(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    return await artists_repository.list(skip=skip, limit=limit, sort=("name", 1))


@router.post("/artists", response_model=Artist, status_code=201)
async def create_artist(payload: ArtistIn):
    return await artists_repository.create(payload.model_dump())


@router.put("/artists/{artist_id}", response_model=Artist)
async def update_artist(artist_id: str, payload: ArtistUpdate):
    return await _update_or_404(artists_repository, artist_id, payload, "Artist")


@router.delete("/artists/{artist_id}", status_code=204)
async def delete_artist(artist_id: str):
    return await _delete_or_404(artists_repository, artist_id, "Artist")


@router.get("/albums", response_model=list[Album])
async def list_albums(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    return await albums_repository.list(skip=skip, limit=limit, sort=("year", -1))


@router.post("/albums", response_model=Album, status_code=201)
async def create_album(payload: AlbumIn):
    return await albums_repository.create(payload.model_dump())


@router.put("/albums/{album_id}", response_model=Album)
async def update_album(album_id: str, payload: AlbumUpdate):
    return await _update_or_404(albums_repository, album_id, payload, "Album")


@router.delete("/albums/{album_id}", status_code=204)
async def delete_album(album_id: str):
    return await _delete_or_404(albums_repository, album_id, "Album")


@router.get("/tracks", response_model=list[Track])
async def list_tracks(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    return await tracks_repository.list(skip=skip, limit=limit, sort=("title", 1))


@router.post("/tracks", response_model=Track, status_code=201)
async def create_track(payload: TrackIn):
    return await tracks_repository.create(payload.model_dump())


@router.put("/tracks/{track_id}", response_model=Track)
async def update_track(track_id: str, payload: TrackUpdate):
    return await _update_or_404(tracks_repository, track_id, payload, "Track")


@router.delete("/tracks/{track_id}", status_code=204)
async def delete_track(track_id: str):
    return await _delete_or_404(tracks_repository, track_id, "Track")


@router.get("/lore", response_model=list[LoreOut])
async def list_lore(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    return await lore_repository.list(skip=skip, limit=limit, sort=("created_at", -1))


@router.post("/lore", response_model=LoreOut, status_code=201)
async def create_lore(payload: LoreCreate, current_user: dict = Depends(require_admin)):
    return await create_lore_entry(payload, current_user)


@router.delete("/lore/{lore_id}", status_code=204)
async def delete_lore(lore_id: str):
    return await _delete_or_404(lore_repository, lore_id, "Lore entry")


@router.get("/theories", response_model=list[Theory])
async def list_theories(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    return await theories_repository.list(skip=skip, limit=limit, sort=("supporters", -1))


@router.post("/theories", response_model=Theory, status_code=201)
async def create_theory(payload: TheoryCreate):
    theory = {
        **payload.model_dump(),
        "supporters": 0,
        "challengers": 0,
    }
    return await theories_repository.create(theory)


@router.put("/theories/{theory_id}", response_model=Theory)
async def update_theory(theory_id: str, payload: TheoryUpdate):
    return await _update_or_404(theories_repository, theory_id, payload, "Theory")


@router.delete("/theories/{theory_id}", status_code=204)
async def delete_theory(theory_id: str):
    return await _delete_or_404(theories_repository, theory_id, "Theory")


@router.get("/relationships", response_model=list[Relationship])
async def list_relationships(skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    return await relationships_repository.list(skip=skip, limit=limit, sort=("created_at", -1))


@router.post("/relationships", response_model=Relationship, status_code=201)
async def create_relationship(payload: RelationshipCreate):
    return await relationships_repository.create(payload.model_dump())


@router.put("/relationships/{relationship_id}", response_model=Relationship)
async def update_relationship(relationship_id: str, payload: RelationshipUpdate):
    return await _update_or_404(relationships_repository, relationship_id, payload, "Relationship")


@router.delete("/relationships/{relationship_id}", status_code=204)
async def delete_relationship(relationship_id: str):
    return await _delete_or_404(relationships_repository, relationship_id, "Relationship")
