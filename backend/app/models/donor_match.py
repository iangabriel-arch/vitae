import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import MatchStatus, enum_values


class DonorMatch(Base):
    """
    Join table tracking the lifecycle of a single request-to-donor
    notification: notified -> accepted/declined -> donated.
    Powers "realistic response likelihood" in the UI (Section 6/8).
    """
    __tablename__ = "donor_matches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("blood_requests.id"), nullable=False)
    donor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    status = Column(
        Enum(MatchStatus, values_callable=enum_values),
        default=MatchStatus.NOTIFIED,
        nullable=False,
    )
    notified_at = Column(DateTime(timezone=True), server_default=func.now())
    responded_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    request = relationship("BloodRequest", back_populates="matches")
    donor = relationship("User", back_populates="donor_matches", foreign_keys=[donor_id])
