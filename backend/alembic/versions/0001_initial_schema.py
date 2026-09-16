"""create initial schema (users, blood_requests, donor_matches, donations, blood_banks)

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-09-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

blood_type_enum = postgresql.ENUM(
    "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", name="bloodtype", create_type=False
)
user_role_enum = postgresql.ENUM(
    "donor", "requester", "both", "admin", name="userrole", create_type=False
)
request_status_enum = postgresql.ENUM(
    "open", "fulfilled", "expired", "cancelled", name="requeststatus", create_type=False
)
urgency_level_enum = postgresql.ENUM(
    "low", "medium", "high", "critical", name="urgencylevel", create_type=False
)
match_status_enum = postgresql.ENUM(
    "notified", "accepted", "declined", "donated", "expired", name="matchstatus", create_type=False
)


def upgrade() -> None:
    bind = op.get_bind()
    blood_type_enum.create(bind, checkfirst=True)
    user_role_enum.create(bind, checkfirst=True)
    request_status_enum.create(bind, checkfirst=True)
    urgency_level_enum.create(bind, checkfirst=True)
    match_status_enum.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("blood_type", blood_type_enum, nullable=True),
        sa.Column("blood_type_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("location_area", sa.String(), nullable=True),
        sa.Column("last_donation_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("role", user_role_enum, nullable=False, server_default="both"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("phone", name="uq_users_phone"),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index(
        "ix_users_blood_type_location_area", "users", ["blood_type", "location_area"]
    )

    op.create_table(
        "blood_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "requester_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("blood_type_needed", blood_type_enum, nullable=False),
        sa.Column("units_needed", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("urgency", urgency_level_enum, nullable=False, server_default="medium"),
        sa.Column("hospital_name", sa.String(), nullable=False),
        sa.Column("location_area", sa.String(), nullable=False),
        sa.Column("status", request_status_enum, nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_blood_requests_status_urgency", "blood_requests", ["status", "urgency"]
    )

    op.create_table(
        "donor_matches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "request_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("blood_requests.id"),
            nullable=False,
        ),
        sa.Column(
            "donor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False
        ),
        sa.Column("status", match_status_enum, nullable=False, server_default="notified"),
        sa.Column("notified_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("responded_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "donations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "donor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False
        ),
        sa.Column(
            "request_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("blood_requests.id"),
            nullable=True,
        ),
        sa.Column("donation_date", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("blood_bank_name", sa.String(), nullable=False),
        sa.Column("units_donated", sa.Integer(), nullable=False, server_default="1"),
    )

    op.create_table(
        "blood_banks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("location_area", sa.String(), nullable=False),
        sa.Column("contact_phone", sa.String(), nullable=True),
        sa.Column("hours", sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("blood_banks")
    op.drop_table("donations")
    op.drop_table("donor_matches")
    op.drop_index("ix_blood_requests_status_urgency", table_name="blood_requests")
    op.drop_table("blood_requests")
    op.drop_index("ix_users_blood_type_location_area", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    match_status_enum.drop(bind, checkfirst=True)
    urgency_level_enum.drop(bind, checkfirst=True)
    request_status_enum.drop(bind, checkfirst=True)
    user_role_enum.drop(bind, checkfirst=True)
    blood_type_enum.drop(bind, checkfirst=True)cd ~/vitae/backend
