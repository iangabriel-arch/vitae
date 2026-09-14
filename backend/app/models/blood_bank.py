import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class BloodBank(Base):
    """
    Lightweight reference table for the "always show an official fallback"
    principle. No live inventory tracking — that's explicitly out of scope
    (Section 3 of the project plan).
    """
    __tablename__ = "blood_banks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    location_area = Column(String, nullable=False)
    contact_phone = Column(String, nullable=True)
    hours = Column(String, nullable=True)
