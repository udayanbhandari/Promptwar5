"""Deterministic fallback services for AI planning outputs."""

from app.schemas.ai_outputs import VendorBriefOutput
from app.services.budget_fallbacks import FALLBACK_BUDGETS
from app.services.idea_fallbacks import FALLBACK_IDEAS
from app.services.risk_fallbacks import FALLBACK_RISKS
from app.services.vendor_fallbacks import FALLBACK_VENDOR_CATEGORIES


def _event_fallback(mapping: dict, event_type: str):
    """Return an event-specific fallback, defaulting to community guidance."""
    return mapping.get(event_type.lower().strip(), mapping["community"])


def get_fallback_budget_split(event_type: str):
    """Return deterministic budget allocation percentages."""
    return _event_fallback(FALLBACK_BUDGETS, event_type)


def get_fallback_ideas(event_type: str):
    """Return deterministic five-part creative ideas."""
    return _event_fallback(FALLBACK_IDEAS, event_type)


def get_fallback_vendor_categories(event_type: str):
    """Return deterministic vendor questions and red flags."""
    return _event_fallback(FALLBACK_VENDOR_CATEGORIES, event_type)


def get_fallback_risk_scenarios(event_type: str):
    """Return deterministic Plan B risk scenarios."""
    return _event_fallback(FALLBACK_RISKS, event_type)


def get_fallback_vendor_brief(
    vendor_category: str,
    event_type: str,
    event_date: str = "Upcoming Date",
    guest_count: int = 50,
    city: str = "Local City",
) -> VendorBriefOutput:
    """Return a ready-to-send vendor inquiry and comparison checklist."""
    category_clean = vendor_category.strip().title()
    event_clean = event_type.strip().title()
    enquiry_msg = (
        f"Hi there! I hope you're having a great week.\n\n"
        f"I am organizing a {event_clean} in {city} on {event_date} for approximately "
        f"{guest_count} guests. We are currently scouting for an experienced {category_clean} "
        "partner who delivers high-quality service and seamless coordination.\n\n"
        f"Could you please share:\n1. Your availability on {event_date}?\n"
        f"2. Your standard packages and pricing guides for ~{guest_count} attendees?\n"
        "3. An overview of what deliverables and setup/teardown time are included?\n\n"
        "Looking forward to hearing from you and discussing how we might collaborate!\n\n"
        "Warm regards."
    )
    checklist = [
        "Transparent pricing with all service charges, taxes, and fees explicitly itemized.",
        "Clear overtime rate and cancellation/reschedule policy stated in writing.",
        "Possession of active business liability insurance and required health/safety permits.",
        "Demonstrated experience with similar event scale and venue constraints.",
        "Contingency plan or backup personnel in case of equipment failure or illness.",
    ]
    return VendorBriefOutput(enquiry_message=enquiry_msg, comparison_checklist=checklist)
