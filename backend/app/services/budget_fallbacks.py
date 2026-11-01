"""Deterministic fallback data for AI planning outputs."""

from app.schemas.ai_outputs import (
    BudgetSplitOutput,
    CategoryPercentage,
)

FALLBACK_BUDGETS: dict[str, BudgetSplitOutput] = {
    "wedding": BudgetSplitOutput(
        categories=[
            CategoryPercentage(category="Catering & Bar", percentage=40.0, reason="Core guest hospitality experience."),
            CategoryPercentage(
                category="Venue & Rentals", percentage=25.0, reason="Secures site and essential tables/seating."
            ),
            CategoryPercentage(category="Photography & Video", percentage=15.0, reason="Preserves lifelong memories."),
            CategoryPercentage(
                category="Floral & Styling", percentage=10.0, reason="Transforms atmosphere and aesthetic."
            ),
            CategoryPercentage(category="Music & Entertainment", percentage=5.0, reason="Sets celebration energy."),
            CategoryPercentage(
                category="Contingency Buffer", percentage=5.0, reason="Covers day-of emergency expenses."
            ),
        ]
    ),
    "birthday": BudgetSplitOutput(
        categories=[
            CategoryPercentage(
                category="Food, Drinks & Cake",
                percentage=45.0,
                reason="Main enjoyment factor for celebratory gatherings.",
            ),
            CategoryPercentage(
                category="Venue / Activity Fees",
                percentage=30.0,
                reason="Space rental, entry tickets, or table reservations.",
            ),
            CategoryPercentage(
                category="Decor & Visual Theme", percentage=12.0, reason="Balloons, lighting, and signage."
            ),
            CategoryPercentage(
                category="Entertainment & Games", percentage=8.0, reason="DJ, playlist gear, or group activities."
            ),
            CategoryPercentage(category="Contingency Buffer", percentage=5.0, reason="Tips and last-minute supplies."),
        ]
    ),
    "community": BudgetSplitOutput(
        categories=[
            CategoryPercentage(
                category="Permits, Safety & Sanitation",
                percentage=25.0,
                reason="Mandatory city compliance, first-aid, and waste management.",
            ),
            CategoryPercentage(
                category="Staging, Tents & Equipment",
                percentage=35.0,
                reason="Infrastructure for mass outdoor/indoor attendance.",
            ),
            CategoryPercentage(
                category="Promotion & Signage", percentage=15.0, reason="Outreach, banners, and directional wayfinding."
            ),
            CategoryPercentage(
                category="Hydration & Refreshments",
                percentage=15.0,
                reason="Volunteer fuel and participant water stations.",
            ),
            CategoryPercentage(
                category="Contingency Fund", percentage=10.0, reason="Weather adjustments and equipment repairs."
            ),
        ]
    ),
}
