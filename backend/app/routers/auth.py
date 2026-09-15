"""
Auth resource — see API Contract Section 9 of the project plan.
POST /auth/register | POST /auth/login | POST /auth/logout
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = User(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
        blood_type=payload.blood_type,
        location_area=payload.location_area,
        role=payload.role,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        # Unique constraint on email or phone — don't leak which one to
        # avoid account enumeration on the phone field specifically.
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email or phone already exists",
        )
    db.refresh(user)

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    # Same error for "no such user" and "wrong password" — don't leak
    # which one it was (standard mitigation against account enumeration).
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )
    if user is None or not verify_password(payload.password, user.password_hash):
        raise invalid_credentials

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout():
    # This API is stateless JWT with no server-side session, so there is
    # nothing to invalidate server-side yet — logout is a client-side
    # token discard. This endpoint exists to match the API contract and
    # as the seam where real invalidation (a token blocklist, most likely
    # backed by Redis, or a move to short-lived access + refresh tokens)
    # gets added if/when it's actually needed. Not adding that
    # infrastructure now — it's unjustified complexity for a single-device,
    # no-real-users MVP.
    return None