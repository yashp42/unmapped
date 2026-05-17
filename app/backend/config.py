import logging
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

logger = logging.getLogger("unmapped.config")

BACKEND_ROOT = Path(__file__).parent
UPLOAD_DIR = BACKEND_ROOT / "uploads" / "avatars"


class Settings:
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")

    MONGO_URL: str = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME: str = os.environ.get("DB_NAME", "unmapped")

    JWT_SECRET: str | None = os.environ.get("JWT_SECRET")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "720"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    CORS_ORIGINS: List[str] = [
        origin.strip()
        for origin in os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")
        if origin.strip()
    ]

    PUBLIC_API_URL: str = os.environ.get("PUBLIC_API_URL", "http://127.0.0.1:8001").rstrip("/")
    MAX_UPLOAD_MB: int = int(os.environ.get("MAX_UPLOAD_MB", "5"))

    CLOUDINARY_CLOUD_NAME: str | None = os.environ.get("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY: str | None = os.environ.get("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: str | None = os.environ.get("CLOUDINARY_API_SECRET")

    ADMIN_EMAIL: str = os.environ.get("ADMIN_EMAIL", "admin@unmapped.fm")
    ADMIN_HANDLE: str = os.environ.get("ADMIN_HANDLE", "admin")
    ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD", "changeme")

    @property
    def cloudinary_enabled(self) -> bool:
        return bool(self.CLOUDINARY_CLOUD_NAME and self.CLOUDINARY_API_KEY and self.CLOUDINARY_API_SECRET)

    def validate(self) -> None:
        if self.JWT_SECRET:
            pass
        elif self.ENVIRONMENT == "production":
            raise RuntimeError("JWT_SECRET must be set when ENVIRONMENT=production")
        else:
            self.JWT_SECRET = "dev-only-change-before-deploy"
            logger.warning("JWT_SECRET is not set; using insecure development default")

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.validate()
