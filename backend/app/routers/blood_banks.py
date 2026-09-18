"""
Blood banks resource — public, no auth required. The always-available
emergency fallback (Section 6/10 of the project plan).
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.blood_bank import BloodBank
from app.schemas.blood_bank import BloodBankRead

router = APIRouter(prefix="/blood-banks", tags=["blood-banks"])


@router.get("", response_model=list[BloodBankRead])
def list_blood_banks(location_area: str | None = None, db: Session = Depends(get_db)):
    query = db.query(BloodBank)
    if location_area is not None:
        query = query.filter(BloodBank.location_area.ilike(f"%{location_area}%"))
    return query.order_by(BloodBank.name).all()


@router.get("/{blood_bank_id}", response_model=BloodBankRead)
def get_blood_bank(blood_bank_id: uuid.UUID, db: Session = Depends(get_db)):
    blood_bank = db.get(BloodBank, blood_bank_id)
    if blood_bank is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blood bank not found")
    return blood_bank
