"""Deterministic budget allocation and rebalancing utilities."""

from __future__ import annotations

import math
from collections import OrderedDict
from typing import Any, Iterable, List, Mapping


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

    contingency_name = None
    for key in list(normalized.keys()):
        if "contingency" in key.lower() or "buffer" in key.lower():
            contingency_name = key
            break

    if contingency_name is not None:
        contingency_percent = normalized.pop(contingency_name)
        logical_contingency = total_minor * 0.10
        reserved = int(round(logical_contingency))
        if reserved > total_minor:
            reserved = total_minor
        remaining_total = total_minor - reserved
        remaining_weights = OrderedDict({k: v for k, v in normalized.items() if v > 0})
        if not remaining_weights:
            return OrderedDict({contingency_name: total_minor})
        if sum(remaining_weights.values()) <= 0:
            raise ValueError("Remaining category weights must be positive.")
        scaled = _largest_remainder(remaining_total, remaining_weights)
        scaled[contingency_name] = reserved
        return OrderedDict((k, int(v)) for k, v in scaled.items())

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


def _coerce_item_dicts(current_items: Iterable[Mapping[str, Any]] | Mapping[str, Any] | None) -> List[OrderedDict[str, Any]]:
    if current_items is None:
        return []
    if isinstance(current_items, Mapping):
        items = [{"category": key, "amount": value} for key, value in current_items.items()]
        return [OrderedDict(item) for item in items]

    normalized: List[OrderedDict[str, Any]] = []
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


def recalculate(
    current_items: Iterable[Mapping[str, Any]] | Mapping[str, Any] | None,
    total: float | int | None = None,
    locked: Mapping[str, float | int] | None = None,
    guest_count: int | None = None,
) -> List[OrderedDict[str, Any]]:
    """Rebalance a list of budget items while keeping locked categories fixed."""
    items = _coerce_item_dicts(current_items)
    if not items and (locked is None or not locked):
        return []

    if total is None:
        total = sum(int(item.get("amount", 0)) for item in items)

    total_minor = _as_amount(total)
    fixed_lock = {} if locked is None else {str(key).strip(): _as_amount(value) for key, value in locked.items() if key is not None and str(key).strip()}
    if sum(fixed_lock.values()) > total_minor:
        raise ValueError("Locked category amounts exceed the total budget.")

    locked_by_name = OrderedDict((category, amount) for category, amount in fixed_lock.items())
    unlocked_items: List[OrderedDict[str, Any]] = []
    for item in items:
        category = str(item.get("category", "")).strip()
        if category in locked_by_name:
            continue
        unlocked_items.append(item)

    remaining_total = total_minor - sum(locked_by_name.values())
    if remaining_total < 0:
        raise ValueError("Remaining budget after locks cannot be negative.")

    if not unlocked_items and not locked_by_name:
        return []

    unlocked_weights: OrderedDict[str, float] = OrderedDict()
    for item in unlocked_items:
        category = str(item.get("category", "")).strip()
        current_amount = max(_as_amount(item.get("amount", 0)), 0)
        unlocked_weights[category] = current_amount if current_amount > 0 else 1.0

    if not unlocked_weights and locked_by_name:
        unlocked_weights = OrderedDict((category, 1.0) for category in [str(name) for name in locked_by_name.keys()])

    if sum(unlocked_weights.values()) <= 0:
        equal_amount = remaining_total // max(1, len(unlocked_weights))
        residue = remaining_total % max(1, len(unlocked_weights))
        redistributed = OrderedDict()
        for idx, category in enumerate(unlocked_weights.keys()):
            redistributed[category] = equal_amount + (1 if idx < residue else 0)
        unlocked_weights = redistributed

    allocated = _largest_remainder(remaining_total, unlocked_weights)
    result: OrderedDict[str, OrderedDict[str, Any]] = OrderedDict()
    seen: set[str] = set()

    for item in items:
        category = str(item.get("category", "")).strip()
        if category in locked_by_name:
            amount = locked_by_name[category]
        elif category in allocated:
            amount = allocated[category]
        else:
            amount = 0
        seen.add(category)
        updated = OrderedDict(item)
        updated["category"] = category
        updated["amount"] = int(amount)
        result[category] = updated

    for category, amount in locked_by_name.items():
        if category not in result:
            result[category] = OrderedDict({"category": category, "amount": int(amount)})

    for category, amount in allocated.items():
        if category not in seen:
            result[category] = OrderedDict({"category": category, "amount": int(amount)})

    if sum(int(item.get("amount", 0)) for item in result.values()) != total_minor:
        diff = total_minor - sum(int(item.get("amount", 0)) for item in result.values())
        if result:
            last_key = next(reversed(result))
            result[last_key]["amount"] = int(result[last_key].get("amount", 0)) + diff

    return list(result.values())


def warnings(items: Iterable[Mapping[str, Any]] | Mapping[str, Any], guest_count: int | None) -> List[str]:
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
    flags: List[str] = []

    catering_names = [
        category for category in item_map if "catering" in category.lower() or "food" in category.lower() or "bar" in category.lower()
    ]
    if guest_count and guest_count > 0 and catering_names:
        catering_total = sum(item_map[name] for name in catering_names)
        per_guest_minor = catering_total / guest_count
        if per_guest_minor < 4000:
            flags.append(
                "Catering spend per guest is below the recommended floor; consider increasing food and bar coverage for this guest count."
            )

    contingency_names = [category for category in item_map if "contingency" in category.lower() or "buffer" in category.lower()]
    if contingency_names:
        contingency_total = sum(item_map[name] for name in contingency_names)
        if total > 0 and (contingency_total / total) < 0.05:
            flags.append("Contingency is below 5% of the total budget; a larger reserve is recommended.")

    return flags
