-- =============================================
-- Migration 004: Create Document Chunks Table
-- ForgeAI Enterprise AI Operations Copilot
-- =============================================
-- Stores text chunks with vector embeddings
-- for semantic similarity search.

CREATE TABLE IF NOT EXISTS public.document_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES public.documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(384),  -- bge-small-en-v1.5 outputs 384-dim vectors
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON public.document_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_chunk_index ON public.document_chunks(document_id, chunk_index);

-- HNSW index for fast approximate nearest neighbor search (cosine distance)
-- ef_construction and m are tuned for quality vs speed tradeoff
CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON public.document_chunks
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Unique constraint: one chunk index per document
ALTER TABLE public.document_chunks
    ADD CONSTRAINT uq_document_chunk_index UNIQUE (document_id, chunk_index);
