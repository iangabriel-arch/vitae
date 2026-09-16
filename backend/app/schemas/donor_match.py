import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

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
    status: MatchStatus

    @field_validator("status")
    @classmethod
    def restrict_to_donor_choices(cls, value: MatchStatus) -> MatchStatus:
        # A donor can only ever accept or decline through this endpoint —
        # `donated` is set by complete_match (owner/admin only, after
        # verified collection), never self-reported by the donor.
        if value not in (MatchStatus.ACCEPTED, MatchStatus.DECLINED):
            raise ValueError("status must be 'accepted' or 'declined'")
        return value
