from pydantic import BaseModel, EmailStr

from app.models.enums import BloodType, UserRole


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    password: str
    blood_type: BloodType | None = None
    location_area: str | None = None
    role: UserRole = UserRole.BOTH


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
