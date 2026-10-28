"""Security, rate limiting, and sanitization utilities."""

import re
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

# Global rate limiter using remote client IP
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.RATE_LIMIT_DEFAULT],
)


def sanitize_text(value: Optional[str]) -> Optional[str]:
    """Sanitize freeform user input.

    - Removes script and style blocks entirely (including their contents)
    - Removes all remaining HTML tags
    - Strips leading/trailing whitespace
    - Normalizes internal multiple spaces
    """
    if value is None:
        return None

    # Strip script and style blocks and their internal contents
    cleaned = re.sub(r"<(script|style)[^>]*?>.*?</\1>", "", value, flags=re.IGNORECASE | re.DOTALL)
    # Strip any remaining HTML tags
    cleaned = re.sub(r"<[^>]*?>", "", cleaned)
    # Normalize multiple whitespace characters to single space
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned
