"""
Notification logic — email/in-app to start (Section 3 of the project plan).
Kept separate from matching.py so the channel (email now, SMS/USSD later)
can be swapped without touching matching logic.
"""
from app.models.donor_match import DonorMatch


def send_new_request_notification(match: DonorMatch) -> None:
    """
    TODO: send an email (and/or in-app notification) to the matched donor
    telling them a nearby compatible blood request was posted. Keep this
    function's signature stable so a later SMS/USSD gateway can call the
    same matching pipeline without a rewrite (Section 5 of the plan).
    """
    raise NotImplementedError
