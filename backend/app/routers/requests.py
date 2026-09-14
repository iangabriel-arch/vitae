"""
Blood requests resource — see API Contract Section 9 of the project plan.
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.blood_request import BloodRequestCreate, BloodRequestRead, BloodRequestUpdate

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("", response_model=BloodRequestRead, status_code=status.HTTP_201_CREATED)
def create_request(payload: BloodRequestCreate, current_user: User = Depends(get_current_user)):
    # TODO: insert BloodRequest row, then kick off matching + notification
    # pipeline as a background side effect (see services/matching.py) —
    # NOT a separate client-facing endpoint, per the contract-level decision.
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("", response_model=list[BloodRequestRead])
def list_requests(
    location_area: str | None = None,
    blood_type_needed: str | None = None,
    urgency: str | None = None,
    current_user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{request_id}", response_model=BloodRequestRead)
def get_request(request_id: uuid.UUID, current_user: User = Depends(get_current_user)):
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.patch("/{request_id}", response_model=BloodRequestRead)
def update_request(
    request_id: uuid.UUID,
    payload: BloodRequestUpdate,
    current_user: User = Depends(get_current_user),
):
    # TODO: restrict to owner/admin.
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_request(request_id: uuid.UUID, current_user: User = Depends(get_current_user)):
    # TODO: restrict to owner/admin.
    raise HTTPException(status_code=501, detail="Not implemented yet")
