"""HTTP routes for event plan operations."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.security import limiter
from app.db.session import get_db
from app.schemas.task import TaskUpdate
from app.services.ai_client import generate_structured
from app.services.plan_service import (
    generate_event_plan,
    get_event_plan,
    get_event_runsheet,
    update_event_task,
)

router = APIRouter(prefix="/events", tags=["Planning"])


@router.post("/{event_id}/generate-plan", status_code=200)
@limiter.limit("10/minute")
def generate_plan(
    request: Request,
    event_id: str,
    db: Session = Depends(get_db),  # noqa: B008
) -> dict[str, Any]:
    """Generate a fresh plan for an event."""
    return generate_event_plan(event_id, db, generate_structured)


@router.get("/{event_id}/plan")
def get_plan(event_id: str, db: Session = Depends(get_db)) -> dict[str, Any]:  # noqa: B008
    """Return the generated plan for an event."""
    return get_event_plan(event_id, db)


@router.patch("/tasks/{task_id}")
def update_task(
    task_id: str,
    payload: TaskUpdate,
    db: Session = Depends(get_db),  # noqa: B008
) -> dict[str, Any]:
    """Apply a partial update to a task."""
    return update_event_task(task_id, payload, db)


@router.get("/{event_id}/runsheet")
def get_runsheet(event_id: str, db: Session = Depends(get_db)) -> dict[str, Any]:  # noqa: B008
    """Return the event-day run sheet."""
    return get_event_runsheet(event_id, db)
