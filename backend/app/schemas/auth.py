from pydantic import BaseModel, EmailStr, Field, field_validator

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

    @field_validator("role")
    @classmethod
    def reject_admin_self_registration(cls, value: UserRole) -> UserRole:
        # Public registration must never grant ADMIN. There's currently no
        # promotion path (no endpoint, no seed script) — that's a
        # deliberate gap until there's an actual need for a second admin,
        # rather than building unused machinery now. Until then, admin
        # accounts are created directly in the database.
        if value == UserRole.ADMIN:
            raise ValueError("Cannot self-register as admin")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
