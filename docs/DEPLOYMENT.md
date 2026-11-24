# ForgeAI Deployment Guide

## Frontend — Vercel

### Setup

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com) and import the repository
3. Set the **Root Directory** to `frontend/`
4. Add environment variables:
   ```
   NEXT_PUBLIC_SUPABASE_URL=<YOUR_URL>
   NEXT_PUBLIC_SUPABASE_ANON_KEY=<YOUR_KEY>
   NEXT_PUBLIC_BACKEND_URL=<YOUR_RENDER_URL>
   ```
5. Deploy

### Settings

- **Framework**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Node.js Version**: 20.x

---

## Backend — Render

### Setup

1. Go to [render.com](https://render.com) and create a new **Web Service**
2. Connect your GitHub repository
3. Set the **Root Directory** to `backend/`
4. Configure:
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   ```
   SUPABASE_URL=<YOUR_URL>
   SUPABASE_ANON_KEY=<YOUR_KEY>
   SUPABASE_SERVICE_ROLE_KEY=<YOUR_KEY>
   DATABASE_URL=<YOUR_DATABASE_URL>
   GEMINI_API_KEY=<YOUR_KEY>
   ENVIRONMENT=production
   LOG_LEVEL=WARNING
   FRONTEND_URL=<YOUR_VERCEL_URL>
   ```
6. Deploy

### Health Check

Set the health check path to `/health`.

---

## Database — Supabase

Your Supabase project is already hosted. Ensure:

1. All migrations have been run
2. `pgvector` extension is enabled
3. RLS policies are in place
4. Storage bucket `documents` exists (private)

---

## Post-Deployment Checklist

- [ ] Backend health check returns `200 OK`
- [ ] Frontend loads without errors
- [ ] CORS is configured for production frontend URL
- [ ] Registration and login work
- [ ] Document upload works
- [ ] Chat produces grounded answers
- [ ] Swagger docs are disabled in production
