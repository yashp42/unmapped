from pathlib import Path
from typing import List

from pydantic import AnyHttpUrl, BaseSettings, Field


class Settings(BaseSettings):
    MONGO_URL: str = Field(..., env="MONGO_URL")
    DB_NAME: str = Field("unmapped", env="DB_NAME")

    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(720, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, env="REFRESH_TOKEN_EXPIRE_DAYS")

    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    ADMIN_EMAIL: str = Field("admin@unmapped.fm", env="ADMIN_EMAIL")
    ADMIN_HANDLE: str = Field("admin", env="ADMIN_HANDLE")
    ADMIN_PASSWORD: str = Field("changeme", env="ADMIN_PASSWORD")

    class Config:
        env_file = Path(__file__).parent / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
