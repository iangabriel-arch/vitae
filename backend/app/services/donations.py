"""
Shared donation-recording logic — used by both POST /donations (walk-ins)
and PATCH /matches/{id}/complete (in-app-matched donations), so both paths
stay consistent about what happens when a donation is logged.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.donation import Donation
from app.models.user import User


def record_donation(
    db: Session,
    donor: User,
    blood_bank_name: str,
    request_id: uuid.UUID | None = None,
    units_donated: int = 1,
) -> Donation:
    """
    Creates a Donation row AND updates the donor's last_donation_date.

    Centralizing this matters because the eligibility reminder (Section 3
    of the project plan, ~90-day window) reads last_donation_date — if a
    donation could be logged without updating it, the reminder would drift
    out of sync with reality depending on which code path logged it.
    """
    donation = Donation(
        donor_id=donor.id,
        request_id=request_id,
        blood_bank_name=blood_bank_name,
        units_donated=units_donated,
    )
    db.add(donation)
    donor.last_donation_date = datetime.now(timezone.utc)
    return donation
