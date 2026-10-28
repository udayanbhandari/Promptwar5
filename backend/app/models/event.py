"""SQLAlchemy model for Event entity."""

import uuid
from sqlalchemy import Column, Date, DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import relationship
from app.db.session import Base


def generate_uuid() -> str:
    """Generate a standard 36-character UUID string."""
    return str(uuid.uuid4())


class Event(Base):
    """Core Event entity."""

    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=False)
    event_type = Column(String(50), nullable=False)  # wedding, birthday, community
    target_date = Column(Date, nullable=False)
    guest_count = Column(Integer, nullable=False)
    total_budget = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    city = Column(String(100), nullable=False)
    theme_style = Column(String(150), nullable=True)
    special_requirements = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships with cascade delete
    budget_items = relationship(
        "BudgetItem",
        back_populates="event",
        cascade="all, delete-orphan",
        order_by="BudgetItem.priority",
    )
    tasks = relationship(
        "Task",
        back_populates="event",
        cascade="all, delete-orphan",
        order_by="Task.due_date",
    )
    vendors = relationship(
        "Vendor",
        back_populates="event",
        cascade="all, delete-orphan",
    )
    risk_scenarios = relationship(
        "RiskScenario",
        back_populates="event",
        cascade="all, delete-orphan",
    )
    share_links = relationship(
        "ShareLink",
        back_populates="event",
        cascade="all, delete-orphan",
    )
