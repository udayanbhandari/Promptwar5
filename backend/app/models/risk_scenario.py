"""SQLAlchemy model for RiskScenario entity."""

import uuid

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import relationship

from app.db.session import Base


def generate_uuid() -> str:
    """Generate a standard 36-character UUID string."""
    return str(uuid.uuid4())


class RiskScenario(Base):
    """Plan B contingency scenario."""

    __tablename__ = "risk_scenarios"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(
        String(36),
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    scenario_type = Column(String(50), nullable=False)  # weather, budget_cut, vendor_flake, guest_surge
    trigger_name = Column(String(150), nullable=False)
    mitigation_plan = Column(Text, nullable=False)
    budget_impact = Column(Float, nullable=False, default=0.0)
    is_activated = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    event = relationship("Event", back_populates="risk_scenarios")
