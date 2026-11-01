"""SQLAlchemy model for BudgetItem entity."""

import uuid

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.session import Base


def generate_uuid() -> str:
    """Generate a standard 36-character UUID string."""
    return str(uuid.uuid4())


class BudgetItem(Base):
    """Budget line item belonging to an Event."""

    __tablename__ = "budget_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(
        String(36),
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category = Column(String(50), nullable=False)
    item_name = Column(String(150), nullable=False)
    estimated_cost = Column(Float, nullable=False)
    actual_cost = Column(Float, nullable=False, default=0.0)
    is_paid = Column(Boolean, nullable=False, default=False)
    priority = Column(Integer, nullable=False, default=2)  # 1 (Vital) to 3 (Optional)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    event = relationship("Event", back_populates="budget_items")
