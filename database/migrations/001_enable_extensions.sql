-- =============================================
-- Migration 001: Enable Required Extensions
-- ForgeAI Enterprise AI Operations Copilot
-- =============================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pgvector for embedding storage and similarity search
CREATE EXTENSION IF NOT EXISTS "vector";

-- Enable pg_trgm for text search optimization
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
