"""
ForgeAI – Enterprise AI Operations Copilot.

FastAPI application factory with CORS, structured logging, and health check.
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.router import api_router
from app.core.config import get_settings
from app.core.limiter import limiter
from app.core.logging import get_logger, setup_logging
from app.schemas.common import HealthResponse

# Initialize logging before anything else
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager.

    Handles startup and shutdown events.
    """
    settings = get_settings()
    logger.info(
        "ForgeAI starting",
        version=settings.app_version,
        environment=settings.environment,
    )
    yield
    logger.info("ForgeAI shutting down")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Enterprise AI Operations Copilot — RAG-powered document intelligence",
        version=settings.app_version,
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        lifespan=lifespan,
    )

    # ── Rate Limiting ────────────────────────────────────────
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # ── CORS ─────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routes ───────────────────────────────────────────────
    app.include_router(api_router)

    # ── Health Check ─────────────────────────────────────────
    @app.get(
        "/health",
        response_model=HealthResponse,
        tags=["System"],
        summary="Health check",
    )
    async def health_check() -> HealthResponse:
        """Check if the application is running and healthy."""
        return HealthResponse(
            status="healthy",
            version=settings.app_version,
            environment=settings.environment,
        )

    # ── Global Exception Handler ─────────────────────────────
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):  # noqa: ANN001
        logger.error(
            "Unhandled exception",
            path=str(request.url),
            method=request.method,
            error=str(exc),
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "detail": str(exc) if settings.is_development else None,
            },
        )

    return app


# Create the application instance
app = create_app()
