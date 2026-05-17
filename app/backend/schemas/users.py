from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    id: str
    email: EmailStr
    handle: str
    bio: str | None = None
    depth_score: int = 0
    created_at: str
    updated_at: str


class UserPublic(BaseModel):
    id: str
    handle: str
    bio: str | None = None
    depth_score: int = 0
    created_at: str


class UserCreate(BaseModel):
    email: EmailStr
    handle: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    bio: str | None = None
    depth_score: int | None = None
