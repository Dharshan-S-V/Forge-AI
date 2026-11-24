# ForgeAI – Enterprise AI Operations Copilot Manual

Welcome to ForgeAI! This manual explains how to set up, run, and use the platform.

ForgeAI is an enterprise-grade AI assistant that uses Retrieval-Augmented Generation (RAG) to let you "chat" with your uploaded company documents. It strictly answers questions based *only* on the documents you upload, eliminating AI hallucinations.

---

## 1. Prerequisites

Before running ForgeAI locally, you must have the following installed:
* **Python 3.10+**
* **Node.js 18+**
* **Git**
* **A Supabase Project**: You need a free Supabase account to host the PostgreSQL database and manage authentication.

---

## 2. Initial Setup

### A. Environment Variables
You must set up environment variables for both the backend and frontend.

1. **Backend**: Open `backend/.env` (create it if it doesn't exist by copying `.env.example`).
   Fill in the following details:
   ```env
   # Database (From Supabase Dashboard -> Project Settings -> Database)
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[your-project-ref].supabase.co:5432/postgres

   # Supabase Keys (From Supabase Dashboard -> Project Settings -> API)
   SUPABASE_URL=https://[your-project-ref].supabase.co
   SUPABASE_ANON_KEY=ey...
   SUPABASE_SERVICE_ROLE_KEY=ey...

   # AI Keys
   GEMINI_API_KEY=your-google-gemini-api-key
   ```

2. **Frontend**: Open `frontend/.env` (create it if it doesn't exist by copying `.env.example`).
   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://[your-project-ref].supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=ey...
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   ```

### B. Database Setup (Supabase)
To set up your database schema, you must run the SQL scripts located in the `database/migrations/` folder.
1. Log into your Supabase Dashboard.
2. Go to the **SQL Editor**.
3. Create a new query and paste the contents of each file from `database/migrations/` in order (from `001_` to `007_`), and click **Run**.

---

## 3. How to Run the Project

Since we are running this locally without Docker, you need to open **two separate terminal windows**.

### Terminal 1: Start the Backend (FastAPI)
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   *The backend will now be running at `http://localhost:8000`.*

### Terminal 2: Start the Frontend (Next.js)
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install the dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   *The frontend will now be running at `http://localhost:3000`.*

---

## 4. How to Use ForgeAI

1. **Access the App**: Open your browser and go to `http://localhost:3000`.
2. **Register/Login**: Click "Sign Up" to create an account. Once registered, log in.
3. **Upload Documents**:
   * Navigate to the **Documents** tab on the sidebar.
   * Click **Upload Document**.
   * Select a PDF, Word document, Excel file, or Text file.
   * *What happens next?* The backend will automatically extract the text, split it into chunks, convert those chunks into AI embeddings, and save them to the database. Wait for the status to turn green/completed.
4. **Chat with your Data**:
   * Navigate to the **Chat** tab.
   * Ask a question related to the document you just uploaded (e.g., *"What is the main policy mentioned in the handbook?"*).
   * The AI will retrieve the exact paragraphs from your document and generate a factual answer, citing the document it used.

## 5. Troubleshooting
* **Database Errors / Authentication Issues**: Double-check your `.env` files. Ensure you are using the `service_role` key in the backend, and the `anon` key in the frontend.
* **Model Not Found**: Ensure you have generated a free API key from Google AI Studio and placed it in `GEMINI_API_KEY`.
