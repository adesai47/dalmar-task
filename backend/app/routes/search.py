from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import SearchRequest, SearchResponse
from app.services.vector_store import VectorStoreService
from app.services.web_search import WebSearchService
from app.services.rag_service import RAGService

router = APIRouter()

def get_vector_service() -> VectorStoreService:
    from app.main import vector_service
    if not vector_service:
        raise HTTPException(status_code=500, detail="Vector service not initialized")
    return vector_service

def get_web_search_service() -> WebSearchService:
    from app.main import web_search_service
    if not web_search_service:
        raise HTTPException(status_code=500, detail="Web search service not initialized")
    return web_search_service

@router.post("/search", response_model=SearchResponse)
async def search_documents(
    request: SearchRequest,
    vector_service: VectorStoreService = Depends(get_vector_service),
    web_search_service: WebSearchService = Depends(get_web_search_service)
):
    """
    Search for relevant documents using RAG architecture.
    Falls back to web search if no relevant documents are found.
    """
    try:
        rag_service = RAGService(vector_service, web_search_service)
        response = await rag_service.search(
            query=request.query,
            limit=request.limit,
            threshold=request.threshold,
            use_web_fallback=request.use_web_fallback
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/search/suggestions")
async def get_search_suggestions():
    """Get search suggestions for common healthcare queries"""
    suggestions = [
        "diabetes treatment guidelines",
        "hypertension management",
        "COVID-19 symptoms",
        "heart disease prevention",
        "mental health resources",
        "pediatric care protocols",
        "emergency medicine procedures",
        "pharmaceutical interactions"
    ]
    return {"suggestions": suggestions}

