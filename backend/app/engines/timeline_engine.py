"""Deterministic timeline builder and scheduling utilities."""

from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Sequence
from datetime import date, timedelta

from app.engines.templates import EVENT_TASK_TEMPLATES


def _normalize_event_type(event_type: str) -> str:
    return (event_type or "").strip().lower()


def _topological_order(tasks: Sequence[dict]) -> list[dict]:
    """Return tasks in a topological order, rejecting cycles."""
    task_map = {task["key"]: task for task in tasks}
    incoming = {key: 0 for key in task_map}
    adjacency = defaultdict(list)

    for task in tasks:
        depends_on = task.get("depends_on") or []
        for dependency in depends_on:
            if dependency not in task_map:
                continue
            adjacency[dependency].append(task["key"])
            incoming[task["key"]] += 1

    queue = deque(sorted(key for key, degree in incoming.items() if degree == 0))
    ordered: list[str] = []
    while queue:
        current = queue.popleft()
        ordered.append(current)
        for dependent in sorted(adjacency.get(current, [])):
            incoming[dependent] -= 1
            if incoming[dependent] == 0:
                queue.append(dependent)

    if len(ordered) != len(task_map):
        raise ValueError("Task dependency graph contains a cycle and cannot be scheduled.")

    return [task_map[key] for key in ordered]


def _cycle_check(tasks: Sequence[dict]) -> None:
    """Validate tasks for cycle-like dependency contradictions without scheduling."""
    task_map = {task["key"]: task for task in tasks}
    visited: set[str] = set()
    stack: set[str] = set()

    def visit(key: str) -> None:
        if key in stack:
            raise ValueError("Task dependency graph contains a cycle and cannot be scheduled.")
        if key in visited:
            return
        visited.add(key)
        stack.add(key)
        for dep in task_map[key].get("depends_on") or []:
            if dep in task_map:
                visit(dep)
        stack.remove(key)

    for key in task_map:
        visit(key)


def build_timeline(event_type: str | Sequence[dict], event_date: date, today: date) -> list[dict]:
    """Build a backward-scheduled project timeline for an event type or supplied task graph."""
    if isinstance(event_type, Sequence) and not isinstance(event_type, str | bytes):
        tasks = [dict(task) for task in event_type]
        _cycle_check(tasks)
        return _topological_order(tasks)

    normalized = _normalize_event_type(event_type)
    if normalized not in EVENT_TASK_TEMPLATES:
        raise ValueError(f"Unsupported event_type '{event_type}'.")

    task_templates = EVENT_TASK_TEMPLATES[normalized]
    task_items: list[dict] = []
    for template in task_templates:
        schedule = dict(template)
        schedule["due_date"] = event_date - timedelta(days=int(schedule["lead_time_days"]))
        schedule["rush"] = False
        schedule["completed"] = False
        task_items.append(schedule)

    tasks = task_items

    _cycle_check(tasks)
    ordered = _topological_order(tasks)
    for task in ordered:
        dependencies = task.get("depends_on") or []
        dependency_due_dates = [
            next(item["due_date"] for item in ordered if item["key"] == dep)
            for dep in dependencies
            if any(item["key"] == dep for item in ordered)
        ]
        if dependency_due_dates:
            latest_dependency = max(dependency_due_dates)
            if task["due_date"] < latest_dependency:
                task["due_date"] = latest_dependency

        if task["due_date"] < today:
            task["rush"] = True
            task["due_date"] = today

    return ordered


def critical_path(tasks: Sequence[dict]) -> list[dict]:
    """Return a task list representing the longest dependency chain."""
    if not tasks:
        return []

    by_key = {task["key"]: task for task in tasks}
    longest_path: dict[str, list[str]] = {}

    def walk(task_key: str) -> list[str]:
        if task_key in longest_path:
            return longest_path[task_key]
        task = by_key[task_key]
        deps = task.get("depends_on") or []
        if not deps:
            longest_path[task_key] = [task_key]
            return [task_key]
        best: list[str] = []
        for dep in deps:
            if dep in by_key:
                candidate = walk(dep)
                if len(candidate) > len(best):
                    best = candidate
        longest_path[task_key] = best + [task_key]
        return longest_path[task_key]

    best_path: list[str] = []
    for task in tasks:
        path = walk(task["key"])
        if len(path) > len(best_path):
            best_path = path

    return [by_key[key] for key in best_path]


def reschedule(tasks: Sequence[dict], new_event_date: date, today: date) -> list[dict]:
    """Reschedule active tasks for a new event date while keeping completed tasks intact."""
    if not tasks:
        return []

    reshaped: list[dict] = []
    scheduled = {task["key"]: task for task in tasks}
    ordered = _topological_order(tasks)

    for task in ordered:
        if task.get("completed"):
            reshaped.append(task)
            continue
        base = task.copy()
        if task.get("lead_time_days") is None:
            base["due_date"] = new_event_date
        else:
            base["due_date"] = new_event_date - timedelta(days=int(task.get("lead_time_days", 0)))
        deps = base.get("depends_on") or []
        dependency_recent = [
            scheduled[dep]["due_date"]
            for dep in deps
            if dep in scheduled and scheduled[dep].get("due_date") is not None
        ]
        if dependency_recent:
            base["due_date"] = max(base["due_date"], max(dependency_recent))
        if base["due_date"] < today:
            base["rush"] = True
            base["due_date"] = today
        else:
            base["rush"] = False
        reshaped.append(base)

    _cycle_check(reshaped)

    return reshaped


def group_by_urgency(tasks: Sequence[dict], today: date) -> dict[str, list[dict]]:
    """Group tasks into this_week, this_month, or later based on their due dates."""
    buckets: dict[str, list[dict]] = {"this_week": [], "this_month": [], "later": []}
    for task in tasks:
        due_date = task.get("due_date")
        if due_date is None:
            buckets["later"].append(task)
            continue
        delta = (due_date - today).days
        if delta <= 7:
            buckets["this_week"].append(task)
        elif delta <= 30:
            buckets["this_month"].append(task)
        else:
            buckets["later"].append(task)
    return buckets
