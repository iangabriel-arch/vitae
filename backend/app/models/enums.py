"""
Shared enums for model fields. Kept in one place so Pydantic schemas
and SQLAlchemy models stay in sync.
"""
import enum


class UserRole(str, enum.Enum):
    DONOR = "donor"
    REQUESTER = "requester"
    BOTH = "both"
    ADMIN = "admin"


class RequestStatus(str, enum.Enum):
    OPEN = "open"
    FULFILLED = "fulfilled"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class UrgencyLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MatchStatus(str, enum.Enum):
    NOTIFIED = "notified"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    DONATED = "donated"
    EXPIRED = "expired"


class BloodType(str, enum.Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"
