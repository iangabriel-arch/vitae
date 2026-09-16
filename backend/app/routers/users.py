"""
Users resource — see API Contract Section 9 of the project plan.
GET/PATCH /users/me | GET /donors/search
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.enums import BloodType, UserRole
from app.models.user import User
from app.schemas.user import DonorCard, UserRead, UserUpdate

router = APIRouter(tags=["users"])

# Hard cap on donor search results. The point of this endpoint (per the
# security section of the project plan) is "never expose the full donor
# table" — without some limit, broad/empty filters return exactly that in
# a single response. Real pagination is the complete fix; this is the
# one-line version that closes the obvious case for now.
_DONOR_SEARCH_LIMIT = 50


@router.get("/users/me", response_model=UserRead)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/users/me", response_model=UserRead)
def update_my_profile(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(current_user, field, value)

    try:
        db.commit()
    except IntegrityError:
        # Only `phone` is unique among the updatable fields.
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="That phone number is already in use by another account",
        )
    db.refresh(current_user)
    return current_user


@router.get("/donors/search", response_model=list[DonorCard])
def search_donors(
    blood_type: BloodType | None = None,
    location_area: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(User).filter(User.role.in_([UserRole.DONOR, UserRole.BOTH]))

    if blood_type is not None:
        query = query.filter(User.blood_type == blood_type)
    if location_area is not None:
        query = query.filter(User.location_area.ilike(f"%{location_area}%"))

    # Don't show the requester their own account as a "match."
    query = query.filter(User.id != current_user.id)

    return query.limit(_DONOR_SEARCH_LIMIT).all()
