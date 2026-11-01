"""Pydantic schemas for Plan B Risk Scenarios."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.security import sanitize_text
from app.schemas.common import ScenarioType


class RiskScenarioBase(BaseModel):
    """Base contingency scenario attributes."""

    scenario_type: ScenarioType
    trigger_name: str = Field(..., min_length=1, max_length=150)
    mitigation_plan: str = Field(..., min_length=1, max_length=2000)
    budget_impact: float = Field(default=0.0)
    is_activated: bool = Field(default=False)

    @field_validator("trigger_name", "mitigation_plan", mode="before")
    @classmethod
    def strip_text(cls, v: str | None) -> str | None:
        if isinstance(v, str):
            cleaned = sanitize_text(v)
            if not cleaned:
                raise ValueError("Text field cannot be empty.")
            return cleaned
        return v


class RiskScenarioCreate(RiskScenarioBase):
    """Schema for creating a contingency scenario."""

    pass


class RiskScenarioUpdate(BaseModel):
    """Schema for updating a contingency scenario."""

    scenario_type: ScenarioType | None = None
    trigger_name: str | None = Field(None, min_length=1, max_length=150)
    mitigation_plan: str | None = Field(None, min_length=1, max_length=2000)
    budget_impact: float | None = None
    is_activated: bool | None = None

    @field_validator("trigger_name", "mitigation_plan", mode="before")
    @classmethod
    def strip_text(cls, v: str | None) -> str | None:
        if isinstance(v, str):
            cleaned = sanitize_text(v)
            if not cleaned:
                raise ValueError("Text field cannot be empty.")
            return cleaned
        return v


class RiskScenarioResponse(RiskScenarioBase):
    """Schema for returning a contingency scenario."""

    id: str
    event_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
