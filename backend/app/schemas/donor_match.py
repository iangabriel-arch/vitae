import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import MatchStatus


class DonorMatchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    request_id: uuid.UUID
    donor_id: uuid.UUID
    status: MatchStatus
    notified_at: datetime
    responded_at: datetime | None


class DonorMatchRespond(BaseModel):
    """PATCH /matches/{id} — donor accepts or declines."""
    status: MatchStatus  # expected: ACCEPTED or DECLINED
