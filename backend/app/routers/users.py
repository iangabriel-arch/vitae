"""
Users resource — see API Contract Section 9 of the project plan.
GET/PATCH /users/me | GET /donors/search
"""
from fastapi import APIRouter, Depends, HTTPException

from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import DonorCard, UserRead, UserUpdate

router = APIRouter(tags=["users"])


@router.get("/users/me", response_model=UserRead)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/users/me", response_model=UserRead)
def update_my_profile(payload: UserUpdate, current_user: User = Depends(get_current_user)):
    # TODO: apply payload fields to current_user, commit, refresh.
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/donors/search", response_model=list[DonorCard])
def search_donors(
    blood_type: str | None = None,
    location_area: str | None = None,
    current_user: User = Depends(get_current_user),
):
    # TODO: filtered query by blood_type + location_area only — never the
    # full donor table (RBAC principle, Section 4). Rate-limit this endpoint.
    raise HTTPException(status_code=501, detail="Not implemented yet")
