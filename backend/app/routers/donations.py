"""
Donations resource — API Contract Section 9.
"""
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.blood_request import BloodRequest
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationRead, EligibilityRead
from app.services.donations import record_donation

router = APIRouter(tags=["donations"])

# Matches the "~90 days since last donation" eligibility reminder named in
# the MVP scope (Section 3 of the project plan) — the standard minimum
# interval between whole-blood donations.
ELIGIBILITY_INTERVAL_DAYS = 90


@router.post("/donations", response_model=DonationRead, status_code=status.HTTP_201_CREATED)
def log_donation(
    payload: DonationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # request_id is nullable (walk-ins) but if one is given, it must be real —
    # otherwise a donation could silently reference a nonexistent request.
    if payload.request_id is not None:
        blood_request = db.get(BloodRequest, payload.request_id)
        if blood_request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Referenced request not found",
            )

    donation = record_donation(
        db,
        donor=current_user,
        blood_bank_name=payload.blood_bank_name,
        request_id=payload.request_id,
        units_donated=payload.units_donated,
    )
    db.commit()
    db.refresh(donation)
    return donation


@router.get("/users/me/donations", response_model=list[DonationRead])
def my_donation_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Donation)
        .filter(Donation.donor_id == current_user.id)
        .order_by(Donation.donation_date.desc())
        .all()
    )


@router.get("/users/me/eligibility", response_model=EligibilityRead)
def my_eligibility(current_user: User = Depends(get_current_user)):
    if current_user.last_donation_date is None:
        # Never donated (in-app) — nothing to wait out.
        return EligibilityRead(
            eligible=True,
            last_donation_date=None,
            next_eligible_date=None,
            days_until_eligible=None,
        )

    next_eligible_date = current_user.last_donation_date + timedelta(
        days=ELIGIBILITY_INTERVAL_DAYS
    )
    now = datetime.now(timezone.utc)
    eligible = now >= next_eligible_date

    return EligibilityRead(
        eligible=eligible,
        last_donation_date=current_user.last_donation_date,
        next_eligible_date=next_eligible_date,
        days_until_eligible=None if eligible else (next_eligible_date - now).days,
    )
