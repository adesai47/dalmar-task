# RAG Retrieval System Architecture

## Overview

The RAG (Retrieval-Augmented Generation) system is designed to retrieve relevant healthcare documents from a vector database and supplement the search with web search when needed. The system consists of a Next.js frontend and a Python FastAPI backend.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Search    │  │   Results   │  │ Suggestions │             │
│  │    Bar      │  │   Display    │  │   Panel     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP/REST API
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Search    │  │   RAG       │  │   Web       │             │
│  │   Routes    │  │  Service    │  │  Search     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Vector Database (ChromaDB)                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Document   │  │  Embeddings │  │  Similarity  │             │
│  │   Storage   │  │   (BERT)    │  │   Search     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Fallback
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Web Search Service                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ DuckDuckGo  │  │  Healthcare │  │   General   │             │
│  │    API      │  │   Sources   │  │   Search    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### Frontend (Next.js + TypeScript)

**Technology Stack:**
- Next.js 14 with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- React Query for API state management
- Lucide React for icons

**Key Components:**
- `SearchBar`: Input component for user queries
- `SearchResults`: Display component for search results
- `SearchSuggestions`: Pre-defined search suggestions
- `Header`: Navigation and branding

**Features:**
- Real-time search with loading states
- Responsive design for all devices
- Error handling and user feedback
- Search suggestions for common queries

### Backend (Python + FastAPI)

**Technology Stack:**
- FastAPI for REST API
- ChromaDB for vector storage
- Sentence Transformers for embeddings
- BeautifulSoup for web scraping
- Async/await for performance

**Key Services:**
- `VectorStoreService`: Manages ChromaDB operations
- `WebSearchService`: Handles web search fallback
- `RAGService`: Orchestrates the retrieval workflow

**API Endpoints:**
- `POST /api/search`: Main search endpoint
- `GET /api/health`: Health check
- `POST /api/ingest`: Document ingestion
- `GET /api/search/suggestions`: Search suggestions

### Vector Database (ChromaDB)

**Features:**
- Persistent storage with automatic persistence
- Cosine similarity search
- Metadata filtering
- Collection management

**Embedding Model:**
- `all-MiniLM-L6-v2` from Sentence Transformers
- 384-dimensional embeddings
- Optimized for semantic similarity

### Web Search Service

**Search Sources:**
1. DuckDuckGo Instant Answer API (primary)
2. Healthcare-specific sources (CDC, NIH, Mayo Clinic)
3. General web search (fallback)

**Features:**
- Healthcare-focused filtering
- Content extraction and cleaning
- Rate limiting and error handling

## Data Flow

1. **User Query**: User enters search query in frontend
2. **API Request**: Frontend sends POST request to `/api/search`
3. **Vector Search**: Backend searches ChromaDB for similar documents
4. **Threshold Check**: If results meet similarity threshold, return them
5. **Web Fallback**: If insufficient results, perform web search
6. **Result Combination**: Combine vector and web results
7. **Response**: Return formatted results to frontend
8. **Display**: Frontend renders results with metadata and sources

## Healthcare Dataset

**Pre-loaded Documents:**
- Diabetes management guidelines
- Hypertension treatment protocols
- COVID-19 clinical information
- Heart disease prevention
- Mental health resources
- Pediatric care protocols
- Emergency medicine procedures
- Drug interaction information
- Cancer screening guidelines
- Chronic kidney disease management

**Document Structure:**
```json
{
  "content": "Document text content...",
  "metadata": {
    "title": "Document title",
    "category": "Medical specialty",
    "source": "Source organization",
    "keywords": ["keyword1", "keyword2"]
  }
}
```

## Scalability Considerations

**Horizontal Scaling:**
- Stateless backend services
- Load balancer support
- Database sharding capabilities

**Performance Optimizations:**
- Async/await throughout
- Connection pooling
- Caching strategies
- Embedding model optimization

**Monitoring:**
- Health check endpoints
- Search analytics
- Error tracking
- Performance metrics

## Security Features

- CORS configuration
- Input validation
- Error handling
- Rate limiting
- Secure API endpoints

## Deployment

**Development:**
- Local development with hot reload
- Docker support (optional)
- Environment configuration

**Production:**
- Containerized deployment
- Environment variables
- Database persistence
- Load balancing ready

