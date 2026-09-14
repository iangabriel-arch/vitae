import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import BloodType, RequestStatus, UrgencyLevel


class BloodRequestCreate(BaseModel):
    blood_type_needed: BloodType
    units_needed: int = 1
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM
    hospital_name: str
    location_area: str
    expires_at: datetime | None = None


class BloodRequestUpdate(BaseModel):
    status: RequestStatus | None = None


class BloodRequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    requester_id: uuid.UUID
    blood_type_needed: BloodType
    units_needed: int
    urgency: UrgencyLevel
    hospital_name: str
    location_area: str
    status: RequestStatus
    created_at: datetime
    expires_at: datetime | None
