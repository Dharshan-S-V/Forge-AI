-- =============================================
-- Migration 003: Create Documents Table
-- ForgeAI Enterprise AI Operations Copilot
-- =============================================

CREATE TABLE IF NOT EXISTS public.documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    file_type TEXT NOT NULL CHECK (file_type IN ('pdf', 'docx', 'txt', 'xlsx')),
    file_size BIGINT NOT NULL CHECK (file_size > 0),
    storage_path TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'uploaded' CHECK (
        status IN ('uploaded', 'processing', 'completed', 'failed')
    ),
    chunk_count INTEGER DEFAULT 0,
    processing_error TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON public.documents(user_id);
CREATE INDEX IF NOT EXISTS idx_documents_status ON public.documents(status);
CREATE INDEX IF NOT EXISTS idx_documents_created_at ON public.documents(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_documents_file_type ON public.documents(file_type);

-- Auto-update updated_at
CREATE TRIGGER set_documents_updated_at
    BEFORE UPDATE ON public.documents
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();
