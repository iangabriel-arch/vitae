import uuid

from pydantic import BaseModel, ConfigDict


class BloodBankRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    location_area: str
    contact_phone: str | None
    hours: str | None
