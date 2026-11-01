"""Application services for generating and retrieving event plans."""

from __future__ import annotations

from datetime import date
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import BudgetItem, Event, Task, Vendor
from app.engines.budget_engine import allocate
from app.engines.budget_engine import warnings as budget_warnings
from app.engines.runsheet_engine import build_runsheet
from app.engines.timeline_engine import build_timeline
from app.prompts import budget_split_v1, ideas_v1, vendor_categories_v1
from app.schemas.task import TaskUpdate
from app.services.ai_client import generate_structured
from app.services.errors import AIUnavailable
from app.services.fallbacks import (
    get_fallback_budget_split,
    get_fallback_ideas,
    get_fallback_vendor_categories,
)


def get_event_or_404(event_id: str, db: Session) -> Event:
    """Load an event or raise the standard not-found response."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


def _build_prompts(event: Event) -> tuple[str, str, str]:
    """Build the three prompts required for a generated plan."""
    event_type = str(event.event_type)
    guest_count = int(event.guest_count)
    city = str(event.city)
    culture_style = str(event.theme_style or "")
    special_requirements = str(event.special_requirements or "")
    return (
        budget_split_v1.build_prompt(
            event_type=event_type,
            guest_count=guest_count,
            city=city,
            culture_style=culture_style,
            special_requirements=special_requirements,
        ),
        ideas_v1.build_prompt(
            event_type=event_type,
            guest_count=guest_count,
            city=city,
            culture_style=culture_style,
            special_requirements=special_requirements,
        ),
        vendor_categories_v1.build_prompt(
            event_type=event_type,
            guest_count=guest_count,
            city=city,
            special_requirements=special_requirements,
        ),
    )


def get_ai_plan_payload(event: Event, ai_generator=generate_structured) -> dict[str, Any]:
    """Generate structured suggestions, falling back when AI is unavailable."""
    budget_prompt, idea_prompt, vendor_prompt = _build_prompts(event)
    try:
        return {
            "budget": ai_generator(budget_prompt, budget_split_v1.OutputSchema),
            "ideas": ai_generator(idea_prompt, ideas_v1.OutputSchema),
            "vendors": ai_generator(vendor_prompt, vendor_categories_v1.OutputSchema),
            "used_fallback": False,
        }
    except AIUnavailable:
        event_type = str(event.event_type)
        return {
            "budget": get_fallback_budget_split(event_type),
            "ideas": get_fallback_ideas(event_type),
            "vendors": get_fallback_vendor_categories(event_type),
            "used_fallback": True,
        }


def _save_budget_items(event: Event, allocations: dict[str, int], db: Session) -> list[BudgetItem]:
    """Persist generated budget allocations."""
    items = []
    for category, amount in allocations.items():
        item = BudgetItem(
            event_id=event.id,
            category=category,
            item_name=category,
            estimated_cost=float(amount) / 100.0,
            actual_cost=0.0,
            is_paid=False,
            priority=2,
        )
        db.add(item)
        items.append(item)
    return items


def _save_tasks(event: Event, target_date: date, db: Session) -> list[Task]:
    """Build and persist the deterministic event timeline."""
    saved = []
    for task in build_timeline(str(event.event_type), target_date, date.today()):
        created = Task(
            event_id=event.id,
            title=str(task["title"]),
            category=str(task["category"]),
            due_date=task["due_date"],
            status="pending",
            owner="Host",
            depends_on=list(task.get("depends_on") or []),
            is_day_of=bool(task.get("is_critical") and "event" in str(task["title"]).lower()),
            start_time=None,
        )
        db.add(created)
        saved.append(created)
    return saved


def _save_vendors(event: Event, categories: Any, db: Session) -> list[Vendor]:
    """Persist vendor recommendations and their decision checklists."""
    vendors = []
    for category in categories:
        vendor = Vendor(
            event_id=event.id,
            category=category.category,
            name=f"{category.category} Specialist",
            status="researching",
            quoted_price=0.0,
            contact_info=None,
            notes="Questions: " + "; ".join(category.questions) + " | Red flags: " + "; ".join(category.red_flags),
        )
        db.add(vendor)
        vendors.append(vendor)
    return vendors


def _serialize_budget(items: list[BudgetItem], include_id: bool = True) -> list[dict[str, Any]]:
    """Serialize persisted budget records."""
    return [
        {
            **({"id": item.id} if include_id else {}),
            "category": item.category,
            "item_name": item.item_name,
            "estimated_cost": item.estimated_cost,
            "actual_cost": item.actual_cost,
            "priority": item.priority,
        }
        for item in items
    ]


def _serialize_task(task: Task) -> dict[str, Any]:
    """Serialize a persisted task record."""
    return {
        "id": task.id,
        "title": task.title,
        "category": task.category,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "status": task.status,
        "owner": task.owner,
        "depends_on": task.depends_on,
        "is_day_of": task.is_day_of,
    }


def _serialize_vendor(vendor: Vendor) -> dict[str, Any]:
    """Serialize a persisted vendor record."""
    return {
        "id": vendor.id,
        "category": vendor.category,
        "name": vendor.name,
        "status": vendor.status,
        "quoted_price": vendor.quoted_price,
        "contact_info": vendor.contact_info,
    }


def _clear_existing_plan(event_id: str, db: Session) -> None:
    """Delete previous generated records before regeneration."""
    for model in (BudgetItem, Task, Vendor):
        db.query(model).filter(model.event_id == event_id).delete(synchronize_session=False)


def generate_event_plan(event_id: str, db: Session, ai_generator=generate_structured) -> dict[str, Any]:
    """Generate, persist, and serialize a complete event plan."""
    event = get_event_or_404(event_id, db)
    payload = get_ai_plan_payload(event, ai_generator)
    percentages = {item.category: float(item.percentage) for item in payload["budget"].categories}
    allocations = allocate(int(round(float(event.total_budget) * 100)), percentages)
    _clear_existing_plan(str(event.id), db)
    budget_items = _save_budget_items(event, allocations, db)
    target_date = (
        event.target_date
        if isinstance(event.target_date, date)
        else date.fromisoformat(str(event.target_date))
    )
    tasks = _save_tasks(event, target_date, db)
    vendors = _save_vendors(event, payload["vendors"].categories, db)
    db.commit()
    for record in [*budget_items, *tasks, *vendors]:
        db.refresh(record)
    return {
        "title": event.title,
        "event_id": event.id,
        "used_fallback": payload["used_fallback"],
        "budget": _serialize_budget(budget_items, include_id=False),
        "ideas": [idea.model_dump() for idea in payload["ideas"].ideas],
        "vendor_categories": [category.model_dump() for category in payload["vendors"].categories],
        "tasks": [_serialize_task(task) for task in tasks],
        "vendors": [_serialize_vendor(vendor) for vendor in vendors],
        "warnings": budget_warnings(
            [{"category": item.category, "amount": item.estimated_cost} for item in budget_items],
            int(event.guest_count),
        ),
    }


def get_event_plan(event_id: str, db: Session) -> dict[str, Any]:
    """Retrieve a persisted plan for an event."""
    event = get_event_or_404(event_id, db)
    budget_items = db.query(BudgetItem).filter(BudgetItem.event_id == event.id).all()
    tasks = db.query(Task).filter(Task.event_id == event.id).order_by(Task.due_date.asc()).all()
    vendors = db.query(Vendor).filter(Vendor.event_id == event.id).all()
    if not budget_items and not tasks and not vendors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not generated for this event")
    return {
        "title": event.title,
        "event_id": event.id,
        "budget": _serialize_budget(budget_items),
        "tasks": [_serialize_task(task) for task in tasks],
        "vendors": [_serialize_vendor(vendor) for vendor in vendors],
    }


def update_event_task(task_id: str, payload: TaskUpdate, db: Session) -> dict[str, Any]:
    """Apply a partial update to a task and return the updated record."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return _serialize_task(task)


def get_event_runsheet(event_id: str, db: Session) -> dict[str, Any]:
    """Build the event-day run sheet for an event."""
    event = get_event_or_404(event_id, db)
    return {
        "event_id": event.id,
        "runsheet": build_runsheet(str(event.event_type), "09:00", int(event.guest_count)),
    }
