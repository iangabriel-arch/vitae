"""
Donor matches resource (notification lifecycle) — API Contract Section 9.
"""
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.blood_request import BloodRequest
from app.models.donation import Donation
from app.models.donor_match import DonorMatch
from app.models.enums import MatchStatus, UserRole
from app.models.user import User
from app.schemas.donor_match import DonorMatchRead, DonorMatchRespond

router = APIRouter(tags=["matches"])


def _get_match_or_404(match_id: uuid.UUID, db: Session) -> DonorMatch:
    match = db.get(DonorMatch, match_id)
    if match is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return match


@router.get("/requests/{request_id}/matches", response_model=list[DonorMatchRead])
def list_matches_for_request(
    request_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    blood_request = db.get(BloodRequest, request_id)
    if blood_request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")

    is_owner = blood_request.requester_id == current_user.id
    is_admin = current_user.role == UserRole.ADMIN
    if not (is_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view matches for this request",
        )

    return db.query(DonorMatch).filter(DonorMatch.request_id == request_id).all()


@router.patch("/matches/{match_id}", response_model=DonorMatchRead)
def respond_to_match(
    match_id: uuid.UUID,
    payload: DonorMatchRespond,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    match = _get_match_or_404(match_id, db)

    if match.donor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the matched donor can respond to this match",
        )
    if match.status != MatchStatus.NOTIFIED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot respond to a match already in '{match.status.value}' status",
        )

    match.status = payload.status
    match.responded_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(match)
    return match


@router.patch("/matches/{match_id}/complete", response_model=DonorMatchRead)
def complete_match(
    match_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    match = _get_match_or_404(match_id, db)
    blood_request = db.get(BloodRequest, match.request_id)

    is_owner = blood_request is not None and blood_request.requester_id == current_user.id
    is_admin = current_user.role == UserRole.ADMIN
    if not (is_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to complete this match",
        )
    if match.status != MatchStatus.ACCEPTED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot complete a match in '{match.status.value}' status — donor must accept first",
        )

    match.status = MatchStatus.DONATED

    # Per the API contract: completing a match creates a donations row.
    # A single whole-blood donation is always 1 unit regardless of how many
    # units the request needed in total — units_needed can require several
    # separate donors/donations to fulfill.
    donation = Donation(
        donor_id=match.donor_id,
        request_id=match.request_id,
        blood_bank_name=blood_request.hospital_name if blood_request else "Unknown",
        units_donated=1,
    )
    db.add(donation)

    db.commit()
    db.refresh(match)
    return match
