"""Pydantic schemas for Vendors."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.core.security import sanitize_text
from app.schemas.common import VendorStatus


class VendorBase(BaseModel):
    """Base vendor attributes."""

    category: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=150)
    status: VendorStatus = VendorStatus.RESEARCHING
    quoted_price: float = Field(default=0.0, ge=0.0)
    contact_info: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = Field(None, max_length=1000)

    @field_validator("category", "name", mode="before")
    @classmethod
    def strip_required_text(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            cleaned = sanitize_text(v)
            if not cleaned:
                raise ValueError("Text field cannot be empty.")
            return cleaned
        return v

    @field_validator("contact_info", "notes", mode="before")
    @classmethod
    def strip_optional_text(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            cleaned = sanitize_text(v)
            return cleaned if cleaned else None
        return v


class VendorCreate(VendorBase):
    """Schema for creating a vendor."""

    pass


class VendorUpdate(BaseModel):
    """Schema for updating a vendor."""

    category: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    status: Optional[VendorStatus] = None
    quoted_price: Optional[float] = Field(None, ge=0.0)
    contact_info: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = Field(None, max_length=1000)

    @field_validator("category", "name", mode="before")
    @classmethod
    def strip_required_text(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            cleaned = sanitize_text(v)
            if not cleaned:
                raise ValueError("Text field cannot be empty.")
            return cleaned
        return v

    @field_validator("contact_info", "notes", mode="before")
    @classmethod
    def strip_optional_text(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            cleaned = sanitize_text(v)
            return cleaned if cleaned else None
        return v


class VendorResponse(VendorBase):
    """Schema for returning a vendor."""

    id: str
    event_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
