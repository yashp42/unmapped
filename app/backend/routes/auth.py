from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..config import settings
from ..schemas.auth import LoginPayload, RegisterPayload, TokenResponse
from ..schemas.users import UserCreate, UserPublic
from ..services.user_service import authenticate_user, create_user, find_user_by_email, find_user_by_handle
from ..utils.security import create_access_token
from ..dependencies import get_current_user

router = APIRouter()


@router.post("/register", response_model=UserPublic)
async def register(payload: RegisterPayload):
    email = payload.email.lower().strip()
    if await find_user_by_email(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if await find_user_by_handle(payload.handle):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Handle already taken")

    created = await create_user({
        "id": str(uuid4()),
        "email": email,
        "handle": payload.handle.strip().lower(),
        "password": payload.password,
    })
    return UserPublic(**created)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginPayload):
    user = await authenticate_user(payload.email.lower().strip(), payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {
        "access_token": create_access_token(user["id"]),
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserPublic)
async def me(current_user: dict = Depends(get_current_user)):
    return UserPublic(**current_user)
