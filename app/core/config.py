import os
from decouple import config as decouple_conf
from pathlib import Path
from pydantic import PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings
from typing import Any, Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "zerone-quest-backend"
    SECRET_KEY: str = decouple_conf("SECRET_KEY")
    MEDIA_DIR_NAME: str = "media"
    BASE_DIR: str = str(Path(__file__).resolve().parent.parent.parent)
    MEDIA_DIR: str = os.path.join(BASE_DIR, MEDIA_DIR_NAME)
    WEBSOCKET_CHANNEL: str = 'zerone-quest-backend-websocket'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 
    ALGORITHM: str = "HS256"
    DATABASE_USER: str = decouple_conf('DATABASE_USER')
    DATABASE_PASSWORD: str = decouple_conf('DATABASE_PASSWORD')
    DATABASE_HOST: str = decouple_conf('DATABASE_HOST')
    DATABASE_PORT: int = decouple_conf('DATABASE_PORT')
    DATABASE_NAME: str = decouple_conf('DATABASE_NAME')
    SQL_DATABASE_URI: Optional[PostgresDsn] = None

    MAIL_USERNAME: str = decouple_conf("MAIL_USERNAME")
    MAIL_PASSWORD: str = decouple_conf("MAIL_PASSWORD")
    MAIL_FROM: str = decouple_conf("MAIL_FROM")
    MAIL_PORT: int = decouple_conf("MAIL_PORT", default=587, cast=int)
    MAIL_SERVER: str = decouple_conf("MAIL_SERVER", default="smtp.gmail.com")
    MAIL_STARTTLS: bool = decouple_conf("MAIL_STARTTLS", default=True, cast=bool)
    MAIL_SSL_TLS: bool = decouple_conf("MAIL_SSL_TLS", default=False, cast=bool)
    IS_DEV: bool = decouple_conf("IS_DEV", default=False, cast=bool)
    GOOGLE_CLIENT_ID: str = decouple_conf("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = decouple_conf("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = decouple_conf("GOOGLE_REDIRECT_URI", default="http://localhost:8000/auth/callback")

    FRONTEND_URL: str = decouple_conf("FRONTEND_URL", default="http://localhost:3000")
    @field_validator("SQL_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("DATABASE_USER"),
            password=values.data.get("DATABASE_PASSWORD"),
            host=values.data.get("DATABASE_HOST"),
            path=values.data.get('DATABASE_NAME'),
            port=values.data.get('DATABASE_PORT')
        )


settings = Settings()
