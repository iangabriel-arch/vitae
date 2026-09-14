"""
Auth resource — see API Contract Section 9 of the project plan.
POST /auth/register | POST /auth/login | POST /auth/logout
"""
from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest):
    # TODO: hash password (app.core.security.hash_password), insert User row,
    # issue an access token via create_access_token(str(user.id)).
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    # TODO: look up user by email, verify_password, issue access token.
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout():
    # TODO: token invalidation strategy (blocklist / short-lived tokens + refresh).
    raise HTTPException(status_code=501, detail="Not implemented yet")
