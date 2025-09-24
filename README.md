# Healthcare Document Search

A simple search system for healthcare documents using AI-powered retrieval.

## Quick Start

1. **Start everything:**
   ```bash
   ./start.sh
   ```

2. **Open your browser:**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

## What it does

- Search through healthcare documents using AI
- Find relevant medical information quickly
- Includes documents about diabetes, heart disease, mental health, and more

## Try searching for:

- "diabetes treatment"
- "hypertension management" 
- "mental health"
- "COVID-19 symptoms"
- "heart disease prevention"

## Tech Stack

- **Frontend:** Next.js + TypeScript
- **Backend:** Python + FastAPI
- **Database:** ChromaDB (vector search)

## Manual Setup

If the startup script doesn't work:

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

That's it! 🚀