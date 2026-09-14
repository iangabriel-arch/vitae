"""
Import every model here so Alembic's `target_metadata = Base.metadata`
picks all of them up for autogenerate.
"""
from app.models.user import User  # noqa: F401
from app.models.blood_request import BloodRequest  # noqa: F401
from app.models.donor_match import DonorMatch  # noqa: F401
from app.models.donation import Donation  # noqa: F401
from app.models.blood_bank import BloodBank  # noqa: F401
