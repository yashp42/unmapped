from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

import os
import logging
import uuid
import bcrypt
import jwt

from datetime import datetime, timezone, timedelta
from typing import List, Optional

from fastapi import FastAPI, APIRouter, HTTPException, Request, Response, Depends
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field

from seed_data import (
    ARTISTS,
    ALBUMS,
    TRACKS,
    VIBES,
    LORE,
    THEORIES,
    CONNECTIONS,
    SAMPLE_CHAINS,
    TRANSITIONS,
    CONTRIBUTORS,
)

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------

mongo_url = os.environ["MONGO_URL"]

client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGO = "HS256"

app = FastAPI(title="Unmapped — Music Culture Platform")
api = APIRouter(prefix="/api")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("unmapped")

# -----------------------------------------------------------------------------
# Auth Helpers
# -----------------------------------------------------------------------------

def hash_pw(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_pw(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def make_access(user_id: str, email: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(hours=12)
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def make_refresh(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def set_auth_cookies(response: Response, access: str, refresh: str):
    response.set_cookie(
        "access_token",
        access,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=12 * 3600,
        path="/"
    )

    response.set_cookie(
        "refresh_token",
        refresh,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=7 * 24 * 3600,
        path="/"
    )


async def current_user(request: Request) -> dict:

    token = request.cookies.get("access_token")

    if not token:
        auth = request.headers.get("Authorization", "")

        if auth.startswith("Bearer "):
            token = auth[7:]

    if not token:
        raise HTTPException(401, "not authenticated")

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGO]
        )

        if payload.get("type") != "access":
            raise HTTPException(401, "invalid token")

        user = await db.users.find_one(
            {"id": payload["sub"]},
            {"_id": 0, "password_hash": 0}
        )

        if not user:
            raise HTTPException(401, "user not found")

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(401, "invalid token")


# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    handle: str = Field(min_length=2, max_length=30)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


# -----------------------------------------------------------------------------
# Seed
# -----------------------------------------------------------------------------

async def seed():

    admin_email = os.environ["ADMIN_EMAIL"]
    admin_pw = os.environ["ADMIN_PASSWORD"]

    if not await db.users.find_one({"email": admin_email}):

        await db.users.insert_one({
            "id": str(uuid.uuid4()),
            "email": admin_email,
            "password_hash": hash_pw(admin_pw),
            "handle": "admin",
            "name": "admin",
            "role": "admin",
            "bio": "keeper of the archive",
            "depth_score": 100,
            "created_at": datetime.now(timezone.utc).isoformat()
        })

    if await db.artists.count_documents({}) == 0:
        await db.artists.insert_many([{**a} for a in ARTISTS])

    if await db.albums.count_documents({}) == 0:
        await db.albums.insert_many([{**a} for a in ALBUMS])

    if await db.tracks.count_documents({}) == 0:
        await db.tracks.insert_many([{**t} for t in TRACKS])

    if await db.vibes.count_documents({}) == 0:
        await db.vibes.insert_many([{**v} for v in VIBES])

    if await db.lore.count_documents({}) == 0:
        await db.lore.insert_many([{**l} for l in LORE])

    if await db.theories.count_documents({}) == 0:
        await db.theories.insert_many([{**t} for t in THEORIES])

    if await db.connections.count_documents({}) == 0:
        await db.connections.insert_many([{**c} for c in CONNECTIONS])

    if await db.samples.count_documents({}) == 0:
        await db.samples.insert_many([{**s} for s in SAMPLE_CHAINS])

    if await db.transitions.count_documents({}) == 0:
        await db.transitions.insert_many([{**t} for t in TRANSITIONS])

    if await db.contributors.count_documents({}) == 0:
        await db.contributors.insert_many([{**c} for c in CONTRIBUTORS])

    await db.users.create_index("email", unique=True)

    logger.info("seed complete")


@app.on_event("startup")
async def on_startup():
    await seed()


@app.on_event("shutdown")
async def on_shutdown():
    client.close()

# -----------------------------------------------------------------------------
# Auth Routes
# -----------------------------------------------------------------------------

@api.post("/auth/register")
async def register(payload: RegisterIn, response: Response):

    email = payload.email.lower()

    if await db.users.find_one({"email": email}):
        raise HTTPException(400, "email already registered")

    if await db.users.find_one({"handle": payload.handle}):
        raise HTTPException(400, "handle taken")

    uid = str(uuid.uuid4())

    doc = {
        "id": uid,
        "email": email,
        "password_hash": hash_pw(payload.password),
        "handle": payload.handle,
        "name": payload.handle,
        "role": "curator",
        "bio": "",
        "depth_score": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    await db.users.insert_one(doc)

    access = make_access(uid, email)

    set_auth_cookies(
        response,
        access,
        make_refresh(uid)
    )

    doc.pop("password_hash", None)
    doc.pop("_id", None)

    return {
        "user": doc,
        "access_token": access,
        **doc
    }


@api.post("/auth/login")
async def login(payload: LoginIn, response: Response):

    email = payload.email.lower()

    user = await db.users.find_one({"email": email})

    if not user or not verify_pw(payload.password, user["password_hash"]):
        raise HTTPException(401, "invalid credentials")

    access = make_access(user["id"], email)

    set_auth_cookies(
        response,
        access,
        make_refresh(user["id"])
    )

    user.pop("password_hash", None)
    user.pop("_id", None)

    return {
        "user": user,
        "access_token": access,
        **user
    }


@api.get("/auth/me")
async def me(user: dict = Depends(current_user)):
    return user


# -----------------------------------------------------------------------------
# Discovery Routes
# -----------------------------------------------------------------------------

@api.get("/artists")
async def list_artists():
    return await db.artists.find({}, {"_id": 0}).to_list(500)


@api.get("/albums")
async def list_albums():
    return await db.albums.find({}, {"_id": 0}).to_list(500)


@api.get("/tracks")
async def list_tracks():
    return await db.tracks.find({}, {"_id": 0}).to_list(500)


@api.get("/vibes")
async def list_vibes():
    return await db.vibes.find({}, {"_id": 0}).to_list(500)


@api.get("/explore/portal")
async def portal():

    featured_album = await db.albums.find_one(
        {"id": "blonde"},
        {"_id": 0}
    )

    rabbit_holes = await db.lore.find(
        {},
        {"_id": 0}
    ).limit(5).to_list(5)

    vibes = await db.vibes.find(
        {},
        {"_id": 0}
    ).limit(8).to_list(8)

    theories = await db.theories.find(
        {},
        {"_id": 0}
    ).limit(3).to_list(3)

    contributors = await db.contributors.find(
        {},
        {"_id": 0}
    ).limit(4).to_list(4)

    return {
        "featured_album": featured_album,
        "rabbit_holes": rabbit_holes,
        "vibes": vibes,
        "theories": theories,
        "contributors": contributors
    }


@api.get("/")
async def root():
    return {
        "name": "unmapped",
        "tagline": "music culture is a place to inhabit"
    }


# -----------------------------------------------------------------------------
# Mount
# -----------------------------------------------------------------------------

app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)