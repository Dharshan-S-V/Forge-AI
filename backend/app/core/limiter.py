"""
ForgeAI Rate Limiter.

Shared slowapi Limiter instance, keyed by client IP.

This lives in its own module (rather than app.main) so that route modules
can import `limiter` to decorate individual endpoints with @limiter.limit(...)
without creating a circular import with app.main (which imports the API
router, which imports the route modules).
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
