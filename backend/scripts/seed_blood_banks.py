"""
One-time seed script for blood_banks — not an API endpoint on purpose.
The API contract only specifies GET for this resource (it's reference
data, not user-generated), so seeding happens here instead of through
a POST route that was never part of the design.

Run once against a fresh database:
    python -m scripts.seed_blood_banks

Data source: Kenya's six official KNBTS (Kenya National Blood Transfusion
Service) Regional Blood Transfusion Centres, per a U.S. CDC Kenya blog
post (archive.cdc.gov, dated 2014):
https://archive.cdc.gov/www_cdc_gov/globalhealth/countries/kenya/blog/giving.htm

IMPORTANT — before this goes anywhere near real users: the phone numbers
below are from a 2014 source. Re-verify every number directly with KNBTS
(https://nbtskenya.or.ke) before launch — this is the app's stated
emergency fallback (Section 6/10 of the project plan), so a wrong number
here is actively harmful, not just stale data. Operating hours aren't
included because no reliable source for them was found; that field is
left empty rather than guessed.
"""
from app.core.database import SessionLocal
from app.models.blood_bank import BloodBank

REGIONAL_CENTRES = [
    {
        "name": "KNBTS Regional Blood Transfusion Centre — Nairobi",
        "location_area": "Nairobi",
        "contact_phone": "0716773904",
        "hours": None,
    },
    {
        "name": "KNBTS Regional Blood Transfusion Centre — Kisumu",
        "location_area": "Kisumu",
        "contact_phone": "0716773933",
        "hours": None,
    },
    {
        "name": "KNBTS Regional Blood Transfusion Centre — Mombasa",
        "location_area": "Mombasa",
        "contact_phone": "0716773934",
        "hours": None,
    },
    {
        "name": "KNBTS Regional Blood Transfusion Centre — Eldoret",
        "location_area": "Eldoret",
        "contact_phone": "0716775229",
        "hours": None,
    },
    {
        "name": "KNBTS Regional Blood Transfusion Centre — Embu",
        "location_area": "Embu",
        "contact_phone": "0716775232",
        "hours": None,
    },
    {
        "name": "KNBTS Regional Blood Transfusion Centre — Nakuru",
        "location_area": "Nakuru",
        "contact_phone": "0716773916",
        "hours": None,
    },
]


def seed():
    db = SessionLocal()
    try:
        existing_names = {b.name for b in db.query(BloodBank.name).all()}
        added = 0
        for centre in REGIONAL_CENTRES:
            if centre["name"] in existing_names:
                continue  # safe to re-run — won't create duplicates
            db.add(BloodBank(**centre))
            added += 1
        db.commit()
        print(f"Seeded {added} blood bank(s); {len(REGIONAL_CENTRES) - added} already present.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
