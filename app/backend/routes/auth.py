from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status, Response

from schemas.auth import LoginPayload, RegisterPayload, TokenResponse
from schemas.users import UserPublic
from services.user_service import (
    authenticate_user,
    create_user,
    enrich_user,
    find_user_by_email,
    find_user_by_handle,
)
from utils.security import create_access_token, create_refresh_token, decode_token
from dependencies import get_current_user

router = APIRouter()


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie("access_token", access_token, httponly=True, samesite="lax")
    response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="lax")


def _clear_auth_cookies(response: Response) -> None:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


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
    return UserPublic(**{k: created[k] for k in UserPublic.model_fields if k in created})


@router.post("/login")
async def login(payload: LoginPayload, response: Response):
    user = await authenticate_user(payload.email.lower().strip(), payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(user["id"])
    refresh_token = create_refresh_token(user["id"])
    _set_auth_cookies(response, access_token, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": UserPublic(**{k: user[k] for k in UserPublic.model_fields if k in user}),
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_session(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

    try:
        payload = decode_token(token)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token payload")

    access_token = create_access_token(user_id)
    response.set_cookie("access_token", access_token, httponly=True, samesite="lax")
    return TokenResponse(access_token=access_token)


@router.post("/logout")
async def logout(response: Response):
    _clear_auth_cookies(response)
    return {"message": "logged out"}


@router.get("/me", response_model=UserPublic)
async def me(current_user: dict = Depends(get_current_user)):
    enriched = await enrich_user(current_user, include_private=False)
    return UserPublic(**enriched)  # type: ignore[arg-type]
