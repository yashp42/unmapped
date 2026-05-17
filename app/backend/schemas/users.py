from pydantic import BaseModel, Field


class UserPublic(BaseModel):
    id: str
    handle: str
    role: str = "user"
    display_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    depth_score: int = 0
    favorite_genres: list[str] = []
    favorite_artist_ids: list[str] = []
    lore_count: int = 0
    theory_count: int = 0
    contributions_count: int = 0
    created_at: str


class UserPrivate(UserPublic):
    email: str
    saved_album_ids: list[str] = []
    saved_track_ids: list[str] = []
    patron_album_id: str | None = None
    scenes: list[str] = []


class ProfileUpdate(BaseModel):
    display_name: str | None = Field(None, min_length=1, max_length=64)
    bio: str | None = Field(None, max_length=500)
    avatar_url: str | None = Field(None, max_length=500)
    favorite_genres: list[str] | None = None
    favorite_artist_ids: list[str] | None = None
    patron_album_id: str | None = None
    scenes: list[str] | None = None


class SaveToggleResponse(BaseModel):
    saved: bool
    saved_album_ids: list[str] = []
    saved_track_ids: list[str] = []


class UserCreate(BaseModel):
    email: str
    handle: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=8)
