"""Standard API error response schema."""

from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standardized API error envelope."""

    error: str
    message: str
    details: Any | None = None
