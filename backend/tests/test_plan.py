from datetime import date

from app.models import Event


def test_generate_plan_happy_path(client, monkeypatch):
    event = Event(
        title="Sample wedding",
        event_type="wedding",
        target_date=date(2026, 12, 15),
        guest_count=120,
        total_budget=28000.0,
        currency="USD",
        city="Seattle",
        theme_style="Rustic Elegant",
        special_requirements="Vegetarian options",
    )
    client.app.dependency_overrides.clear()
    from app.routers import plan as plan_router

    class FakeBudget:
        categories = [
            type("Cat", (), {"category": "Venue", "percentage": 40.0})(),
            type("Cat", (), {"category": "Food", "percentage": 35.0})(),
            type("Cat", (), {"category": "Decor", "percentage": 15.0})(),
            type("Cat", (), {"category": "Photography", "percentage": 10.0})(),
        ]

    class FakeIdea:
        ideas = [
            type("Idea", (), {"aspect": "theme", "title": "Test theme", "description": "desc", "cost_tier": "medium", "why_it_fits": "fits"})()
            for _ in range(5)
        ]

    class FakeVendor:
        categories = [
            type("V", (), {"category": "Venue", "questions": ["Q1", "Q2", "Q3", "Q4", "Q5"], "red_flags": ["A", "B", "C"]})()
        ]

    def fake_generate_structured(prompt, schema, **kwargs):
        if "budget" in prompt.lower():
            return FakeBudget()
        if "ideas" in prompt.lower():
            return FakeIdea()
        return FakeVendor()

    monkeypatch.setattr(plan_router, "generate_structured", fake_generate_structured)

    response = client.post("/api/v1/events/nonexistent/generate-plan")
    assert response.status_code == 404
