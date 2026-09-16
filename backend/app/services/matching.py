"""
Matching logic: given a new BloodRequest, find compatible donors and
create `donor_matches` rows.

This is invoked as a background side effect of POST /requests — never
exposed as its own client-facing endpoint (API Contract Section 9).
"""
from sqlalchemy.orm import Session

from app.models.blood_request import BloodRequest
from app.models.donor_match import DonorMatch
from app.models.enums import BloodType, UserRole
from app.models.user import User

# Maps a *requested* blood type to the donor types that can safely give to
# it (standard transfusion compatibility — not exact-match only). E.g. an
# O+ request can be filled by an O+ or O- donor; O- is compatible with
# everyone, so it's listed as a donor option everywhere.
COMPATIBLE_DONOR_TYPES: dict[BloodType, list[BloodType]] = {
    BloodType.O_NEG: [BloodType.O_NEG],
    BloodType.O_POS: [BloodType.O_POS, BloodType.O_NEG],
    BloodType.A_NEG: [BloodType.A_NEG, BloodType.O_NEG],
    BloodType.A_POS: [BloodType.A_POS, BloodType.A_NEG, BloodType.O_POS, BloodType.O_NEG],
    BloodType.B_NEG: [BloodType.B_NEG, BloodType.O_NEG],
    BloodType.B_POS: [BloodType.B_POS, BloodType.B_NEG, BloodType.O_POS, BloodType.O_NEG],
    BloodType.AB_NEG: [BloodType.AB_NEG, BloodType.A_NEG, BloodType.B_NEG, BloodType.O_NEG],
    BloodType.AB_POS: list(BloodType),  # AB+ is the universal recipient
}


def find_and_notify_matching_donors(db: Session, blood_request: BloodRequest) -> list[DonorMatch]:
    """
    Creates (but does not commit) a DonorMatch row for every compatible,
    same-area donor. Caller is responsible for committing and then sending
    notifications — kept separate so a failed commit never triggers
    notifications for matches that don't actually exist yet.

    Location matching is exact-string for now (same as the rest of the
    schema) — a real radius/geo lookup is later-phase work per Section 5
    of the project plan.
    """
    compatible_types = COMPATIBLE_DONOR_TYPES[blood_request.blood_type_needed]

    donors = (
        db.query(User)
        .filter(User.role.in_([UserRole.DONOR, UserRole.BOTH]))
        .filter(User.blood_type.in_(compatible_types))
        .filter(User.location_area == blood_request.location_area)
        .filter(User.id != blood_request.requester_id)
        .all()
    )

    matches = []
    for donor in donors:
        match = DonorMatch(request_id=blood_request.id, donor_id=donor.id)
        db.add(match)
        matches.append(match)
    return matches
