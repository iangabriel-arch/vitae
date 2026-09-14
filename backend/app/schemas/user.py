import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import BloodType, UserRole


class UserRead(BaseModel):
    """Full profile — returned only for `/users/me` (the owner)."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    email: str
    phone: str | None
    blood_type: BloodType | None
    blood_type_verified: bool
    location_area: str | None
    last_donation_date: datetime | None
    role: UserRole
    created_at: datetime


class UserUpdate(BaseModel):
    """PATCH /users/me — only self-editable fields."""
    location_area: str | None = None
    last_donation_date: datetime | None = None
    phone: str | None = None


class DonorCard(BaseModel):
    """
    Anonymized donor card returned by /donors/search — per the API contract's
    'never return raw contact info' decision. No name/email/phone here.
    """
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    blood_type: BloodType | None
    blood_type_verified: bool
    location_area: str | None
