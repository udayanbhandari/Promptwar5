from datetime import date

import pytest

from app.engines.timeline_engine import build_timeline, critical_path, group_by_urgency, reschedule


def test_build_timeline_orders_dependencies():
    tasks = build_timeline("wedding", date(2026, 12, 15), date(2026, 10, 1))
    assert tasks
    keys = [task["key"] for task in tasks]
    for task in tasks:
        for dep in task.get("depends_on") or []:
            assert keys.index(dep) < keys.index(task["key"])


def test_build_timeline_marks_rush_less_than_two_weeks_out():
    tasks = build_timeline("birthday", date(2026, 10, 10), date(2026, 10, 1))
    assert any(task.get("rush") for task in tasks)


def test_cycle_rejection():
    tasks = [
        {"key": "a", "title": "A", "category": "x", "lead_time_days": 1, "depends_on": ["b"], "is_critical": True},
        {"key": "b", "title": "B", "category": "x", "lead_time_days": 2, "depends_on": ["a"], "is_critical": True},
    ]
    with pytest.raises(ValueError, match="cycle"):
        build_timeline(tasks, date(2026, 12, 15), date(2026, 10, 1))


def test_reschedule_keeps_completed_tasks():
    tasks = [
        {"key": "a", "title": "A", "category": "x", "lead_time_days": 10, "depends_on": [], "is_critical": True, "completed": True, "due_date": date(2026, 11, 1)},
        {"key": "b", "title": "B", "category": "x", "lead_time_days": 7, "depends_on": ["a"], "is_critical": True, "completed": False, "due_date": date(2026, 11, 5)},
    ]
    updated = reschedule(tasks, date(2026, 12, 15), date(2026, 10, 1))
    assert any(task["key"] == "a" and task["completed"] for task in updated)


def test_group_by_urgency():
    tasks = [
        {"key": "now", "title": "Now", "category": "x", "due_date": date(2026, 10, 5)},
        {"key": "soon", "title": "Soon", "category": "x", "due_date": date(2026, 10, 15)},
        {"key": "later", "title": "Later", "category": "x", "due_date": date(2026, 11, 1)},
    ]
    grouped = group_by_urgency(tasks, date(2026, 10, 1))
    assert grouped["this_week"]
    assert grouped["this_month"]
    assert grouped["later"]
