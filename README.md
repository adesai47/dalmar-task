# Healthcare Document Search & AI Chat

A comprehensive RAG (Retrieval-Augmented Generation) system for healthcare documents with AI-powered chat capabilities.

## Quick Start

1. **Start everything:**
   ```bash
   ./start.sh
   ```

2. **Open your browser:**
   - Frontend: http://localhost:3000
   - Chat Interface: http://localhost:3000/chat
   - API Docs: http://localhost:8000/docs

## What it does

### 🔍 Document Search
- Search through healthcare documents using vector similarity
- Find relevant medical information quickly
- Includes documents about diabetes, heart disease, mental health, and more

### 🤖 AI Chat Assistant
- **Streaming Chat Interface** - Real-time AI responses
- **RAG-Powered** - Uses retrieved documents as context for accurate answers
- **Web Search Fallback** - Automatically supplements with web search when needed
- **Azure OpenAI Integration** - Powered by GPT-4o-mini for intelligent responses

## Features

### Chat Interface
- ✅ **Real-time Streaming** - Watch responses generate token by token
- ✅ **Context Awareness** - Uses retrieved documents for accurate answers
- ✅ **Image Upload & Analysis** - Upload images and get AI analysis
- ✅ **Image Rendering** - Display images in chat messages
- ✅ **Web Search Integration** - Falls back to web search when needed
- ✅ **Chat History** - Maintains conversation context

### Document Search
- ✅ **Vector Similarity Search** - ChromaDB with sentence transformers
- ✅ **Healthcare Focus** - Pre-loaded with medical documents
- ✅ **Web Search Fallback** - DuckDuckGo integration for additional results

## Try these queries:

### In Chat Interface:
- "What are the symptoms of diabetes?"
- "How do I manage hypertension?"
- "Explain COVID-19 prevention methods"
- "What are the signs of heart disease?"
- **Upload medical images** and ask questions like:
  - "What do you see in this X-ray?"
  - "Can you analyze this medical chart?"
  - "What might this skin condition be?"

### In Document Search:
- "diabetes treatment"
- "hypertension management" 
- "mental health"
- "COVID-19 symptoms"
- "heart disease prevention"

## Tech Stack

- **Frontend:** Next.js + TypeScript + Tailwind CSS
- **Backend:** Python + FastAPI + Azure OpenAI
- **Database:** ChromaDB (vector search)
- **AI:** Azure OpenAI GPT-4o-mini
- **Search:** DuckDuckGo API for web fallback

## API Endpoints

### Chat Endpoints
- `POST /api/chat/stream` - Streaming chat with RAG
- `POST /api/chat` - Non-streaming chat for testing
- `GET /api/chat/test` - Azure OpenAI connection test

### Search Endpoints
- `POST /api/search` - Document search with vector similarity
- `GET /api/search/suggestions` - Get search suggestions

### Utility Endpoints
- `GET /api/health` - Health check
- `POST /api/ingest` - Ingest new documents

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

## Architecture

```
Frontend (Next.js) ←→ Backend (FastAPI) ←→ Azure OpenAI
                              ↓
                    Vector Store (ChromaDB)
                              ↓
                    Web Search (DuckDuckGo)
```

The system uses RAG (Retrieval-Augmented Generation) to provide accurate, context-aware responses by:
1. Retrieving relevant documents from the vector store
2. Supplementing with web search if needed
3. Using the retrieved context to generate intelligent responses with Azure OpenAI

That's it! 🚀