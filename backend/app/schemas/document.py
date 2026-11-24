"""
ForgeAI Document Schemas.

Pydantic models for document upload, listing, and status responses.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import BaseSchema


class DocumentResponse(BaseSchema):
    """Document metadata response."""

    id: UUID
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    status: str
    chunk_count: int
    # The Document ORM model exposes this column via the Python attribute
    # `doc_metadata` (the DB column itself is named `metadata`). Without this
    # alias, from_attributes lookup of "metadata" silently misses and always
    # falls back to the default {} instead of the real value.
    metadata: dict = Field(default_factory=dict, validation_alias="doc_metadata")
    created_at: datetime
    updated_at: datetime


class DocumentListResponse(BaseModel):
    """Paginated document list."""

    documents: list[DocumentResponse]
    total: int


class DocumentStatusResponse(BaseModel):
    """Document processing status."""

    id: UUID
    status: str
    chunk_count: int
    processing_error: str | None = None


class DocumentUploadResponse(BaseModel):
    """Response after successful document upload."""

    id: UUID
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    status: str
    message: str = "Document uploaded successfully. Processing will begin shortly."
