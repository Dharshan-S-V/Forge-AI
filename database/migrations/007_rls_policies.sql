-- =============================================
-- Migration 007: Row Level Security Policies
-- ForgeAI Enterprise AI Operations Copilot
-- =============================================
-- RLS ensures users can only access their own data.
-- Service role key bypasses RLS for backend operations.

-- =============================================
-- Users Table
-- =============================================
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
    ON public.users FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON public.users FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

-- =============================================
-- Documents Table
-- =============================================
ALTER TABLE public.documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own documents"
    ON public.documents FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own documents"
    ON public.documents FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own documents"
    ON public.documents FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own documents"
    ON public.documents FOR DELETE
    USING (auth.uid() = user_id);

-- =============================================
-- Document Chunks Table
-- =============================================
ALTER TABLE public.document_chunks ENABLE ROW LEVEL SECURITY;

-- Users can view chunks of their own documents
CREATE POLICY "Users can view own document chunks"
    ON public.document_chunks FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.documents
            WHERE documents.id = document_chunks.document_id
            AND documents.user_id = auth.uid()
        )
    );

-- Insert/delete managed by service role (backend)
CREATE POLICY "Service role manages chunks"
    ON public.document_chunks FOR ALL
    USING (auth.role() = 'service_role');

-- =============================================
-- Chat Sessions Table
-- =============================================
ALTER TABLE public.chat_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own chat sessions"
    ON public.chat_sessions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create own chat sessions"
    ON public.chat_sessions FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own chat sessions"
    ON public.chat_sessions FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own chat sessions"
    ON public.chat_sessions FOR DELETE
    USING (auth.uid() = user_id);

-- =============================================
-- Chat Messages Table
-- =============================================
ALTER TABLE public.chat_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own chat messages"
    ON public.chat_messages FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.chat_sessions
            WHERE chat_sessions.id = chat_messages.session_id
            AND chat_sessions.user_id = auth.uid()
        )
    );

-- Insert managed by service role (backend creates assistant messages)
CREATE POLICY "Service role manages messages"
    ON public.chat_messages FOR ALL
    USING (auth.role() = 'service_role');

-- =============================================
-- Activity Logs Table
-- =============================================
ALTER TABLE public.activity_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own activity logs"
    ON public.activity_logs FOR SELECT
    USING (auth.uid() = user_id);

-- Insert managed by service role (backend logs activity)
CREATE POLICY "Service role manages activity logs"
    ON public.activity_logs FOR ALL
    USING (auth.role() = 'service_role');
