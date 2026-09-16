import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, blood_banks, donations, health, matches, requests, users

# Without this, app-level logger.info() calls (e.g. the notification stub)
# are silently dropped — Python's root logger defaults to WARNING with no
# handler attached. This affects every logger under the "app" hierarchy,
# not just notifications.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers — one per resource, matching the API contract (project plan Section 9).
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(requests.router)
app.include_router(matches.router)
app.include_router(donations.router)
app.include_router(blood_banks.router)
