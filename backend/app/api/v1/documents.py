"""
ForgeAI Documents API Routes.

Document upload, listing, deletion, and status routes.
"""

import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_db
from app.schemas.common import MessageResponse
from app.schemas.document import DocumentListResponse, DocumentResponse, DocumentUploadResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a document",
)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> DocumentUploadResponse:
    """Upload a document and start processing in the background."""
    service = DocumentService(db)
    doc = await service.upload_document(uuid.UUID(user_id), file, background_tasks)
    
    return DocumentUploadResponse(
        id=doc.id,
        filename=doc.filename,
        original_filename=doc.original_filename,
        file_type=doc.file_type,
        file_size=doc.file_size,
        status=doc.status,
    )


@router.get(
    "",
    response_model=DocumentListResponse,
    summary="List user's documents",
)
async def list_documents(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> DocumentListResponse:
    """List all documents uploaded by the current user."""
    service = DocumentService(db)
    docs = await service.get_user_documents(uuid.UUID(user_id))
    
    return DocumentListResponse(
        documents=[
            DocumentResponse.model_validate(doc) for doc in docs
        ],
        total=len(docs)
    )


@router.delete(
    "/{document_id}",
    response_model=MessageResponse,
    summary="Delete a document",
)
async def delete_document(
    document_id: uuid.UUID,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """Delete a document by ID."""
    service = DocumentService(db)
    await service.delete_document(uuid.UUID(user_id), document_id)
    return MessageResponse(message="Document deleted successfully")
