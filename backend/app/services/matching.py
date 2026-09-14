"""
Matching logic: given a new BloodRequest, find nearby donors of a
compatible blood type and create `donor_matches` rows.

This is invoked as a background side effect of POST /requests — never
exposed as its own client-facing endpoint (API Contract Section 9).
"""
from sqlalchemy.orm import Session

from app.models.blood_request import BloodRequest


def find_and_notify_matching_donors(db: Session, blood_request: BloodRequest) -> None:
    """
    TODO:
    1. Query users where blood_type is compatible with blood_request.blood_type_needed
       and location_area is within the request's area (start with exact-match,
       extend to a radius/geo lookup later).
    2. Create a DonorMatch row per matched donor (status=NOTIFIED).
    3. Call notifications.send_new_request_notification for each match.
    """
    raise NotImplementedError
