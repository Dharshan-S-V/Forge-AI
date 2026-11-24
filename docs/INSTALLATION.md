# ForgeAI Installation Guide

## Prerequisites

- **Python** 3.11 or higher
- **Node.js** 20 or higher
- **npm** 10 or higher
- A **Supabase** project ([create one here](https://supabase.com))
- A **Google Gemini API key** ([get one here](https://aistudio.google.com))

## Step 1: Clone & Setup Environment

```bash
git clone https://github.com/your-org/forge-ai.git
cd forge-ai
cp .env.example .env
```

Edit `.env` and fill in your actual keys:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
DATABASE_URL=postgresql://postgres:password@db.your-project.supabase.co:5432/postgres
GEMINI_API_KEY=your-gemini-api-key
```

## Step 2: Run Database Migrations

In the Supabase SQL Editor (Dashboard → SQL Editor), run each migration file in order:

1. `database/migrations/001_enable_extensions.sql`
2. `database/migrations/002_create_users.sql`
3. `database/migrations/003_create_documents.sql`
4. `database/migrations/004_create_chunks.sql`
5. `database/migrations/005_create_chats.sql`
6. `database/migrations/006_create_activity_logs.sql`
7. `database/migrations/007_rls_policies.sql`

## Step 3: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy env file
cp .env.example .env
# Edit with your actual keys

# Run the server
uvicorn app.main:app --reload --port 8000
```

Verify: Open http://localhost:8000/health — you should see:
```json
{"status": "healthy", "version": "0.1.0", "environment": "development"}
```

## Step 4: Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run the dev server
npm run dev
```

Verify: Open http://localhost:3000

## Step 5: Create Supabase Storage Bucket

In Supabase Dashboard → Storage:

1. Create a new bucket named `documents`
2. Set it to **private** (not public)
3. Add a policy to allow authenticated users to upload to their own folder

## Docker (Alternative)

```bash
cd docker
docker-compose up --build
```

This starts both frontend (port 3000) and backend (port 8000).
