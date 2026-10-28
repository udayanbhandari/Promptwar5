"""Pydantic schemas enforcing Gemini structured outputs for all planning domains."""

from typing import List, Literal
from pydantic import BaseModel, Field, field_validator


# -----------------------------------------------------------------------------
# 1. Budget Split Schema
# -----------------------------------------------------------------------------
class CategoryPercentage(BaseModel):
    """Budget category allocation percentage with rationale."""

    category: str = Field(..., min_length=2, max_length=60, description="Budget category name")
    percentage: float = Field(..., gt=0.0, le=100.0, description="Percentage of total budget")
    reason: str = Field(..., min_length=5, max_length=250, description="One-line justification tailored to event")


class BudgetSplitOutput(BaseModel):
    """Structured output for budget allocations. Must sum to exactly 100%."""

    categories: List[CategoryPercentage] = Field(..., min_length=3, max_length=12)

    @field_validator("categories")
    @classmethod
    def validate_sum_100(cls, categories: List[CategoryPercentage]) -> List[CategoryPercentage]:
        """Verify that category percentages sum to 100 within floating point precision."""
        total = sum(c.percentage for c in categories)
        if abs(total - 100.0) > 0.5:
            raise ValueError(f"Category percentages must sum to 100.0, got {total:.2f}")
        return categories


# -----------------------------------------------------------------------------
# 2. Personalized Ideas Schema
# -----------------------------------------------------------------------------
class PersonalizedIdea(BaseModel):
    """A personalized idea recommendation."""

    aspect: Literal["theme", "decor", "food", "entertainment", "memorable_touch"]
    title: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10, max_length=400)
    cost_tier: Literal["low", "medium", "high"]
    why_it_fits: str = Field(..., min_length=5, max_length=250, description="Why this fits user's specific context")


class IdeasOutput(BaseModel):
    """Exactly 5 curated ideas covering theme, decor, food, entertainment, and memorable touch."""

    ideas: List[PersonalizedIdea]

    @field_validator("ideas")
    @classmethod
    def validate_exactly_five(cls, ideas: List[PersonalizedIdea]) -> List[PersonalizedIdea]:
        if len(ideas) != 5:
            raise ValueError(f"Must have exactly 5 ideas (one per aspect), received {len(ideas)}")
        aspects = {i.aspect for i in ideas}
        required_aspects = {"theme", "decor", "food", "entertainment", "memorable_touch"}
        if aspects != required_aspects:
            raise ValueError(f"Ideas must cover all 5 aspects: {required_aspects}")
        return ideas


# -----------------------------------------------------------------------------
# 3. Vendor Categories Schema
# -----------------------------------------------------------------------------
class VendorCategoryRecommendation(BaseModel):
    """Required vendor category with inquiry questions and red flags."""

    category: str = Field(..., min_length=2, max_length=60)
    questions: List[str] = Field(..., description="Exactly 5 screening questions to ask")
    red_flags: List[str] = Field(..., description="Exactly 3 warning signs or red flags")

    @field_validator("questions")
    @classmethod
    def validate_questions_count(cls, v: List[str]) -> List[str]:
        if len(v) != 5:
            raise ValueError(f"Must provide exactly 5 questions, got {len(v)}")
        return v

    @field_validator("red_flags")
    @classmethod
    def validate_red_flags_count(cls, v: List[str]) -> List[str]:
        if len(v) != 3:
            raise ValueError(f"Must provide exactly 3 red flags, got {len(v)}")
        return v


class VendorCategoriesOutput(BaseModel):
    """List of vendor categories needed for this event."""

    categories: List[VendorCategoryRecommendation] = Field(..., min_length=2, max_length=10)


# -----------------------------------------------------------------------------
# 4. Risk Scenarios Schema (Plan B)
# -----------------------------------------------------------------------------
class RiskScenarioItem(BaseModel):
    """A contingency scenario tailored to the specific event."""

    scenario_title: str = Field(..., min_length=3, max_length=120)
    likelihood: Literal["low", "medium", "high"]
    impact: Literal["low", "medium", "high"]
    early_warning_sign: str = Field(..., min_length=5, max_length=200)
    fallback_steps: str = Field(..., min_length=10, max_length=500)
    cost_impact_percent: float = Field(..., description="Estimated percentage shift in budget, e.g. +10.0 or -5.0")


class RiskScenariosOutput(BaseModel):
    """Exactly 5 prioritized risk scenarios."""

    risks: List[RiskScenarioItem]

    @field_validator("risks")
    @classmethod
    def validate_exactly_five(cls, risks: List[RiskScenarioItem]) -> List[RiskScenarioItem]:
        if len(risks) != 5:
            raise ValueError(f"Must provide exactly 5 risk scenarios, got {len(risks)}")
        return risks


# -----------------------------------------------------------------------------
# 5. Vendor Brief Schema
# -----------------------------------------------------------------------------
class VendorBriefOutput(BaseModel):
    """Concise inquiry communication and vendor selection checklist."""

    enquiry_message: str = Field(..., min_length=20, max_length=1000, description="WhatsApp/Email inquiry message")
    comparison_checklist: List[str] = Field(..., min_length=3, max_length=8, description="Criteria to evaluate quotes")
