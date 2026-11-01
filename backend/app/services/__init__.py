"""Services package exports."""

from app.services.ai_client import generate_structured, wrap_user_input
from app.services.errors import AIError, AISchemaValidationError, AIUnavailable
from app.services.fallbacks import (
    get_fallback_budget_split,
    get_fallback_ideas,
    get_fallback_risk_scenarios,
    get_fallback_vendor_brief,
    get_fallback_vendor_categories,
)

__all__ = [
    "AIError",
    "AIUnavailable",
    "AISchemaValidationError",
    "generate_structured",
    "wrap_user_input",
    "get_fallback_budget_split",
    "get_fallback_ideas",
    "get_fallback_vendor_categories",
    "get_fallback_risk_scenarios",
    "get_fallback_vendor_brief",
]
