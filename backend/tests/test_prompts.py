"""Test suite for versioned prompts, AI schemas, and deterministic fallbacks."""

import pytest
from pydantic import ValidationError

from app.prompts import (
    budget_split_v1,
    ideas_v1,
    risk_scenarios_v1,
    vendor_brief_v1,
    vendor_categories_v1,
)
from app.schemas.ai_outputs import (
    BudgetSplitOutput,
    CategoryPercentage,
    IdeasOutput,
    PersonalizedIdea,
    RiskScenarioItem,
    RiskScenariosOutput,
    VendorBriefOutput,
    VendorCategoriesOutput,
    VendorCategoryRecommendation,
)
from app.services.fallbacks import (
    get_fallback_budget_split,
    get_fallback_ideas,
    get_fallback_risk_scenarios,
    get_fallback_vendor_brief,
    get_fallback_vendor_categories,
)


# -----------------------------------------------------------------------------
# 1. Prompt Builders & Versioning Tests
# -----------------------------------------------------------------------------
def test_prompt_modules_metadata():
    """Verify all prompt modules export VERSION, OutputSchema, and build_prompt."""
    modules = [
        budget_split_v1,
        ideas_v1,
        vendor_categories_v1,
        risk_scenarios_v1,
        vendor_brief_v1,
    ]
    for mod in modules:
        assert hasattr(mod, "VERSION")
        assert hasattr(mod, "OutputSchema")
        assert callable(getattr(mod, "build_prompt"))
        assert "v1" in mod.VERSION


def test_budget_prompt_wrapping():
    """Verify build_prompt wraps untrusted user data securely."""
    prompt = budget_split_v1.build_prompt(
        event_type="wedding",
        guest_count=120,
        city="Mumbai",
        culture_style="Traditional Hindu",
        special_requirements="Pure vegetarian catering",
    )
    assert "<user_data>" in prompt
    assert "</user_data>" in prompt
    assert "Traditional Hindu" in prompt
    assert "120 attendees" in prompt
    assert "DO NOT output currency amounts" in prompt


# -----------------------------------------------------------------------------
# 2. Schema Rejection Tests
# -----------------------------------------------------------------------------
def test_budget_split_schema_rejects_non_100_sum():
    """BudgetSplitOutput must reject percentages that do not sum to 100."""
    # Sum = 90.0
    bad_categories = [
        CategoryPercentage(category="Venue", percentage=50.0, reason="Location booking fee"),
        CategoryPercentage(category="Food", percentage=30.0, reason="Catering and meals"),
        CategoryPercentage(category="Decor", percentage=10.0, reason="Floral styling and decor"),
    ]
    with pytest.raises(ValidationError) as exc_info:
        BudgetSplitOutput(categories=bad_categories)
    assert "must sum to 100.0" in str(exc_info.value)

    # Sum = 110.0
    bad_categories_2 = [
        CategoryPercentage(category="Venue", percentage=50.0, reason="Location booking fee"),
        CategoryPercentage(category="Food", percentage=40.0, reason="Catering and meals"),
        CategoryPercentage(category="Decor", percentage=20.0, reason="Floral styling and decor"),
    ]
    with pytest.raises(ValidationError) as exc_info_2:
        BudgetSplitOutput(categories=bad_categories_2)
    assert "must sum to 100.0" in str(exc_info_2.value)


def test_ideas_schema_rejects_non_5_items():
    """IdeasOutput must reject counts != 5 or missing aspects."""
    # 4 ideas only
    four_ideas = [
        PersonalizedIdea(aspect="theme", title="Theme 1", description="Valid description length", cost_tier="low", why_it_fits="Fits context well"),
        PersonalizedIdea(aspect="decor", title="Decor 2", description="Valid description length", cost_tier="medium", why_it_fits="Fits context well"),
        PersonalizedIdea(aspect="food", title="Food 3", description="Valid description length", cost_tier="high", why_it_fits="Fits context well"),
        PersonalizedIdea(aspect="entertainment", title="Music 4", description="Valid description length", cost_tier="low", why_it_fits="Fits context well"),
    ]
    with pytest.raises(ValidationError) as exc_info:
        IdeasOutput(ideas=four_ideas)
    assert "exactly 5 ideas" in str(exc_info.value)

    # 5 ideas but duplicate aspect (missing memorable_touch)
    duplicate_aspect_ideas = four_ideas + [
        PersonalizedIdea(aspect="theme", title="Theme 5", description="Valid description length", cost_tier="low", why_it_fits="Fits context well"),
    ]
    with pytest.raises(ValidationError) as exc_info_2:
        IdeasOutput(ideas=duplicate_aspect_ideas)
    assert "cover all 5 aspects" in str(exc_info_2.value)


def test_vendor_categories_schema_validation():
    """VendorCategoryRecommendation must enforce exactly 5 questions and 3 red flags."""
    # 4 questions instead of 5
    with pytest.raises(ValidationError) as exc_info:
        VendorCategoryRecommendation(
            category="Venue",
            questions=["Q1", "Q2", "Q3", "Q4"],
            red_flags=["RF1", "RF2", "RF3"],
        )
    assert "exactly 5 questions" in str(exc_info.value)

    # 2 red flags instead of 3
    with pytest.raises(ValidationError) as exc_info:
        VendorCategoryRecommendation(
            category="Venue",
            questions=["Q1", "Q2", "Q3", "Q4", "Q5"],
            red_flags=["RF1", "RF2"],
        )
    assert "exactly 3 red flags" in str(exc_info.value)


def test_risk_scenarios_schema_rejects_non_5_items():
    """RiskScenariosOutput must enforce exactly 5 risk scenarios."""
    four_risks = [
        RiskScenarioItem(
            scenario_title=f"Risk {i}",
            likelihood="low",
            impact="medium",
            early_warning_sign="Warning sign details",
            fallback_steps="Fallback mitigation details",
            cost_impact_percent=5.0,
        )
        for i in range(4)
    ]
    with pytest.raises(ValidationError) as exc_info:
        RiskScenariosOutput(risks=four_risks)
    assert "exactly 5 risk scenarios" in str(exc_info.value)


# -----------------------------------------------------------------------------
# 3. Fallback Templates Validation Tests
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("event_type", ["wedding", "birthday", "community"])
def test_fallback_budget_splits_valid(event_type):
    """Every event type fallback budget split must sum to 100.0 and validate."""
    fallback = get_fallback_budget_split(event_type)
    assert isinstance(fallback, BudgetSplitOutput)
    total_pct = sum(c.percentage for c in fallback.categories)
    assert abs(total_pct - 100.0) < 0.01


@pytest.mark.parametrize("event_type", ["wedding", "birthday", "community"])
def test_fallback_ideas_valid(event_type):
    """Every event type fallback ideas bundle must have exactly 5 distinct aspects."""
    fallback = get_fallback_ideas(event_type)
    assert isinstance(fallback, IdeasOutput)
    assert len(fallback.ideas) == 5
    aspects = {i.aspect for i in fallback.ideas}
    assert aspects == {"theme", "decor", "food", "entertainment", "memorable_touch"}


@pytest.mark.parametrize("event_type", ["wedding", "birthday", "community"])
def test_fallback_vendor_categories_valid(event_type):
    """Every vendor category must have exactly 5 questions and 3 red flags."""
    fallback = get_fallback_vendor_categories(event_type)
    assert isinstance(fallback, VendorCategoriesOutput)
    assert len(fallback.categories) >= 2
    for cat in fallback.categories:
        assert len(cat.questions) == 5
        assert len(cat.red_flags) == 3


@pytest.mark.parametrize("event_type", ["wedding", "birthday", "community"])
def test_fallback_risks_valid(event_type):
    """Every event type fallback risk bundle must have exactly 5 scenarios."""
    fallback = get_fallback_risk_scenarios(event_type)
    assert isinstance(fallback, RiskScenariosOutput)
    assert len(fallback.risks) == 5


def test_fallback_vendor_brief_valid():
    """Vendor brief fallback must produce a ready enquiry message and checklist."""
    brief = get_fallback_vendor_brief(
        vendor_category="Catering",
        event_type="wedding",
        event_date="2026-11-20",
        guest_count=120,
        city="Mumbai",
    )
    assert isinstance(brief, VendorBriefOutput)
    assert "Catering" in brief.enquiry_message
    assert "2026-11-20" in brief.enquiry_message
    assert len(brief.comparison_checklist) >= 3
