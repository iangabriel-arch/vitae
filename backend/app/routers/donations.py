"""
Donations resource — API Contract Section 9.
"""
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationRead, EligibilityRead

router = APIRouter(tags=["donations"])


@router.post("/donations", response_model=DonationRead, status_code=status.HTTP_201_CREATED)
def log_donation(payload: DonationCreate, current_user: User = Depends(get_current_user)):
    # request_id is nullable — supports walk-in donations not tied to a match.
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/users/me/donations", response_model=list[DonationRead])
def my_donation_history(current_user: User = Depends(get_current_user)):
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/users/me/eligibility", response_model=EligibilityRead)
def my_eligibility(current_user: User = Depends(get_current_user)):
    # TODO: derive from last_donation_date, ~90-day eligibility window (Section 3).
    raise HTTPException(status_code=501, detail="Not implemented yet")
