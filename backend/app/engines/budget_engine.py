"""Deterministic budget allocation and rebalancing utilities."""

from __future__ import annotations

import math
from collections import OrderedDict
from collections.abc import Iterable, Mapping
from typing import Any


def _as_amount(value: Any) -> int:
    """Convert a monetary value to integer minor units (e.g. cents)."""
    if value is None:
        return 0
    return int(round(float(value)))


def _normalize_mapping(percentages: Mapping[str, Any]) -> OrderedDict[str, float]:
    normalized: OrderedDict[str, float] = OrderedDict()
    for key, value in percentages.items():
        name = str(key).strip()
        if not name or value is None:
            continue
        normalized[name] = float(value)
    return normalized


def _largest_remainder(total: int, weights: Mapping[str, float]) -> OrderedDict[str, int]:
    """Distribute total across weighted categories using the largest-remainder method."""
    if not weights:
        return OrderedDict()

    total_weight = sum(weights.values())
    if total_weight <= 0:
        raise ValueError("Category weights must sum to a positive value.")

    raw_amounts = OrderedDict()
    floors = OrderedDict()
    remainders = OrderedDict()

    for category, weight in weights.items():
        raw = total * (weight / total_weight)
        floor_amount = math.floor(raw)
        raw_amounts[category] = raw
        floors[category] = floor_amount
        remainders[category] = raw - floor_amount

    allocated = sum(floors.values())
    remaining = total - allocated
    if remaining > 0:
        ordered = sorted(
            weights.keys(),
            key=lambda category: (-remainders[category], weights[category], category),
        )
        for category in ordered[:remaining]:
            floors[category] += 1

    return floors


def _find_contingency(mapping: Mapping[str, float]) -> str | None:
    """Find the first category representing a contingency reserve."""
    return next(
        (key for key in mapping if "contingency" in key.lower() or "buffer" in key.lower()),
        None,
    )


def _allocate_with_contingency(total: int, weights: OrderedDict[str, float], contingency: str) -> OrderedDict[str, int]:
    """Allocate the non-contingency amount and add a ten-percent reserve."""
    reserved = min(int(round(total * 0.10)), total)
    remaining = OrderedDict((key, value) for key, value in weights.items() if key != contingency and value > 0)
    if not remaining:
        return OrderedDict({contingency: total})
    if sum(remaining.values()) <= 0:
        raise ValueError("Remaining category weights must be positive.")
    allocated = _largest_remainder(total - reserved, remaining)
    allocated[contingency] = reserved
    return allocated


def allocate(total: float | int, percentages: Mapping[str, float]) -> OrderedDict[str, int]:
    """Allocate a total budget across categories and reserve a mandatory 10% contingency."""
    if total is None:
        raise ValueError("Total budget must be provided.")

    total_minor = _as_amount(total)
    if total_minor < 0:
        raise ValueError("Total budget must be non-negative.")
    if not percentages:
        raise ValueError("At least one percentage is required.")

    normalized = _normalize_mapping(percentages)
    if not normalized:
        raise ValueError("At least one valid percentage is required.")

    contingency_name = _find_contingency(normalized)
    if contingency_name is not None:
        return _allocate_with_contingency(total_minor, normalized, contingency_name)

    reservation = int(round(total_minor * 0.10))
    remaining_total = total_minor - reservation
    weights = OrderedDict({name: value for name, value in normalized.items() if value > 0})
    if not weights:
        return OrderedDict({"Contingency": total_minor})

    if sum(weights.values()) <= 0:
        raise ValueError("Category weights must sum to a positive value.")

    allocated = _largest_remainder(remaining_total, weights)
    allocated["Contingency"] = reservation
    return OrderedDict((category, int(amount)) for category, amount in allocated.items())


def _coerce_item_dicts(
    current_items: Iterable[Mapping[str, Any]] | Mapping[str, Any] | None,
) -> list[OrderedDict[str, Any]]:
    if current_items is None:
        return []
    if isinstance(current_items, Mapping):
        items = [{"category": key, "amount": value} for key, value in current_items.items()]
        return [OrderedDict(item) for item in items]

    normalized: list[OrderedDict[str, Any]] = []
    for item in current_items:
        if isinstance(item, Mapping):
            category = item.get("category") or item.get("name") or item.get("title")
            amount = item.get("amount")
            if amount is None:
                amount = item.get("estimated_cost")
            if amount is None:
                amount = item.get("value")
            if category is None:
                continue
            entry = OrderedDict(item)
            entry["category"] = str(category)
            entry["amount"] = _as_amount(amount)
            normalized.append(entry)
    return normalized


def _normalize_locks(locked: Mapping[str, float | int] | None) -> OrderedDict[str, int]:
    """Normalize locked category amounts while preserving insertion order."""
    if not locked:
        return OrderedDict()
    return OrderedDict(
        (str(key).strip(), _as_amount(value))
        for key, value in locked.items()
        if key is not None and str(key).strip()
    )


def _remaining_items(
    items: Iterable[OrderedDict[str, Any]],
    locked: Mapping[str, int],
) -> list[OrderedDict[str, Any]]:
    """Return items whose categories are eligible for redistribution."""
    return [item for item in items if str(item.get("category", "")).strip() not in locked]


def _redistribution_weights(
    items: Iterable[OrderedDict[str, Any]],
    locked: Mapping[str, int],
) -> OrderedDict[str, float]:
    """Build positive weights for unlocked categories."""
    weights: OrderedDict[str, float] = OrderedDict()
    for item in items:
        category = str(item.get("category", "")).strip()
        amount = max(_as_amount(item.get("amount", 0)), 0)
        weights[category] = amount if amount > 0 else 1.0
    if not weights and locked:
        weights.update((category, 1.0) for category in locked)
    return weights


def _build_recalculated_items(
    items: Iterable[OrderedDict[str, Any]],
    locked: Mapping[str, int],
    allocated: Mapping[str, int],
) -> OrderedDict[str, OrderedDict[str, Any]]:
    """Apply locked and redistributed amounts to the original item shape."""
    result: OrderedDict[str, OrderedDict[str, Any]] = OrderedDict()
    seen: set[str] = set()
    for item in items:
        category = str(item.get("category", "")).strip()
        amount = locked.get(category, allocated.get(category, 0))
        updated = OrderedDict(item)
        updated["category"] = category
        updated["amount"] = int(amount)
        result[category] = updated
        seen.add(category)
    for category, amount in locked.items():
        if category not in result:
            result[category] = OrderedDict({"category": category, "amount": int(amount)})
    for category, amount in allocated.items():
        if category not in seen:
            result[category] = OrderedDict({"category": category, "amount": int(amount)})
    return result


def _correct_total(result: OrderedDict[str, OrderedDict[str, Any]], total: int) -> None:
    """Correct a final rounding residue on the last result item."""
    current = sum(int(item.get("amount", 0)) for item in result.values())
    if result and current != total:
        last_key = next(reversed(result))
        result[last_key]["amount"] = int(result[last_key].get("amount", 0)) + total - current


def recalculate(
    current_items: Iterable[Mapping[str, Any]] | Mapping[str, Any] | None,
    total: float | int | None = None,
    locked: Mapping[str, float | int] | None = None,
    guest_count: int | None = None,
) -> list[OrderedDict[str, Any]]:
    """Rebalance a list of budget items while keeping locked categories fixed."""
    items = _coerce_item_dicts(current_items)
    if not items and (locked is None or not locked):
        return []

    if total is None:
        total = sum(int(item.get("amount", 0)) for item in items)

    total_minor = _as_amount(total)
    fixed_lock = _normalize_locks(locked)
    if sum(fixed_lock.values()) > total_minor:
        raise ValueError("Locked category amounts exceed the total budget.")

    unlocked_items = _remaining_items(items, fixed_lock)
    remaining_total = total_minor - sum(fixed_lock.values())
    if remaining_total < 0:
        raise ValueError("Remaining budget after locks cannot be negative.")

    if not unlocked_items and not fixed_lock:
        return []

    unlocked_weights = _redistribution_weights(unlocked_items, fixed_lock)
    if sum(unlocked_weights.values()) <= 0:
        equal_amount = remaining_total // max(1, len(unlocked_weights))
        residue = remaining_total % max(1, len(unlocked_weights))
        redistributed: OrderedDict[str, float] = OrderedDict()
        for idx, category in enumerate(unlocked_weights.keys()):
            redistributed[category] = float(equal_amount + (1 if idx < residue else 0))
        unlocked_weights = redistributed

    allocated = _largest_remainder(remaining_total, unlocked_weights)
    result = _build_recalculated_items(items, fixed_lock, allocated)
    _correct_total(result, total_minor)

    return list(result.values())


def warnings(items: Iterable[Mapping[str, Any]] | Mapping[str, Any], guest_count: int | None) -> list[str]:
    """Return human-readable warnings about likely budget stress points."""
    item_map = OrderedDict()
    for item in _coerce_item_dicts(items):
        category = str(item.get("category", "")).strip()
        if not category:
            continue
        item_map[category] = int(item.get("amount", 0))

    if not item_map:
        return []

    total = sum(item_map.values())
    flags: list[str] = []

    catering_names = [
        category
        for category in item_map
        if "catering" in category.lower() or "food" in category.lower() or "bar" in category.lower()
    ]
    if guest_count and guest_count > 0 and catering_names:
        catering_total = sum(item_map[name] for name in catering_names)
        per_guest_minor = catering_total / guest_count
        if per_guest_minor < 4000:
            flags.append(
                "Catering spend per guest is below the recommended floor; "
                "consider increasing food and bar coverage for this guest count."
            )

    contingency_names = [
        category for category in item_map if "contingency" in category.lower() or "buffer" in category.lower()
    ]
    if contingency_names:
        contingency_total = sum(item_map[name] for name in contingency_names)
        if total > 0 and (contingency_total / total) < 0.05:
            flags.append("Contingency is below 5% of the total budget; a larger reserve is recommended.")

    return flags
