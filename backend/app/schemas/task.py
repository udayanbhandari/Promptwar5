"""Pydantic schemas for Tasks and Milestones."""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.core.security import sanitize_text
from app.schemas.common import TaskStatus


class TaskBase(BaseModel):
    """Base task attributes."""

    title: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., min_length=1, max_length=50)
    due_date: date
    status: TaskStatus = TaskStatus.PENDING
    owner: str = Field(default="Host", min_length=1, max_length=100)
    depends_on: List[str] = Field(default_factory=list, description="List of task IDs that must complete first")
    is_day_of: bool = Field(default=False)
    start_time: Optional[str] = Field(None, pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$")

    @field_validator("title", "category", "owner", mode="before")
    @classmethod
    def strip_text(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            cleaned = sanitize_text(v)
            if not cleaned:
                raise ValueError("Text field cannot be empty.")
            return cleaned
        return v


class TaskCreate(TaskBase):
    """Schema for creating a task."""

    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    due_date: Optional[date] = None
    status: Optional[TaskStatus] = None
    owner: Optional[str] = Field(None, min_length=1, max_length=100)
    depends_on: Optional[List[str]] = None
    is_day_of: Optional[bool] = None
    start_time: Optional[str] = Field(None, pattern=r"^(?:[01]\d|2[0-3]):[0-5]\d$")

    @field_validator("title", "category", "owner", mode="before")
    @classmethod
    def strip_text(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            cleaned = sanitize_text(v)
            if not cleaned:
                raise ValueError("Text field cannot be empty.")
            return cleaned
        return v


class TaskResponse(TaskBase):
    """Schema for returning a task."""

    id: str
    event_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
