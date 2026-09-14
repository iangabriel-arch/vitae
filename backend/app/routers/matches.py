"""
Donor matches resource (notification lifecycle) — API Contract Section 9.
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.donor_match import DonorMatchRead, DonorMatchRespond

router = APIRouter(tags=["matches"])


@router.get("/requests/{request_id}/matches", response_model=list[DonorMatchRead])
def list_matches_for_request(request_id: uuid.UUID, current_user: User = Depends(get_current_user)):
    # TODO: restrict to request owner/admin.
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.patch("/matches/{match_id}", response_model=DonorMatchRead)
def respond_to_match(
    match_id: uuid.UUID,
    payload: DonorMatchRespond,
    current_user: User = Depends(get_current_user),
):
    # TODO: restrict to the matched donor; set responded_at.
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.patch("/matches/{match_id}/complete", response_model=DonorMatchRead)
def complete_match(match_id: uuid.UUID, current_user: User = Depends(get_current_user)):
    # TODO: restrict to owner/admin; mark donated, create a `donations` row.
    raise HTTPException(status_code=501, detail="Not implemented yet")
