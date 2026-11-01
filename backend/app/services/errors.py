"""AI service exception definitions."""


class AIError(Exception):
    """Base exception for all AI-related errors."""

    pass


class AIUnavailableError(AIError):
    """Raised when the AI service is offline, unconfigured, or exhausted retries."""

    pass


AIUnavailable = AIUnavailableError


class AISchemaValidationError(AIError):
    """Raised when AI response fails schema validation."""

    pass
