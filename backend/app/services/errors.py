"""AI service exception definitions."""


class AIError(Exception):
    """Base exception for all AI-related errors."""

    pass


class AIUnavailable(AIError):
    """Raised when the AI service is offline, unconfigured, or exhausted retries."""

    pass


class AISchemaValidationError(AIError):
    """Raised when AI response fails schema validation."""

    pass
