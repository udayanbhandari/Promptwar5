"""Pydantic schemas for Budget Items."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.core.security import sanitize_text


class BudgetItemBase(BaseModel):
    """Base budget item attributes."""

    category: str = Field(..., min_length=1, max_length=50)
    item_name: str = Field(..., min_length=1, max_length=150)
    estimated_cost: float = Field(..., ge=0.0)
    actual_cost: float = Field(default=0.0, ge=0.0)
    is_paid: bool = Field(default=False)
    priority: int = Field(default=2, ge=1, le=3)

    @field_validator("category", "item_name", mode="before")
    @classmethod
    def strip_text(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            cleaned = sanitize_text(v)
            if not cleaned:
                raise ValueError("Text field cannot be empty.")
            return cleaned
        return v


class BudgetItemCreate(BudgetItemBase):
    """Schema for creating a budget item."""

    pass


class BudgetItemUpdate(BaseModel):
    """Schema for updating a budget item."""

    category: Optional[str] = Field(None, min_length=1, max_length=50)
    item_name: Optional[str] = Field(None, min_length=1, max_length=150)
    estimated_cost: Optional[float] = Field(None, ge=0.0)
    actual_cost: Optional[float] = Field(None, ge=0.0)
    is_paid: Optional[bool] = None
    priority: Optional[int] = Field(None, ge=1, le=3)

    @field_validator("category", "item_name", mode="before")
    @classmethod
    def strip_text(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            cleaned = sanitize_text(v)
            if not cleaned:
                raise ValueError("Text field cannot be empty.")
            return cleaned
        return v


class BudgetItemResponse(BudgetItemBase):
    """Schema for returning a budget item."""

    id: str
    event_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
