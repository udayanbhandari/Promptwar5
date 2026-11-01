"""Build day-of run sheet timelines for event-specific schedules."""

from __future__ import annotations

from datetime import datetime, timedelta

_EVENT_RUNSHEET_TEMPLATES: dict[str, list[tuple[str, str, str, int]]] = {
    "wedding": [
        ("08:00", "09:00", "Hair & makeup setup", 60),
        ("09:00", "10:30", "Venue setup and floral staging", 90),
        ("10:30", "11:30", "Vendor check-in and equipment test", 60),
        ("11:30", "12:30", "Lunch and photographer prep", 60),
        ("13:30", "14:00", "First look and portrait session", 30),
        ("14:30", "15:00", "Family formal photos", 30),
        ("15:30", "16:00", "Wedding party lineup", 30),
        ("16:00", "16:30", "Ceremony buffer", 30),
        ("16:30", "17:30", "Ceremony", 60),
        ("17:30", "18:15", "Cocktail hour", 45),
        ("18:15", "19:00", "Guest seating and dinner start", 45),
        ("19:00", "20:30", "Dinner service", 90),
        ("20:30", "21:00", "Toasts & cake cutting", 30),
        ("21:00", "22:30", "Dancing and open floor", 90),
        ("22:30", "23:00", "Late-night snack and send-off buffer", 30),
    ],
    "birthday": [
        ("17:00", "18:00", "Host setup and decorating", 60),
        ("18:00", "18:30", "Cake, favors, and game station prep", 30),
        ("18:30", "19:00", "Guest arrival and check-in", 30),
        ("19:00", "19:30", "Welcome drinks and mingling", 30),
        ("19:30", "20:00", "Group games and photo booth", 30),
        ("20:00", "20:30", "Cake and toast", 30),
        ("20:30", "21:30", "Dance floor and arcade time", 60),
        ("21:30", "22:00", "Dessert and second round of drinks", 30),
        ("22:00", "22:30", "Final game / raffle", 30),
        ("22:30", "23:00", "Teardown and tab settlement", 30),
    ],
    "community": [
        ("06:00", "06:45", "Street closure and setup", 45),
        ("06:45", "07:15", "Volunteer briefing and station check", 30),
        ("07:15", "07:45", "Course readiness and check-in tables", 30),
        ("07:45", "08:15", "Participant arrival and hydration", 30),
        ("08:30", "09:00", "Race kickoff and warm-up", 30),
        ("09:00", "10:30", "Race execution and course support", 90),
        ("10:30", "11:00", "Water station and participant recovery", 30),
        ("11:00", "12:00", "Awards and community fair", 60),
        ("12:00", "12:45", "Lunch break and volunteer rotation", 45),
        ("12:45", "13:15", "Cleanup and debris sweep", 30),
        ("13:15", "14:00", "Road reopen and final inspection", 45),
    ],
}


def _parse_time(value: str) -> datetime:
    hour, minute = map(int, value.split(":"))
    base = datetime(2000, 1, 1)
    return base.replace(hour=hour, minute=minute)


def build_runsheet(event_type: str, start_time: str, guest_count: int) -> list[dict]:
    """Construct a day-of run sheet with realistic buffer windows per event type."""
    normalized = (event_type or "").strip().lower()
    if normalized not in _EVENT_RUNSHEET_TEMPLATES:
        raise ValueError(f"Unsupported event_type '{event_type}'.")

    base_start = _parse_time(start_time)
    schedule: list[dict] = []
    for start_str, _end_str, title, duration in _EVENT_RUNSHEET_TEMPLATES[normalized]:
        start_dt = base_start + timedelta(
            minutes=(_parse_time(start_str).hour * 60 + _parse_time(start_str).minute)
            - (_parse_time("00:00").hour * 60 + _parse_time("00:00").minute)
        )
        end_dt = start_dt + timedelta(minutes=duration)
        schedule.append(
            {
                "title": title,
                "start_time": start_dt.strftime("%H:%M"),
                "end_time": end_dt.strftime("%H:%M"),
                "duration_minutes": duration,
                "buffer": max(10, duration // 6),
                "guest_count": int(guest_count),
            }
        )

    return schedule
