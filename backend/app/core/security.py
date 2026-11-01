"""Security, rate limiting, and sanitization utilities."""

import re
import secrets

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings

# Global rate limiter using remote client IP
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.RATE_LIMIT_DEFAULT],
)

_CONTROL_CHARS_RE = re.compile(r"[\x00-\x1f\x7f]")


def sanitize_text(value: str | None, max_length: int = 2000) -> str | None:
    """Sanitize freeform user input and bound its size."""
    if value is None:
        return None
    cleaned = str(value)
    cleaned = re.sub(r"<(script|style)[^>]*?>.*?</\1>", "", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"<[^>]*?>", "", cleaned)
    cleaned = _CONTROL_CHARS_RE.sub("", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned or None


def normalize_prompt_text(value: str | None, max_length: int = 2000) -> str:
    """Normalize user text for model prompts without allowing injection or oversized content."""
    sanitized = sanitize_text(value, max_length=max_length)
    return sanitized if sanitized is not None else ""


def create_owner_token() -> str:
    """Create a high-entropy owner token for event access checks."""
    return secrets.token_urlsafe(32)


def constant_time_compare(a: str, b: str) -> bool:
    """Compare secrets without exposing timing differences."""
    if not isinstance(a, str) or not isinstance(b, str):
        return False
    return secrets.compare_digest(a, b)


def get_owner_token(request: Request) -> str | None:
    """Read the owner token from the request headers."""
    return request.headers.get(settings.OWNER_TOKEN_HEADER, request.headers.get("x-owner-token"))


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add baseline security headers to every response."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        headers = {
            "Content-Security-Policy": (
                "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
                "script-src 'self'; connect-src 'self' https:; object-src 'none'; "
                "base-uri 'self'; frame-ancestors 'none'"
            ),
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=(), interest-cohort=()",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        }
        for key, value in headers.items():
            response.headers.setdefault(key, value)
        return response


def redact_sensitive_data(message: str) -> str:
    """Remove secrets and tokens from logs."""
    if not message:
        return message
    patterns = [
        settings.GEMINI_API_KEY,
        settings.GEMINI_MODEL,
        settings.DATABASE_URL,
    ]
    for secret in [s for s in patterns if s]:
        message = message.replace(secret, "[REDACTED]")
    return message
