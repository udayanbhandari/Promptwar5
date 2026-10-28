"""Application configuration loaded from environment variables."""

from functools import lru_cache
from typing import List, Union
from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for EventPilot application."""

    # Google Gemini GenAI configuration
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Database connection string
    DATABASE_URL: str = "sqlite:///./events.db"

    # Allowed CORS / request origins
    ALLOWED_ORIGINS: Union[List[str], str] = Field(
        default=[
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
        ],
        validation_alias=AliasChoices("ALLOWED_ORIGINS", "CORS_ORIGINS"),
    )

    # Rate limiting
    RATE_LIMIT_DEFAULT: str = "100/minute"

    # Project metadata
    PROJECT_NAME: str = "EventPilot API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse allowed origins from list or comma-separated string."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

    # Expose CORS_ORIGINS property for backward compatibility
    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Backward compatible accessor for CORS middleware."""
        if isinstance(self.ALLOWED_ORIGINS, list):
            return self.ALLOWED_ORIGINS
        return ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Return a cached instance of application settings."""
    return Settings()


# Singleton instance for direct convenience imports
settings = get_settings()
