"""Application configuration loaded from environment variables."""

import ast
from functools import lru_cache

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for EventPilot application."""

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    DATABASE_URL: str = "sqlite:///./events.db"

    ALLOWED_ORIGINS: list[str] | str = Field(
        default=[
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
        ],
        validation_alias=AliasChoices("ALLOWED_ORIGINS", "CORS_ORIGINS"),
    )
    CORS_METHODS: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    CORS_HEADERS: list[str] = ["Authorization", "Content-Type", "X-Owner-Token", "X-Event-Owner-Token"]

    RATE_LIMIT_DEFAULT: str = "100/minute"
    AI_RATE_LIMIT: str = "10/minute"
    PUBLIC_RATE_LIMIT: str = "20/minute"
    MAX_REQUEST_SIZE_BYTES: int = 5_000_000
    OWNER_TOKEN_HEADER: str = "x-owner-token"

    PROJECT_NAME: str = "EventPilot API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_origins(cls, v: str | list[str]) -> list[str]:
        """Parse allowed origins from a comma-separated string or python list."""
        if v is None:
            return []
        if isinstance(v, str):
            if v.startswith("["):
                try:
                    parsed = ast.literal_eval(v)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed if str(item).strip()]
                except (SyntaxError, ValueError, TypeError):
                    return [item.strip() for item in v.split(",") if item.strip()]
            return [item.strip() for item in v.split(",") if item.strip()]
        if isinstance(v, list):
            return [str(item).strip() for item in v if str(item).strip()]
        return []

    @property
    def cors_origins(self) -> list[str]:
        """Return the configured allowed origins for CORS middleware."""
        return self.ALLOWED_ORIGINS if isinstance(self.ALLOWED_ORIGINS, list) else []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached instance of application settings."""
    return Settings()


# Singleton instance for direct convenience imports
settings = get_settings()
