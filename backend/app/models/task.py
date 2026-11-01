"""SQLAlchemy model for Task entity."""

import uuid

from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship

from app.db.session import Base


def generate_uuid() -> str:
    """Generate a standard 36-character UUID string."""
    return str(uuid.uuid4())


class Task(Base):
    """Planning task and milestone with JSON list dependencies."""

    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(
        String(36),
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="pending")  # pending, in_progress, completed
    owner = Column(String(100), nullable=False, default="Host")
    # Self-referencing task dependencies stored as a JSON list of task IDs
    depends_on = Column(JSON, nullable=False, default=list)
    is_day_of = Column(Boolean, nullable=False, default=False)
    start_time = Column(String(10), nullable=True)  # HH:MM for day-of run sheet
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    event = relationship("Event", back_populates="tasks")
