import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings, UPLOAD_DIR
from .database.connection import close_database, connect_database
from .database.indexes import create_indexes
from .middleware.errors import register_exception_handlers
from .routes import (
    auth,
    albums,
    artists,
    tracks,
    vibes,
    lore,
    theories,
    contributors,
    collections,
    search,
    portal,
    users,
    connections,
    comments,
)
from .seed import seed_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("unmapped")


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_database()
    try:
        await create_indexes()
    except Exception as exc:
        logger.warning("create_indexes failed: %s", exc)
    try:
        await seed_database()
    except Exception as exc:
        logger.warning("seed_database failed: %s", exc)
    yield
    await close_database()


app = FastAPI(
    title="Unmapped Music Culture Platform",
    version="0.2.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(albums.router, prefix="/api/albums", tags=["albums"])
app.include_router(artists.router, prefix="/api/artists", tags=["artists"])
app.include_router(tracks.router, prefix="/api/tracks", tags=["tracks"])
app.include_router(vibes.router, prefix="/api/vibes", tags=["vibes"])
app.include_router(lore.router, prefix="/api/lore", tags=["lore"])
app.include_router(theories.router, prefix="/api/theories", tags=["theories"])
app.include_router(contributors.router, prefix="/api/contributors", tags=["contributors"])
app.include_router(collections.router, prefix="/api/collections", tags=["collections"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(portal.router, prefix="/api/explore/portal", tags=["explore"])
app.include_router(connections.router, prefix="/api/connections", tags=["connections"])
app.include_router(comments.router, prefix="/api/comments", tags=["comments"])

app.mount(
    "/api/media/avatars",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="avatar-media",
)


@app.get("/api/health")
async def health():
    from database.connection import get_database

    await get_database().command("ping")
    return {"status": "ok", "database": settings.DB_NAME}
