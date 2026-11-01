"""Test suite for Event CRUD operations and endpoints."""

from datetime import date, timedelta

from fastapi import status


def get_future_date_str(days: int = 60) -> str:
    """Helper to return an ISO date string in the future."""
    return (date.today() + timedelta(days=days)).isoformat()


def test_health_check(client):
    """Verify /health returns 200 OK and expected structure."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"


def test_create_event_success(client):
    """Test creating an event with valid payload."""
    payload = {
        "title": "Sarah & Alex Wedding",
        "event_type": "wedding",
        "target_date": get_future_date_str(180),
        "guest_count": 120,
        "total_budget": 25000.0,
        "currency": "USD",
        "city": "Seattle, WA",
        "theme_style": "Rustic Elegant",
        "special_requirements": "Wheelchair ramp needed for ceremony stage",
    }
    response = client.post("/api/v1/events", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert "id" in data
    assert data["title"] == "Sarah & Alex Wedding"
    assert data["event_type"] == "wedding"
    assert data["guest_count"] == 120
    assert data["total_budget"] == 25000.0
    assert data["currency"] == "USD"
    assert data["city"] == "Seattle, WA"
    assert data["created_at"] is not None


def test_get_event_by_id(client):
    """Test retrieving an event and its detailed relations."""
    payload = {
        "title": "Leo's 30th Sci-Fi Birthday",
        "event_type": "birthday",
        "target_date": get_future_date_str(30),
        "guest_count": 40,
        "total_budget": 2200.0,
        "currency": "USD",
        "city": "Austin, TX",
        "theme_style": "Cyberpunk Neon",
        "special_requirements": "Vegan cake requested",
    }
    create_res = client.post("/api/v1/events", json=payload)
    event_id = create_res.json()["id"]

    get_res = client.get(f"/api/v1/events/{event_id}")
    assert get_res.status_code == status.HTTP_200_OK
    event_data = get_res.json()
    assert event_data["id"] == event_id
    assert event_data["title"] == "Leo's 30th Sci-Fi Birthday"
    assert event_data["budget_items"] == []
    assert event_data["tasks"] == []
    assert event_data["vendors"] == []
    assert event_data["risk_scenarios"] == []


def test_list_events(client):
    """Test listing multiple created events."""
    payload1 = {
        "title": "Event A",
        "event_type": "birthday",
        "target_date": get_future_date_str(10),
        "guest_count": 25,
        "total_budget": 1000.0,
        "currency": "USD",
        "city": "Denver, CO",
    }
    payload2 = {
        "title": "Event B",
        "event_type": "community",
        "target_date": get_future_date_str(20),
        "guest_count": 300,
        "total_budget": 5000.0,
        "currency": "USD",
        "city": "Denver, CO",
    }
    client.post("/api/v1/events", json=payload1)
    client.post("/api/v1/events", json=payload2)

    list_res = client.get("/api/v1/events")
    assert list_res.status_code == status.HTTP_200_OK
    items = list_res.json()
    assert len(items) == 2


def test_patch_event(client):
    """Test partial update on an event."""
    payload = {
        "title": "Initial Title",
        "event_type": "wedding",
        "target_date": get_future_date_str(90),
        "guest_count": 80,
        "total_budget": 15000.0,
        "currency": "USD",
        "city": "Chicago, IL",
    }
    create_res = client.post("/api/v1/events", json=payload)
    event_id = create_res.json()["id"]

    patch_payload = {
        "title": "Updated Gala Title",
        "guest_count": 95,
        "total_budget": 18000.0,
    }
    patch_res = client.patch(f"/api/v1/events/{event_id}", json=patch_payload)
    assert patch_res.status_code == status.HTTP_200_OK
    updated_data = patch_res.json()
    assert updated_data["title"] == "Updated Gala Title"
    assert updated_data["guest_count"] == 95
    assert updated_data["total_budget"] == 18000.0
    # Unchanged fields remain intact
    assert updated_data["city"] == "Chicago, IL"


def test_delete_event(client):
    """Test deleting an event and confirming 404 on subsequent get."""
    payload = {
        "title": "Temporary Event",
        "event_type": "community",
        "target_date": get_future_date_str(15),
        "guest_count": 50,
        "total_budget": 1200.0,
        "currency": "USD",
        "city": "Miami, FL",
    }
    create_res = client.post("/api/v1/events", json=payload)
    event_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/v1/events/{event_id}")
    assert delete_res.status_code == status.HTTP_200_OK
    assert delete_res.json()["message"] == "Event deleted successfully"

    get_res = client.get(f"/api/v1/events/{event_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND
    assert get_res.json()["error"] == "not_found"
