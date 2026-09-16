"""
Blood requests resource — see API Contract Section 9 of the project plan.
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.blood_request import BloodRequest
from app.models.enums import BloodType, RequestStatus, UrgencyLevel, UserRole
from app.models.user import User
from app.schemas.blood_request import BloodRequestCreate, BloodRequestRead, BloodRequestUpdate
from app.services import matching, notifications

router = APIRouter(prefix="/requests", tags=["requests"])

# Same reasoning as donor search: no result count on a list endpoint is
# effectively "return everything," which undercuts the RBAC/exposure
# principle in Section 4 even though requests are less sensitive than the
# donor table. Real pagination is later-phase work.
_LIST_LIMIT = 100


def _require_owner_or_admin(blood_request: BloodRequest, current_user: User) -> None:
    is_owner = blood_request.requester_id == current_user.id
    is_admin = current_user.role == UserRole.ADMIN
    if not (is_owner or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this request",
        )


def _get_request_or_404(request_id: uuid.UUID, db: Session) -> BloodRequest:
    blood_request = db.get(BloodRequest, request_id)
    if blood_request is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
    return blood_request


@router.post("", response_model=BloodRequestRead, status_code=status.HTTP_201_CREATED)
def create_request(
    payload: BloodRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    blood_request = BloodRequest(requester_id=current_user.id, **payload.model_dump())
    db.add(blood_request)
    db.flush()  # assigns blood_request.id without committing yet

    matches = matching.find_and_notify_matching_donors(db, blood_request)
    db.commit()
    db.refresh(blood_request)

    # Notify only after the commit succeeds — a rollback should never
    # result in a notification about matches that don't actually exist.
    for match in matches:
        notifications.send_new_request_notification(match)

    return blood_request


@router.get("", response_model=list[BloodRequestRead])
def list_requests(
    location_area: str | None = None,
    blood_type_needed: BloodType | None = None,
    urgency: UrgencyLevel | None = None,
    status_filter: RequestStatus = RequestStatus.OPEN,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(BloodRequest).filter(BloodRequest.status == status_filter)

    if location_area is not None:
        query = query.filter(BloodRequest.location_area.ilike(f"%{location_area}%"))
    if blood_type_needed is not None:
        query = query.filter(BloodRequest.blood_type_needed == blood_type_needed)
    if urgency is not None:
        query = query.filter(BloodRequest.urgency == urgency)

    return query.order_by(BloodRequest.created_at.desc()).limit(_LIST_LIMIT).all()


@router.get("/{request_id}", response_model=BloodRequestRead)
def get_request(
    request_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _get_request_or_404(request_id, db)


@router.patch("/{request_id}", response_model=BloodRequestRead)
def update_request(
    request_id: uuid.UUID,
    payload: BloodRequestUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    blood_request = _get_request_or_404(request_id, db)
    _require_owner_or_admin(blood_request, current_user)

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(blood_request, field, value)

    db.commit()
    db.refresh(blood_request)
    return blood_request


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_request(
    request_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    blood_request = _get_request_or_404(request_id, db)
    _require_owner_or_admin(blood_request, current_user)

    # Soft-delete: mark cancelled instead of deleting the row. The row is
    # referenced by donor_matches / donations, and the audit-logging
    # principle in Section 4 argues against destroying request history.
    blood_request.status = RequestStatus.CANCELLED
    db.commit()
    return None
