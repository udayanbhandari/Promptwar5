"""Pydantic schemas for Share Links."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ShareLinkBase(BaseModel):
    """Base share link attributes."""

    token: str = Field(..., min_length=1, max_length=64)
    is_active: bool = True
    expires_at: datetime | None = None
    view_count: int = 0


class ShareLinkCreate(BaseModel):
    """Schema for creating a share link."""

    token: str | None = None
    is_active: bool = True
    expires_at: datetime | None = None


class ShareLinkUpdate(BaseModel):
    """Schema for updating a share link."""

    is_active: bool | None = None
    expires_at: datetime | None = None


class ShareLinkResponse(ShareLinkBase):
    """Schema for returning a share link."""

    id: str
    event_id: str
    created_at: datetime
    share_url: str | None = None

    model_config = ConfigDict(from_attributes=True)
