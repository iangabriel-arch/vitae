from pydantic import BaseModel, EmailStr, Field

from app.models.enums import BloodType, UserRole


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    # max_length=72 matches bcrypt's hard input limit — reject clearly at
    # the API boundary instead of silently truncating in hash_password.
    password: str = Field(min_length=8, max_length=72)
    blood_type: BloodType | None = None
    location_area: str | None = None
    role: UserRole = UserRole.BOTH


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
