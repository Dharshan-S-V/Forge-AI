# ForgeAI Architecture

## System Overview

ForgeAI follows **Clean Architecture** with four distinct layers to ensure maintainability, testability, and separation of concerns.

```mermaid
graph TB
    subgraph "Presentation Layer"
        FE["Frontend (Next.js)"]
        API["FastAPI Routers"]
    end

    subgraph "Application Layer"
        AS["Auth Service"]
        DS["Document Service"]
        CS["Chat Service"]
        SS["Storage Service"]
    end

    subgraph "Domain Layer"
        UM["User Model"]
        DM["Document Model"]
        CM["Chat Model"]
        DC["DocumentChunk Model"]
    end

    subgraph "Infrastructure Layer"
        SB["Supabase Client"]
        DB["PostgreSQL + pgvector"]
        ST["Supabase Storage"]
        GM["Gemini API"]
        EM["Embedding Model"]
    end

    FE -->|REST API| API
    API --> AS & DS & CS
    AS & DS & CS --> UM & DM & CM & DC
    AS --> SB
    DS --> DB & ST & EM
    CS --> DB & GM
```

## Data Flow: RAG Pipeline

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant API as FastAPI
    participant RAG as RAG Pipeline
    participant VS as pgvector
    participant LLM as Gemini

    U->>FE: Ask question
    FE->>API: POST /chat/sessions/{id}/messages
    API->>RAG: Process query
    RAG->>VS: Similarity search (top-K)
    VS-->>RAG: Relevant chunks
    RAG->>LLM: Query + context
    LLM-->>RAG: Grounded answer
    RAG-->>API: Answer + sources
    API-->>FE: Response
    FE-->>U: Display answer with citations
```

## Directory Layout

| Directory | Purpose |
|---|---|
| `frontend/` | Next.js app with TypeScript, Tailwind, Shadcn UI |
| `backend/app/api/` | Presentation layer — FastAPI route handlers |
| `backend/app/services/` | Application layer — business logic orchestration |
| `backend/app/models/` | Domain layer — SQLAlchemy ORM models |
| `backend/app/db/` | Infrastructure — database sessions, Supabase clients |
| `backend/app/ai/` | AI engine — RAG pipeline, embeddings, agents |
| `database/migrations/` | SQL migration scripts for Supabase PostgreSQL |
| `docker/` | Docker Compose and Dockerfiles |

## Security

- JWT-based authentication via Supabase Auth
- Row Level Security (RLS) on all database tables
- File type and size validation on uploads
- Input sanitization on all user inputs
- CORS restricted to frontend origin
- Environment variables for all secrets
