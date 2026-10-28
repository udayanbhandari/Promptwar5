"""Events router providing CRUD operations."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.core.security import limiter
from app.db.session import get_db
from app.models import Event
from app.schemas.event import (
    EventCreate,
    EventDetailResponse,
    EventResponse,
    EventUpdate,
)

router = APIRouter(prefix="/events", tags=["Events"])


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new event",
)
@limiter.limit("60/minute")
def create_event(
    request: Request,
    payload: EventCreate,
    db: Session = Depends(get_db),
) -> EventResponse:
    """Create a new event record with validated parameters."""
    event = Event(
        title=payload.title,
        event_type=payload.event_type.value,
        target_date=payload.target_date,
        guest_count=payload.guest_count,
        total_budget=payload.total_budget,
        currency=payload.currency.value,
        city=payload.city,
        theme_style=payload.theme_style,
        special_requirements=payload.special_requirements,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get(
    "",
    response_model=List[EventResponse],
    summary="List all events",
)
def list_events(
    db: Session = Depends(get_db),
) -> List[EventResponse]:
    """Retrieve all created events, ordered by target date."""
    events = db.query(Event).order_by(Event.target_date.asc()).all()
    return events


@router.get(
    "/{event_id}",
    response_model=EventDetailResponse,
    summary="Get event details by ID",
)
def get_event(
    event_id: str,
    db: Session = Depends(get_db),
) -> EventDetailResponse:
    """Retrieve full event detail including budget, tasks, vendors, and risks."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return event


@router.patch(
    "/{event_id}",
    response_model=EventResponse,
    summary="Update event details",
)
def update_event(
    event_id: str,
    payload: EventUpdate,
    db: Session = Depends(get_db),
) -> EventResponse:
    """Partially update an event's attributes."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field in ("event_type", "currency") and value is not None:
            setattr(event, field, value.value if hasattr(value, "value") else str(value))
        else:
            setattr(event, field, value)

    db.commit()
    db.refresh(event)
    return event


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an event",
)
def delete_event(
    event_id: str,
    db: Session = Depends(get_db),
):
    """Delete an event and cascade-remove all child associations."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}
