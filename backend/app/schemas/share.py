"""Pydantic schemas for Share Links."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ShareLinkBase(BaseModel):
    """Base share link attributes."""

    token: str = Field(..., min_length=1, max_length=64)
    is_active: bool = True
    expires_at: Optional[datetime] = None
    view_count: int = 0


class ShareLinkCreate(BaseModel):
    """Schema for creating a share link."""

    token: Optional[str] = None
    is_active: bool = True
    expires_at: Optional[datetime] = None


class ShareLinkUpdate(BaseModel):
    """Schema for updating a share link."""

    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None


class ShareLinkResponse(ShareLinkBase):
    """Schema for returning a share link."""

    id: str
    event_id: str
    created_at: datetime
    share_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
