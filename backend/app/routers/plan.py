"""Plan generation and management endpoints."""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.security import limiter
from app.db.session import get_db
from app.engines.budget_engine import allocate, warnings as budget_warnings
from app.engines.runsheet_engine import build_runsheet
from app.engines.timeline_engine import build_timeline
from app.models import BudgetItem, Event, Task, Vendor
from app.prompts import budget_split_v1, ideas_v1, vendor_categories_v1
from app.schemas.task import TaskUpdate
from app.services.ai_client import AIUnavailable, generate_structured
from app.services.fallbacks import (
    get_fallback_budget_split,
    get_fallback_ideas,
    get_fallback_vendor_categories,
)

router = APIRouter(prefix="/events", tags=["Planning"])


def _event_or_404(event_id: str, db: Session) -> Event:
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


def _ai_plan_payload(event: Event) -> Dict[str, Any]:
    budget_prompt = budget_split_v1.build_prompt(
        event_type=event.event_type,
        guest_count=event.guest_count,
        city=event.city,
        culture_style=event.theme_style or "",
        special_requirements=event.special_requirements or "",
    )
    idea_prompt = ideas_v1.build_prompt(
        event_type=event.event_type,
        guest_count=event.guest_count,
        city=event.city,
        culture_style=event.theme_style or "",
        special_requirements=event.special_requirements or "",
    )
    vendor_prompt = vendor_categories_v1.build_prompt(
        event_type=event.event_type,
        guest_count=event.guest_count,
        city=event.city,
        special_requirements=event.special_requirements or "",
    )

    used_fallback = False
    try:
        budget_output = generate_structured(budget_prompt, budget_split_v1.OutputSchema)
        idea_output = generate_structured(idea_prompt, ideas_v1.OutputSchema)
        vendor_output = generate_structured(vendor_prompt, vendor_categories_v1.OutputSchema)
    except AIUnavailable:
        used_fallback = True
        budget_output = get_fallback_budget_split(event.event_type)
        idea_output = get_fallback_ideas(event.event_type)
        vendor_output = get_fallback_vendor_categories(event.event_type)

    return {
        "budget": budget_output,
        "ideas": idea_output,
        "vendors": vendor_output,
        "used_fallback": used_fallback,
    }


@router.post("/{event_id}/generate-plan", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
def generate_plan(
    request: Request,
    event_id: str,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    event = _event_or_404(event_id, db)
    payload = _ai_plan_payload(event)

    category_percentages = {
        category.category: float(category.percentage)
        for category in payload["budget"].categories
    }
    total_minor = int(round(float(event.total_budget) * 100))
    allocations = allocate(total_minor, category_percentages)

    db.query(BudgetItem).filter(BudgetItem.event_id == event.id).delete(synchronize_session=False)
    db.query(Task).filter(Task.event_id == event.id).delete(synchronize_session=False)
    db.query(Vendor).filter(Vendor.event_id == event.id).delete(synchronize_session=False)

    budget_items = []
    for category_name, amount in allocations.items():
        item = BudgetItem(
            event_id=event.id,
            category=category_name,
            item_name=category_name,
            estimated_cost=float(amount) / 100.0,
            actual_cost=0.0,
            is_paid=False,
            priority=2,
        )
        db.add(item)
        budget_items.append(item)

    timeline = build_timeline(event.event_type, event.target_date, date.today())
    saved_tasks: List[Task] = []
    for task in timeline:
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
        saved_tasks.append(created)

    for index, task in enumerate(saved_tasks):
        task.depends_on = list(task.depends_on)

    vendors = []
    for category in payload["vendors"].categories:
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

    db.commit()
    for obj in list(budget_items) + saved_tasks + vendors:
        db.refresh(obj)

    return {
        "title": event.title,
        "event_id": event.id,
        "used_fallback": payload["used_fallback"],
        "budget": [
            {
                "category": item.category,
                "item_name": item.item_name,
                "estimated_cost": item.estimated_cost,
                "actual_cost": item.actual_cost,
                "priority": item.priority,
            }
            for item in budget_items
        ],
        "ideas": [
            {
                "aspect": idea.aspect,
                "title": idea.title,
                "description": idea.description,
                "cost_tier": idea.cost_tier,
                "why_it_fits": idea.why_it_fits,
            }
            for idea in payload["ideas"].ideas
        ],
        "vendor_categories": [
            {
                "category": category.category,
                "questions": category.questions,
                "red_flags": category.red_flags,
            }
            for category in payload["vendors"].categories
        ],
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "category": task.category,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "status": task.status,
                "owner": task.owner,
                "depends_on": task.depends_on,
                "is_day_of": task.is_day_of,
            }
            for task in saved_tasks
        ],
        "vendors": [
            {
                "id": vendor.id,
                "category": vendor.category,
                "name": vendor.name,
                "status": vendor.status,
                "quoted_price": vendor.quoted_price,
                "contact_info": vendor.contact_info,
            }
            for vendor in vendors
        ],
        "warnings": budget_warnings(
            [{"category": item.category, "amount": item.estimated_cost} for item in budget_items],
            event.guest_count,
        ),
    }


@router.get("/{event_id}/plan")
def get_plan(event_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    event = _event_or_404(event_id, db)
    budget_items = db.query(BudgetItem).filter(BudgetItem.event_id == event.id).all()
    tasks = db.query(Task).filter(Task.event_id == event.id).order_by(Task.due_date.asc()).all()
    vendors = db.query(Vendor).filter(Vendor.event_id == event.id).all()

    if not budget_items and not tasks and not vendors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not generated for this event")

    return {
        "title": event.title,
        "event_id": event.id,
        "budget": [
            {
                "id": item.id,
                "category": item.category,
                "item_name": item.item_name,
                "estimated_cost": item.estimated_cost,
                "actual_cost": item.actual_cost,
                "priority": item.priority,
            }
            for item in budget_items
        ],
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "category": task.category,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "status": task.status,
                "owner": task.owner,
                "depends_on": task.depends_on,
                "is_day_of": task.is_day_of,
            }
            for task in tasks
        ],
        "vendors": [
            {
                "id": vendor.id,
                "category": vendor.category,
                "name": vendor.name,
                "status": vendor.status,
                "quoted_price": vendor.quoted_price,
                "contact_info": vendor.contact_info,
            }
            for vendor in vendors
        ],
    }


@router.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdate, db: Session = Depends(get_db)) -> Dict[str, Any]:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)

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


@router.get("/{event_id}/runsheet")
def get_runsheet(event_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    event = _event_or_404(event_id, db)
    schedule = build_runsheet(event.event_type, "09:00", event.guest_count)
    return {"event_id": event.id, "runsheet": schedule}
