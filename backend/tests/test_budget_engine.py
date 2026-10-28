from collections import OrderedDict

import pytest

from app.engines.budget_engine import allocate, recalculate, warnings


@pytest.mark.parametrize(
    "total, percentages",
    [
        (1000, {"Venue": 40, "Catering": 35, "Decor": 15, "Music": 10}),
        (25000, {"Venue": 50, "Food": 30, "Decor": 10, "Music": 10}),
        (1, {"Venue": 50, "Catering": 30, "Decor": 20}),
    ],
)
def test_allocate_exact_sum(total, percentages):
    result = allocate(total, percentages)
    assert sum(result.values()) == total
    assert set(result.keys()) == set(percentages) | {"Contingency"}
    if total >= 10:
        assert result["Contingency"] > 0


def test_allocate_handles_locked_total():
    total = 10000
    result = allocate(total, {"Venue": 60, "Food": 25, "Decor": 15})
    assert sum(result.values()) == total
    assert result["Contingency"] == 1000


def test_recalculate_maintains_total_and_respects_locks():
    items = [
        {"category": "Venue", "amount": 5000},
        {"category": "Catering", "amount": 3000},
        {"category": "Decor", "amount": 2000},
    ]
    updated = recalculate(items, total=10000, locked={"Venue": 4000})
    assert sum(item["amount"] for item in updated) == 10000
    assert next(item for item in updated if item["category"] == "Venue")["amount"] == 4000


def test_recalculate_raises_if_locks_exceed_total():
    items = [{"category": "Venue", "amount": 5000}, {"category": "Catering", "amount": 3000}]
    with pytest.raises(ValueError, match="exceed"):
        recalculate(items, total=7000, locked={"Venue": 5000, "Catering": 4000})


def test_warnings_for_low_catering_and_low_contingency():
    items = [
        {"category": "Venue", "amount": 8000},
        {"category": "Food", "amount": 2500},
        {"category": "Contingency", "amount": 200},
    ]
    output = warnings(items, guest_count=50)
    assert any("Catering" in msg for msg in output)
    assert any("Contingency" in msg for msg in output)
