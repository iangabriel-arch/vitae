import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import BloodType, RequestStatus, UrgencyLevel


class BloodRequest(Base):
    """A posted need for blood. See Section 8 of the project plan."""
    __tablename__ = "blood_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requester_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    blood_type_needed = Column(Enum(BloodType), nullable=False)
    units_needed = Column(Integer, nullable=False, default=1)
    urgency = Column(Enum(UrgencyLevel), nullable=False, default=UrgencyLevel.MEDIUM)

    hospital_name = Column(String, nullable=False)
    location_area = Column(String, nullable=False)

    status = Column(Enum(RequestStatus), default=RequestStatus.OPEN, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    requester = relationship("User", back_populates="requests", foreign_keys=[requester_id])
    matches = relationship("DonorMatch", back_populates="request")
    donations = relationship("Donation", back_populates="request")

    __table_args__ = (
        # Speeds up "pull active requests quickly" per Section 8.
        Index("ix_blood_requests_status_urgency", "status", "urgency"),
    )
