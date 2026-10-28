"""Standard API error response schema."""

from typing import Any, Optional
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standardized API error envelope."""

    error: str
    message: str
    details: Optional[Any] = None
