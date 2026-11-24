"""ForgeAI Schemas Package."""

from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, UserProfile
from app.schemas.chat import (
    ChatMessageResponse,
    ChatSessionDetailResponse,
    ChatSessionListResponse,
    ChatSessionResponse,
    CreateSessionRequest,
    SendMessageRequest,
    SendMessageResponse,
)
from app.schemas.common import (
    ErrorResponse,
    HealthResponse,
    MessageResponse,
    PaginatedResponse,
)
from app.schemas.document import (
    DocumentListResponse,
    DocumentResponse,
    DocumentStatusResponse,
    DocumentUploadResponse,
)

__all__ = [
    # Auth
    "RegisterRequest",
    "LoginRequest",
    "AuthResponse",
    "UserProfile",
    # Common
    "HealthResponse",
    "MessageResponse",
    "ErrorResponse",
    "PaginatedResponse",
    # Document
    "DocumentResponse",
    "DocumentListResponse",
    "DocumentStatusResponse",
    "DocumentUploadResponse",
    # Chat
    "ChatSessionResponse",
    "ChatSessionDetailResponse",
    "ChatSessionListResponse",
    "ChatMessageResponse",
    "CreateSessionRequest",
    "SendMessageRequest",
    "SendMessageResponse",
]
