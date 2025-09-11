from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from app.routes import search, health, ingest
from app.services.vector_store import VectorStoreService
from app.services.web_search import WebSearchService

# Global services
vector_service = None
web_search_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global vector_service, web_search_service
    vector_service = VectorStoreService()
    web_search_service = WebSearchService()
    
    # Initialize services
    await vector_service.initialize()
    await web_search_service.initialize()
    
    yield
    
    # Shutdown
    if vector_service:
        await vector_service.close()
    if web_search_service:
        await web_search_service.close()

app = FastAPI(
    title="RAG Retrieval System",
    description="A RAG system for healthcare document retrieval with web search fallback",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(ingest.router, prefix="/api", tags=["ingest"])

@app.get("/")
async def root():
    return {"message": "RAG Retrieval System API", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
