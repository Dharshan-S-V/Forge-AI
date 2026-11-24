# ForgeAI – Enterprise AI Operations Copilot

<div align="center">

**An enterprise AI platform for document-powered knowledge retrieval using RAG.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?style=flat-square&logo=next.js)](https://nextjs.org)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3FCF8E?style=flat-square&logo=supabase)](https://supabase.com)
[![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=flat-square&logo=google)](https://ai.google.dev)

</div>

---

## Overview

ForgeAI enables organizations to upload documents and interact with company knowledge using AI. The system uses **Retrieval-Augmented Generation (RAG)** to ensure answers are grounded exclusively in uploaded documents — no hallucinations, no fabricated answers.

### Key Features (Phase 1 MVP)

- **Secure Authentication** — Register, login, logout with Supabase Auth
- **Document Upload** — PDF, DOCX, TXT, XLSX with drag-and-drop UI
- **AI-Powered Chat** — ChatGPT-like interface with source citations
- **RAG Pipeline** — Semantic search + Gemini for grounded answers
- **Dashboard** — Usage statistics, recent chats, document overview
- **Dark/Light Mode** — Enterprise-grade responsive design

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, React, TypeScript, Tailwind CSS, Shadcn UI |
| Backend | FastAPI, Python, Pydantic, SQLAlchemy |
| Auth | Supabase Auth |
| Database | Supabase PostgreSQL + pgvector |
| Storage | Supabase Storage |
| AI | Google Gemini, LangChain, LangGraph |
| Embeddings | BAAI/bge-small-en-v1.5 (Sentence Transformers) |
| OCR | PaddleOCR (optional) |

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- A [Supabase](https://supabase.com) project
- A [Google Gemini API key](https://aistudio.google.com)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/forge-ai.git
cd forge-ai

# Copy environment files
cp .env.example .env
# Edit .env with your actual keys

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (in a new terminal)
cd frontend
npm install
npm run dev
```

### Run with Docker

```bash
cd docker
docker-compose up --build
```

## Project Structure

```
forge-ai/
├── frontend/          # Next.js application
├── backend/           # FastAPI application
├── database/          # SQL migration scripts
├── docker/            # Docker configuration
├── docs/              # Documentation
├── .env.example       # Environment variable template
└── README.md
```

## Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [API Documentation](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## License

MIT
