"""Task templates for event timelines."""

from __future__ import annotations

from typing import Dict, List


EVENT_TASK_TEMPLATES: Dict[str, List[dict]] = {
    "wedding": [
        {"key": "vendor-booking", "title": "Book venue and ceremony space", "category": "Venue", "lead_time_days": 180, "depends_on": [], "is_critical": True},
        {"key": "guest-list", "title": "Finalize guest list and RSVP workflow", "category": "Planning", "lead_time_days": 150, "depends_on": ["vendor-booking"], "is_critical": True},
        {"key": "budget-confirm", "title": "Lock core budget and contingency", "category": "Budget", "lead_time_days": 150, "depends_on": ["vendor-booking"], "is_critical": True},
        {"key": "catering-shortlist", "title": "Shortlist catering and bar options", "category": "Catering", "lead_time_days": 120, "depends_on": ["guest-list"], "is_critical": True},
        {"key": "photography-book", "title": "Book photography and video team", "category": "Photography", "lead_time_days": 120, "depends_on": ["budget-confirm"], "is_critical": True},
        {"key": "floral-design", "title": "Choose floral and styling direction", "category": "Decor", "lead_time_days": 100, "depends_on": ["budget-confirm"], "is_critical": False},
        {"key": "music-booking", "title": "Confirm DJ or live music package", "category": "Entertainment", "lead_time_days": 90, "depends_on": ["budget-confirm"], "is_critical": True},
        {"key": "save-date", "title": "Send save-the-dates and invitations", "category": "Guest Communication", "lead_time_days": 90, "depends_on": ["guest-list"], "is_critical": True},
        {"key": "dress-fitting", "title": "Arrange dress and attire fitting", "category": "Attire", "lead_time_days": 75, "depends_on": ["save-date"], "is_critical": False},
        {"key": "menu-final", "title": "Finalize menu and dietary plan", "category": "Catering", "lead_time_days": 45, "depends_on": ["catering-shortlist"], "is_critical": True},
        {"key": "ceremony-plan", "title": "Lock ceremony flow and officiant details", "category": "Ceremony", "lead_time_days": 45, "depends_on": ["vendor-booking"], "is_critical": True},
        {"key": "seating-layout", "title": "Finalize seating chart and floor plan", "category": "Operations", "lead_time_days": 30, "depends_on": ["guest-list", "menu-final"], "is_critical": True},
        {"key": "vendor-confirm", "title": "Confirm all vendors and contracts", "category": "Vendor Management", "lead_time_days": 21, "depends_on": ["photography-book", "music-booking", "floral-design"], "is_critical": True},
        {"key": "timeline-draft", "title": "Draft wedding day timeline", "category": "Operations", "lead_time_days": 14, "depends_on": ["vendor-confirm", "ceremony-plan"], "is_critical": True},
        {"key": "rehearsal", "title": "Run rehearsal and final walk-through", "category": "Ceremony", "lead_time_days": 7, "depends_on": ["timeline-draft"], "is_critical": True},
        {"key": "weather-check", "title": "Review weather backup plan", "category": "Risk", "lead_time_days": 3, "depends_on": ["timeline-draft"], "is_critical": True},
        {"key": "day-of-setup", "title": "Set up ceremony and reception area", "category": "Operations", "lead_time_days": 1, "depends_on": ["vendor-confirm"], "is_critical": True},
        {"key": "event-day", "title": "Execute wedding day", "category": "Event Day", "lead_time_days": 0, "depends_on": ["rehearsal", "weather-check", "day-of-setup"], "is_critical": True},
    ],
    "birthday": [
        {"key": "venue-book", "title": "Book venue or private room", "category": "Venue", "lead_time_days": 30, "depends_on": [], "is_critical": True},
        {"key": "guest-count", "title": "Confirm guest list and RSVPs", "category": "Planning", "lead_time_days": 24, "depends_on": ["venue-book"], "is_critical": True},
        {"key": "theme-lock", "title": "Lock theme and decor direction", "category": "Decor", "lead_time_days": 21, "depends_on": ["venue-book"], "is_critical": False},
        {"key": "music-plan", "title": "Arrange playlists or DJ", "category": "Entertainment", "lead_time_days": 18, "depends_on": ["theme-lock"], "is_critical": True},
        {"key": "food-book", "title": "Book food and cake vendor", "category": "Catering", "lead_time_days": 18, "depends_on": ["guest-count"], "is_critical": True},
        {"key": "staging", "title": "Plan activity area and photo backdrop", "category": "Operations", "lead_time_days": 14, "depends_on": ["theme-lock"], "is_critical": False},
        {"key": "invite-send", "title": "Send invitations and reminders", "category": "Guest Communication", "lead_time_days": 14, "depends_on": ["guest-count"], "is_critical": True},
        {"key": "supplies", "title": "Order balloons, favors, and supplies", "category": "Supplies", "lead_time_days": 10, "depends_on": ["theme-lock"], "is_critical": False},
        {"key": "recipe-check", "title": "Confirm dietary requirements and cake details", "category": "Catering", "lead_time_days": 7, "depends_on": ["food-book"], "is_critical": True},
        {"key": "setup-plan", "title": "Finalize room layout and setup checklist", "category": "Operations", "lead_time_days": 5, "depends_on": ["venue-book", "staging"], "is_critical": True},
        {"key": "music-test", "title": "Test sound system and playlist flow", "category": "Entertainment", "lead_time_days": 2, "depends_on": ["music-plan"], "is_critical": True},
        {"key": "host-checkin", "title": "Review event day run-of-show with host", "category": "Planning", "lead_time_days": 1, "depends_on": ["setup-plan", "recipe-check"], "is_critical": True},
        {"key": "event-day", "title": "Celebrate birthday event", "category": "Event Day", "lead_time_days": 0, "depends_on": ["host-checkin", "music-test"], "is_critical": True},
    ],
    "community": [
        {"key": "permit-approval", "title": "Secure permits and city approvals", "category": "Compliance", "lead_time_days": 90, "depends_on": [], "is_critical": True},
        {"key": "site-scout", "title": "Scout venue and access requirements", "category": "Venue", "lead_time_days": 75, "depends_on": ["permit-approval"], "is_critical": True},
        {"key": "volunteer-plan", "title": "Recruit volunteers and orient leads", "category": "Operations", "lead_time_days": 60, "depends_on": ["site-scout"], "is_critical": True},
        {"key": "promo-launch", "title": "Launch promotions and registration push", "category": "Marketing", "lead_time_days": 60, "depends_on": ["permit-approval"], "is_critical": True},
        {"key": "equipment-rent", "title": "Book tents, sound, and hydration rentals", "category": "Equipment", "lead_time_days": 45, "depends_on": ["site-scout"], "is_critical": True},
        {"key": "food-partners", "title": "Confirm food vendors and waste plan", "category": "Catering", "lead_time_days": 35, "depends_on": ["equipment-rent"], "is_critical": True},
        {"key": "safety-plan", "title": "Finalize safety and accessibility checks", "category": "Safety", "lead_time_days": 30, "depends_on": ["volunteer-plan", "site-scout"], "is_critical": True},
        {"key": "promo-final", "title": "Finalize outreach materials and signage", "category": "Marketing", "lead_time_days": 21, "depends_on": ["promo-launch"], "is_critical": False},
        {"key": "setup-check", "title": "Check course, stages, and venue layout", "category": "Operations", "lead_time_days": 10, "depends_on": ["equipment-rent", "safety-plan"], "is_critical": True},
        {"key": "vendor-confirm", "title": "Confirm vendor schedules and site arrival", "category": "Vendor Management", "lead_time_days": 7, "depends_on": ["food-partners", "equipment-rent"], "is_critical": True},
        {"key": "volunteer-brief", "title": "Brief volunteers and assign stations", "category": "Operations", "lead_time_days": 2, "depends_on": ["vendor-confirm", "volunteer-plan"], "is_critical": True},
        {"key": "weather-review", "title": "Review weather and emergency actions", "category": "Risk", "lead_time_days": 2, "depends_on": ["setup-check"], "is_critical": True},
        {"key": "event-day", "title": "Run community event day", "category": "Event Day", "lead_time_days": 0, "depends_on": ["volunteer-brief", "weather-review"], "is_critical": True},
    ],
}
