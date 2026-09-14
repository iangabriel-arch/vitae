import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Donation(Base):
    """
    Donation history. Kept separate from donor_matches because not every
    donation ties back to an in-app request (walk-ins). See Section 8.
    """
    __tablename__ = "donations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    donor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    request_id = Column(UUID(as_uuid=True), ForeignKey("blood_requests.id"), nullable=True)

    donation_date = Column(DateTime(timezone=True), server_default=func.now())
    blood_bank_name = Column(String, nullable=False)
    units_donated = Column(Integer, nullable=False, default=1)

    # Relationships
    donor = relationship("User", back_populates="donations", foreign_keys=[donor_id])
    request = relationship("BloodRequest", back_populates="donations")
