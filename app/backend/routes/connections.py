from typing import Optional

from fastapi import APIRouter, Query

from ..services.connection_service import build_connection_graph

router = APIRouter()


@router.get("/graph")
async def connection_graph(track_id: Optional[str] = Query(None)):
    return await build_connection_graph(track_id)
