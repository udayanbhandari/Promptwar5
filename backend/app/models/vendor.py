"""SQLAlchemy model for Vendor entity."""

import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import relationship
from app.db.session import Base


def generate_uuid() -> str:
    """Generate a standard 36-character UUID string."""
    return str(uuid.uuid4())


class Vendor(Base):
    """Vendor record associated with an Event."""

    __tablename__ = "vendors"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(
        String(36),
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category = Column(String(50), nullable=False)
    name = Column(String(150), nullable=False)
    status = Column(String(30), nullable=False, default="researching")  # researching, contacted, quoted, booked
    quoted_price = Column(Float, nullable=False, default=0.0)
    contact_info = Column(String(200), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    event = relationship("Event", back_populates="vendors")
