"""
ForgeAI API Dependencies.

Shared FastAPI dependencies for dependency injection.
"""

from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.security import get_current_user_id
from app.db.session import get_db_session


async def get_db(
    session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[AsyncSession, None]:
    """Alias for database session dependency."""
    yield session


# Re-export commonly used dependencies for clean import
__all__ = [
    "get_db",
    "get_settings",
    "get_current_user_id",
]
