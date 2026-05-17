import logging
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from ..config import settings, UPLOAD_DIR

logger = logging.getLogger("unmapped.upload")

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}


async def upload_avatar(file: UploadFile, user_id: str) -> str:
    content_type = file.content_type or ""
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image must be JPEG, PNG, WebP, or GIF",
        )

    data = await file.read()
    max_bytes = settings.MAX_UPLOAD_MB * 1024 * 1024
    if len(data) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image must be under {settings.MAX_UPLOAD_MB}MB",
        )

    if settings.cloudinary_enabled:
        return _upload_cloudinary(data, user_id)

    return _upload_local(data, user_id, ALLOWED_CONTENT_TYPES[content_type])


def _upload_cloudinary(data: bytes, user_id: str) -> str:
    try:
        import cloudinary
        import cloudinary.uploader

        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )
        result = cloudinary.uploader.upload(
            data,
            folder="unmapped/avatars",
            public_id=f"{user_id}-{uuid.uuid4().hex[:8]}",
            overwrite=True,
            resource_type="image",
        )
        return result["secure_url"]
    except Exception as exc:
        logger.exception("Cloudinary upload failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Image upload failed",
        ) from exc


def _upload_local(data: bytes, user_id: str, extension: str) -> str:
    filename = f"{user_id}-{uuid.uuid4().hex[:10]}{extension}"
    path = UPLOAD_DIR / filename
    path.write_bytes(data)
    return f"{settings.PUBLIC_API_URL}/api/media/avatars/{filename}"
