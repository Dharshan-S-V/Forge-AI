"""
ForgeAI Supabase Client.

Provides initialized Supabase clients for auth and storage operations.
"""

from functools import lru_cache

from supabase import Client, create_client

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@lru_cache()
def get_supabase_client() -> Client:
    """Get the Supabase client using the anon key.

    Used for client-facing operations that respect RLS.

    Returns:
        An initialized Supabase client.
    """
    settings = get_settings()
    client = create_client(settings.supabase_url, settings.supabase_anon_key)
    logger.info("Supabase client initialized (anon key)")
    return client


@lru_cache()
def get_supabase_admin_client() -> Client:
    """Get the Supabase client using the service role key.

    Used for backend operations that bypass RLS
    (e.g., inserting embeddings, managing documents).

    Returns:
        An initialized Supabase admin client.
    """
    settings = get_settings()
    client = create_client(settings.supabase_url, settings.supabase_service_role_key)
    logger.info("Supabase admin client initialized (service role)")
    return client
