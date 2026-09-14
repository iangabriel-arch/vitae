import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DonationCreate(BaseModel):
    blood_bank_name: str
    units_donated: int = 1
    request_id: uuid.UUID | None = None  # nullable — walk-in donations allowed


class DonationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    donor_id: uuid.UUID
    request_id: uuid.UUID | None
    donation_date: datetime
    blood_bank_name: str
    units_donated: int


class EligibilityRead(BaseModel):
    """GET /users/me/eligibility — derived from last_donation_date."""
    eligible: bool
    last_donation_date: datetime | None
    next_eligible_date: datetime | None
    days_until_eligible: int | None
