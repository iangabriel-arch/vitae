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


def enum_values(enum_cls):
    """
    Pass as values_callable=enum_values to sa.Enum(SomeEnum, ...).

    SQLAlchemy's Enum column defaults to storing the Python member's *name*
    (e.g. "BOTH"), not its *value* (e.g. "both"). Our Postgres enum types
    (created in the Alembic migration) only accept the lowercase values, so
    without this every insert/update on an enum column fails with
    "invalid input value for enum ...".
    """
    return [e.value for e in enum_cls]
