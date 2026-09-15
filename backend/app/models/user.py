import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import BloodType, UserRole, enum_values


class User(Base):
    """
    Doubles as both donor and requester via `role`, per Section 8 of the
    project plan — avoids splitting into separate donor/requester tables.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=False)

    blood_type = Column(Enum(BloodType, values_callable=enum_values), nullable=True)
    # Stays unverified until lab-confirmed — see "Verification risk" in the plan.
    blood_type_verified = Column(Boolean, default=False, nullable=False)

    # General area/radius only — never exact GPS coordinates (Security Section 4).
    location_area = Column(String, nullable=True)
    last_donation_date = Column(DateTime(timezone=True), nullable=True)

    role = Column(Enum(UserRole, values_callable=enum_values), default=UserRole.BOTH, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    requests = relationship(
        "BloodRequest", back_populates="requester", foreign_keys="BloodRequest.requester_id"
    )
    donor_matches = relationship(
        "DonorMatch", back_populates="donor", foreign_keys="DonorMatch.donor_id"
    )
    donations = relationship("Donation", back_populates="donor", foreign_keys="Donation.donor_id")

    __table_args__ = (
        # Speeds up the core donor-matching query: blood_type + location_area.
        Index("ix_users_blood_type_location_area", "blood_type", "location_area"),
    )
