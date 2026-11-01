"""Common enums and error schemas."""

from enum import Enum

from app.schemas.errors import ErrorResponse


class EventType(str, Enum):
    """Allowed event categories."""

    WEDDING = "wedding"
    BIRTHDAY = "birthday"
    COMMUNITY = "community"


class Currency(str, Enum):
    """Allow-listed currency codes (INR, USD, EUR, GBP, AED)."""

    INR = "INR"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    AED = "AED"


class TaskStatus(str, Enum):
    """Execution status of tasks."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class VendorStatus(str, Enum):
    """Procurement status of vendors."""

    RESEARCHING = "researching"
    CONTACTED = "contacted"
    QUOTED = "quoted"
    BOOKED = "booked"


class ScenarioType(str, Enum):
    """Contingency categories."""

    WEATHER = "weather"
    BUDGET_CUT = "budget_cut"
    VENDOR_FLAKE = "vendor_flake"
    GUEST_SURGE = "guest_surge"


__all__ = [
    "EventType",
    "Currency",
    "TaskStatus",
    "VendorStatus",
    "ScenarioType",
    "ErrorResponse",
]
