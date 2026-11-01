"""Unit tests for Pydantic v2 schemas and validation edge cases."""

from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from app.schemas.common import Currency, EventType
from app.schemas.event import EventCreate, EventUpdate


def get_future_date(days: int = 30) -> date:
    """Helper to return a date strictly in the future."""
    return date.today() + timedelta(days=days)


def test_valid_event_create():
    """Verify that a valid payload succeeds with stripped strings."""
    event = EventCreate(
        title="  Rohan & Priya Wedding  ",
        event_type=EventType.WEDDING,
        target_date=get_future_date(90),
        guest_count=250,
        total_budget=500000.0,
        currency=Currency.INR,
        city="  Mumbai  ",
        theme_style="  Royal Heritage  ",
        special_requirements="  Jain meal options  ",
    )
    assert event.title == "Rohan & Priya Wedding"
    assert event.city == "Mumbai"
    assert event.theme_style == "Royal Heritage"
    assert event.special_requirements == "Jain meal options"
    assert event.currency == Currency.INR
    assert event.guest_count == 250
    assert event.total_budget == 500000.0


def test_schema_rejects_past_date():
    """Target date in the past must raise ValidationError."""
    past_date = date.today() - timedelta(days=5)
    with pytest.raises(ValidationError) as exc_info:
        EventCreate(
            title="Anniversary Gala",
            event_type=EventType.BIRTHDAY,
            target_date=past_date,
            guest_count=50,
            total_budget=5000.0,
            currency=Currency.USD,
            city="New York",
        )
    assert "Event date must be in the future" in str(exc_info.value)


def test_schema_rejects_today_date():
    """Target date of today must raise ValidationError (must be strictly in future)."""
    with pytest.raises(ValidationError) as exc_info:
        EventCreate(
            title="Same Day Party",
            event_type=EventType.BIRTHDAY,
            target_date=date.today(),
            guest_count=20,
            total_budget=1000.0,
            currency=Currency.USD,
            city="Boston",
        )
    assert "Event date must be in the future" in str(exc_info.value)


def test_schema_rejects_negative_budget():
    """Negative total_budget must raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        EventCreate(
            title="Negative Budget Gala",
            event_type=EventType.COMMUNITY,
            target_date=get_future_date(45),
            guest_count=100,
            total_budget=-500.0,
            currency=Currency.USD,
            city="Chicago",
        )
    assert "greater than 0" in str(exc_info.value)


def test_schema_rejects_zero_budget():
    """Zero total_budget must raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        EventCreate(
            title="Zero Budget Gala",
            event_type=EventType.COMMUNITY,
            target_date=get_future_date(45),
            guest_count=100,
            total_budget=0.0,
            currency=Currency.USD,
            city="Chicago",
        )
    assert "greater than 0" in str(exc_info.value)


def test_schema_rejects_guest_count_zero():
    """Guest count of 0 must raise ValidationError (ge=1)."""
    with pytest.raises(ValidationError) as exc_info:
        EventCreate(
            title="Zero Guests Event",
            event_type=EventType.BIRTHDAY,
            target_date=get_future_date(20),
            guest_count=0,
            total_budget=1500.0,
            currency=Currency.USD,
            city="Austin",
        )
    assert "greater than or equal to 1" in str(exc_info.value)


def test_schema_rejects_guest_count_5001():
    """Guest count of 5001 must raise ValidationError (le=5000)."""
    with pytest.raises(ValidationError) as exc_info:
        EventCreate(
            title="Overcrowded Festival",
            event_type=EventType.COMMUNITY,
            target_date=get_future_date(60),
            guest_count=5001,
            total_budget=100000.0,
            currency=Currency.USD,
            city="Dallas",
        )
    assert "less than or equal to 5000" in str(exc_info.value)


def test_schema_rejects_bad_currency():
    """Currencies not in allow-list (INR, USD, EUR, GBP, AED) must raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        EventCreate(
            title="Tokyo Meetup",
            event_type=EventType.COMMUNITY,
            target_date=get_future_date(30),
            guest_count=50,
            total_budget=3000.0,
            currency="JPY",  # Not in allow-list
            city="Tokyo",
        )
    assert "Input should be 'INR', 'USD', 'EUR', 'GBP' or 'AED'" in str(exc_info.value)


def test_schema_rejects_empty_string_title():
    """Empty or whitespace-only title must raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        EventCreate(
            title="     ",
            event_type=EventType.WEDDING,
            target_date=get_future_date(120),
            guest_count=100,
            total_budget=15000.0,
            currency=Currency.USD,
            city="San Francisco",
        )
    assert "Field cannot be empty or blank whitespace" in str(exc_info.value)


def test_schema_rejects_empty_string_city():
    """Empty or whitespace-only city must raise ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        EventCreate(
            title="Summer Solstice Party",
            event_type=EventType.COMMUNITY,
            target_date=get_future_date(60),
            guest_count=80,
            total_budget=3500.0,
            currency=Currency.EUR,
            city="   ",
        )
    assert "Field cannot be empty or blank whitespace" in str(exc_info.value)


def test_event_update_validation():
    """EventUpdate optional fields must adhere to the same strict validation if supplied."""
    # Blank string update rejected
    with pytest.raises(ValidationError):
        EventUpdate(title="   ")

    # Past date update rejected
    with pytest.raises(ValidationError):
        EventUpdate(target_date=date.today() - timedelta(days=1))

    # Valid partial update succeeds
    update = EventUpdate(guest_count=350, currency=Currency.AED)
    assert update.guest_count == 350
    assert update.currency == Currency.AED
    assert update.title is None
