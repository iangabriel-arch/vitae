"""
Notification logic — email/in-app to start (Section 3 of the project plan).
Kept separate from matching.py so the channel (email now, SMS/USSD later)
can be swapped without touching matching logic.
"""
import logging

from app.models.donor_match import DonorMatch

logger = logging.getLogger("vitae.notifications")


def send_new_request_notification(match: DonorMatch) -> None:
    """
    STUB: logs what would be sent instead of actually sending email.

    Real delivery needs a provider decision (SMTP/SendGrid/SES + an
    account and credentials) that's out of scope to pick silently. This
    keeps the matching pipeline fully wired and testable end-to-end now;
    swapping in real delivery later is a one-function change — the
    call site in requests.py doesn't need to know the difference.
    """
    logger.info(
        "NOTIFICATION (stub, not actually sent): donor %s notified about "
        "blood request %s",
        match.donor_id,
        match.request_id,
    )
