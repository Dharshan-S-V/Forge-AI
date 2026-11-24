"""
ForgeAI API Router.

Aggregates all v1 API routers into a single router.
"""

from fastapi import APIRouter

from app.api.v1 import auth, chat, documents, users

# Main API router with /api/v1 prefix
api_router = APIRouter(prefix="/api/v1")

# Register all sub-routers
api_router.include_router(auth.router)
api_router.include_router(documents.router)
api_router.include_router(chat.router)
api_router.include_router(users.router)
