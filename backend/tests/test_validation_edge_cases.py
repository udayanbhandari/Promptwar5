"""Test suite for strict validation edge cases and error envelopes."""

from datetime import date, timedelta
from fastapi import status


def get_future_date_str(days: int = 45) -> str:
    """Helper for future ISO date string."""
    return (date.today() + timedelta(days=days)).isoformat()


def test_reject_past_date(client):
    """Validation test: target_date in the past must return 422."""
    payload = {
        "title": "Old Event",
        "event_type": "birthday",
        "target_date": "2020-01-01",
        "guest_count": 50,
        "total_budget": 1500.0,
        "currency": "USD",
        "city": "Boston, MA",
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["error"] == "validation_error"
    assert "target_date" in str(data["details"])


def test_reject_negative_budget(client):
    """Validation test: total_budget <= 0 must return 422."""
    payload = {
        "title": "Negative Budget Event",
        "event_type": "wedding",
        "target_date": get_future_date_str(60),
        "guest_count": 100,
        "total_budget": -500.0,
        "currency": "USD",
        "city": "Dallas, TX",
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["error"] == "validation_error"
    assert "total_budget" in str(data["details"])


def test_reject_zero_budget(client):
    """Validation test: total_budget == 0 must return 422."""
    payload = {
        "title": "Free Event",
        "event_type": "community",
        "target_date": get_future_date_str(60),
        "guest_count": 50,
        "total_budget": 0.0,
        "currency": "USD",
        "city": "Portland, OR",
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["error"] == "validation_error"


def test_reject_zero_guest_count(client):
    """Validation test: guest_count < 1 must return 422."""
    payload = {
        "title": "Empty Event",
        "event_type": "birthday",
        "target_date": get_future_date_str(30),
        "guest_count": 0,
        "total_budget": 1000.0,
        "currency": "USD",
        "city": "Phoenix, AZ",
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["error"] == "validation_error"
    assert "guest_count" in str(data["details"])


def test_reject_excessive_guest_count(client):
    """Validation test: guest_count > 5000 must return 422."""
    payload = {
        "title": "Mega Festival",
        "event_type": "community",
        "target_date": get_future_date_str(90),
        "guest_count": 5001,
        "total_budget": 50000.0,
        "currency": "USD",
        "city": "Atlanta, GA",
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["error"] == "validation_error"
    assert "guest_count" in str(data["details"])


def test_reject_invalid_currency(client):
    """Validation test: currency not in allow-list must return 422."""
    payload = {
        "title": "Crypto Party",
        "event_type": "birthday",
        "target_date": get_future_date_str(30),
        "guest_count": 25,
        "total_budget": 2000.0,
        "currency": "BITCOIN",
        "city": "Miami, FL",
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["error"] == "validation_error"
    assert "currency" in str(data["details"])


def test_reject_invalid_event_type(client):
    """Validation test: invalid event_type enum must return 422."""
    payload = {
        "title": "Conference 2026",
        "event_type": "corporate_expo",
        "target_date": get_future_date_str(30),
        "guest_count": 50,
        "total_budget": 3000.0,
        "currency": "USD",
        "city": "San Jose, CA",
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["error"] == "validation_error"


def test_not_found_error_format(client):
    """Error envelope test: 404 must return standardized JSON."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/events/{fake_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["error"] == "not_found"
    assert data["message"] == "Event not found"
    assert data["details"] is None


def test_input_sanitization(client):
    """Sanitization test: HTML and extraneous whitespace stripped."""
    payload = {
        "title": "<script>alert('xss')</script> Summer   Gala   ",
        "event_type": "community",
        "target_date": get_future_date_str(40),
        "guest_count": 100,
        "total_budget": 4000.0,
        "currency": "USD",
        "city": "  <b>San Francisco</b>, CA   ",
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Summer Gala"
    assert data["city"] == "San Francisco, CA"
