"""
ForgeAI Users API Routes (Stub).

User profile and dashboard stats routes.
Will be fully implemented in Milestone 7.
"""

from fastapi import APIRouter, Depends, status

from app.core.security import get_current_user_id

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/profile",
    summary="Get user profile",
    status_code=status.HTTP_200_OK,
)
async def get_profile(
    user_id: str = Depends(get_current_user_id),
) -> dict:
    """Get the current user's profile."""
    return {"id": user_id, "message": "Profile endpoint — coming in Milestone 7"}
