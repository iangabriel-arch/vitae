"""
Blood banks resource — public, no auth required. The always-available
emergency fallback (Section 6/10 of the project plan).
"""
import uuid

from fastapi import APIRouter, HTTPException

from app.schemas.blood_bank import BloodBankRead

router = APIRouter(prefix="/blood-banks", tags=["blood-banks"])


@router.get("", response_model=list[BloodBankRead])
def list_blood_banks(location_area: str | None = None):
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{blood_bank_id}", response_model=BloodBankRead)
def get_blood_bank(blood_bank_id: uuid.UUID):
    raise HTTPException(status_code=501, detail="Not implemented yet")
