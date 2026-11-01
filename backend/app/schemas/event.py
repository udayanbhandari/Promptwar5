"""Pydantic schemas for Event creation, update, and detail responses."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.security import sanitize_text
from app.schemas.budget import BudgetItemResponse
from app.schemas.common import Currency, EventType
from app.schemas.risk import RiskScenarioResponse
from app.schemas.share import ShareLinkResponse
from app.schemas.task import TaskResponse
from app.schemas.vendor import VendorResponse


class EventBase(BaseModel):
    """Base event attributes with strict validation."""

    title: str = Field(..., min_length=1, max_length=200, description="Event title")
    event_type: EventType = Field(..., description="Type of event: wedding, birthday, community")
    target_date: date = Field(..., description="Target celebration date (must be strictly in the future)")
    guest_count: int = Field(..., ge=1, le=5000, description="Estimated guest count between 1 and 5000")
    total_budget: float = Field(..., gt=0.0, description="Total planned budget (must be greater than 0)")
    currency: Currency = Field(default=Currency.USD, description="Currency from allow-list (INR, USD, EUR, GBP, AED)")
    city: str = Field(..., min_length=1, max_length=100, description="City or region")
    theme_style: str | None = Field(None, max_length=150, description="Aesthetic, theme, or cultural style")
    special_requirements: str | None = Field(
        None, max_length=500, description="Dietary restrictions or accessibility needs"
    )

    @field_validator("target_date")
    @classmethod
    def validate_future_date(cls, v: date) -> date:
        """Enforce that event date must be strictly in the future."""
        if v <= date.today():
            raise ValueError("Event date must be in the future.")
        return v

    @field_validator("title", "city", mode="before")
    @classmethod
    def sanitize_required_strings(cls, v: str | None) -> str:
        """Strip text and ensure required fields are not empty or blank whitespace."""
        if v is None:
            raise ValueError("Field is required and cannot be None.")
        cleaned = sanitize_text(str(v))
        if not cleaned:
            raise ValueError("Field cannot be empty or blank whitespace.")
        return cleaned

    @field_validator("theme_style", "special_requirements", mode="before")
    @classmethod
    def sanitize_optional_strings(cls, v: str | None) -> str | None:
        """Strip text and convert empty strings to None."""
        if v is None:
            return None
        cleaned = sanitize_text(str(v))
        return cleaned if cleaned else None


class EventCreate(EventBase):
    """Schema for creating a new event."""

    pass


class EventUpdate(BaseModel):
    """Schema for partial update of an event (all fields optional)."""

    title: str | None = Field(None, min_length=1, max_length=200)
    event_type: EventType | None = None
    target_date: date | None = None
    guest_count: int | None = Field(None, ge=1, le=5000)
    total_budget: float | None = Field(None, gt=0.0)
    currency: Currency | None = None
    city: str | None = Field(None, min_length=1, max_length=100)
    theme_style: str | None = Field(None, max_length=150)
    special_requirements: str | None = Field(None, max_length=500)

    @field_validator("target_date")
    @classmethod
    def validate_future_date(cls, v: date | None) -> date | None:
        if v is not None and v <= date.today():
            raise ValueError("Event date must be in the future.")
        return v

    @field_validator("title", "city", mode="before")
    @classmethod
    def sanitize_required_strings(cls, v: str | None) -> str | None:
        if v is None:
            return None
        cleaned = sanitize_text(str(v))
        if not cleaned:
            raise ValueError("Field cannot be empty or blank whitespace.")
        return cleaned

    @field_validator("theme_style", "special_requirements", mode="before")
    @classmethod
    def sanitize_optional_strings(cls, v: str | None) -> str | None:
        if v is None:
            return None
        cleaned = sanitize_text(str(v))
        return cleaned if cleaned else None


class EventResponse(EventBase):
    """Standard event response without full relationship payloads."""

    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EventDetailResponse(EventResponse):
    """Detailed event response with all nested relational items."""

    budget_items: list[BudgetItemResponse] = []
    tasks: list[TaskResponse] = []
    vendors: list[VendorResponse] = []
    risk_scenarios: list[RiskScenarioResponse] = []
    share_links: list[ShareLinkResponse] = []

    model_config = ConfigDict(from_attributes=True)
