import os
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV = os.getenv("ENV", "development")


class Settings(BaseSettings):
    """
    Centralized, strongly-typed configuration class using Pydantic Settings.
    Retrieves all values from OS environment variables and `.env` files automatically.
    Provides safe defaults for development and raises strict validation errors in production.
    """

    ENV: str = ENV
    PORT: int = 8000
    IP_ADDRESS: str = "127.0.0.1"

    APP_TITLE: str = "Enterprise CRM Backend"
    APP_DESCRIPTION: str = "High-performance, asynchronous REST API services built with FastAPI, SQLAlchemy 2.0, and Pydantic v2."
    APP_VERSION: str = "1.0.0"

    # Database and secrets (no hardcoding)
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_IN: int = 15  # 15 minutes
    REFRESH_TOKEN_EXPIRES_IN: int = 7  # 7 days
    REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"
    SALT_ROUNDS: int = 12

    # Mail parameters
    MAIL_HOST: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
    MAIL_USER: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_SECURE: bool = False
    MAIL_FROM: str = ""

    # Cookies
    COOKIE_NAME: str = "access_token"
    COOKIE_MAX_AGE: int = 604800
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "Lax"
    COOKIE_SAME_SITE: str | None = None


    # Tell Pydantic how to discover and parse the .env file automatically
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / f".env.{ENV}")
        if (BASE_DIR / f".env.{ENV}").exists()
        else str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        """
        Configure environment-specific settings like secure cookies.
        Pydantic automatically strictly enforces missing variables like DATABASE_URL.
        """
        if self.ENV == "production":
            self.COOKIE_SECURE = True
        else:
            self.COOKIE_SECURE = False

        # Synchronize cookie same-site variable names
        if self.COOKIE_SAME_SITE:
            self.COOKIE_SAMESITE = self.COOKIE_SAME_SITE

        return self


# Global singleton configuration object instance
config = Settings()
