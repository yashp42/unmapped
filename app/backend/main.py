from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes import auth, albums, artists, tracks, vibes, lore, theories, contributors, collections, search, portal, users
from .seed import seed_database

app = FastAPI(title="Unmapped Music Culture Platform", version="0.1.0")

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


@app.on_event("startup")
async def startup_event():
    await seed_database()
