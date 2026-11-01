"""Risk generation and simulation services for Plan B scenario analysis."""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.engines.budget_engine import recalculate
from app.models import BudgetItem, Event, RiskScenario
from app.prompts.risk_scenarios_v1 import build_prompt
from app.schemas.ai_outputs import RiskScenariosOutput
from app.services.ai_client import AIUnavailable, generate_structured
from app.services.fallbacks import get_fallback_risk_scenarios


def _scenario_type_for(title: str) -> str:
    text = (title or "").lower()
    if "weather" in text or "rain" in text or "heat" in text:
        return "weather"
    if "vendor" in text or "cancellation" in text or "no-show" in text:
        return "vendor_flake"
    if "guest" in text or "surge" in text or "attendance" in text:
        return "guest_surge"
    if "budget" in text or "overrun" in text or "cost" in text:
        return "budget_cut"
    return "weather"


def _to_risk_scenario_model(event: Event, item: Any) -> RiskScenario:
    return RiskScenario(
        event_id=event.id,
        scenario_type=_scenario_type_for(item.scenario_title),
        trigger_name=item.scenario_title,
        mitigation_plan=item.fallback_steps,
        budget_impact=float(item.cost_impact_percent),
        is_activated=False,
    )


def generate_risk_scenarios(event: Event, db: Session) -> list[RiskScenario]:
    """Generate and save five event-specific risk scenarios; falls back on deterministic templates if needed."""
    prompt = build_prompt(
        event_type=str(event.event_type),
        guest_count=int(event.guest_count),
        city=str(event.city),
        culture_style=str(event.theme_style or ""),
        special_requirements=str(event.special_requirements or ""),
    )

    try:
        output: RiskScenariosOutput = generate_structured(prompt, RiskScenariosOutput)
    except AIUnavailable:
        output = get_fallback_risk_scenarios(str(event.event_type))

    db.query(RiskScenario).filter(RiskScenario.event_id == event.id).delete(synchronize_session=False)
    rows: list[RiskScenario] = []
    for item in output.risks:
        row = _to_risk_scenario_model(event, item)
        db.add(row)
        rows.append(row)
    db.commit()
    for row in rows:
        db.refresh(row)
    return rows


def _task_impact_for(event: Event, scenario: RiskScenario) -> list[dict[str, Any]]:
    tasks = []
    for task in event.tasks:
        if task.category.lower() in {"risk", "operations", "venue", "catering", "vendor management", "planning"}:
            tasks.append(
                {
                    "id": task.id,
                    "title": task.title,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "status": task.status,
                }
            )
    return tasks[:5]


def simulate_risk(event: Event, risk: RiskScenario, db: Session) -> dict[str, Any]:
    """Apply a simulated risk in-memory without saving any database changes."""
    budget_items = db.query(BudgetItem).filter(BudgetItem.event_id == event.id).all()
    current_items: list[dict[str, float | int | str]] = [
        {"category": str(item.category), "amount": float(item.estimated_cost)} for item in budget_items
    ]
    before_total = (
        sum(float(item.get("amount", 0)) for item in current_items)
        if current_items
        else float(event.total_budget)
    )
    impact_pct = float(risk.budget_impact or 0.0)
    after_total = before_total * (1 + (impact_pct / 100.0))

    simulated_guest_count = int(event.guest_count)
    if "guest" in (risk.trigger_name or "").lower() or risk.scenario_type == "guest_surge":
        simulated_guest_count = int(round(int(event.guest_count) * 1.2))

    scenario_items = recalculate(current_items, total=after_total, guest_count=simulated_guest_count)
    affected_tasks = _task_impact_for(event, risk)
    return {
        "scenario_id": risk.id,
        "scenario_type": risk.scenario_type,
        "trigger_name": risk.trigger_name,
        "before_budget": {"total": round(before_total, 2), "items": current_items},
        "after_budget": {"total": round(after_total, 2), "items": scenario_items},
        "affected_tasks": affected_tasks,
        "fallback_steps": risk.mitigation_plan,
        "cost_impact_percent": impact_pct,
        "cost_impact_amount": round(abs(after_total - before_total), 2),
        "simulated_guest_count": simulated_guest_count,
    }
