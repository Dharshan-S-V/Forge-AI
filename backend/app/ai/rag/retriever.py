"""
ForgeAI RAG Retriever.

Retrieves relevant document chunks from PostgreSQL using pgvector cosine similarity.
"""

import asyncio
import uuid
from typing import Sequence

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.embeddings.service import EmbeddingService
from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.document import DocumentChunk, Document

logger = get_logger(__name__)


class VectorRetriever:
    """Retrieves document chunks using pgvector."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session
        self.settings = get_settings()

    async def search(self, user_id: uuid.UUID, query: str) -> list[dict]:
        """Search for relevant chunks across all documents belonging to a user.

        Args:
            user_id: The UUID of the user.
            query: The search query.

        Returns:
            List of dictionaries containing chunk content and metadata.
        """
        logger.info("Retrieving documents for query", query=query)
        
        # 1. Generate embedding for the query.
        # This runs on the live chat request path (not a background task), so
        # blocking the event loop here would stall every other concurrent
        # request on this worker.
        query_embeddings = await asyncio.to_thread(EmbeddingService.generate_embeddings, [query])
        if not query_embeddings:
            return []
        
        query_vector = query_embeddings[0]

        # 2. Perform vector search in pgvector using L2 distance (<->) or cosine (<=>)
        # We'll use cosine distance (<=>) for sentence-transformers
        # We only want chunks from documents that belong to this user
        
        vector_str = "[" + ",".join(map(str, query_vector)) + "]"
        
        stmt = text("""
            SELECT 
                dc.id, 
                dc.document_id,
                dc.content, 
                dc.metadata,
                d.filename,
                1 - (dc.embedding <=> :vector) AS similarity
            FROM document_chunks dc
            JOIN documents d ON dc.document_id = d.id
            WHERE d.user_id = :user_id
              AND d.status = 'completed'
            ORDER BY dc.embedding <=> :vector
            LIMIT :top_k
        """)

        result = await self.session.execute(
            stmt,
            {
                "vector": vector_str,
                "user_id": user_id,
                "top_k": self.settings.top_k_results
            }
        )
        
        rows = result.fetchall()
        
        chunks = []
        for row in rows:
            chunks.append({
                "chunk_id": str(row.id),
                "document_id": str(row.document_id),
                "filename": row.filename,
                "content": row.content,
                "similarity": float(row.similarity),
            })
            
        logger.info("Retrieved chunks", count=len(chunks))
        return chunks
