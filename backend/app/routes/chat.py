from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest, ChatResponse
from app.services.vector_store import VectorStoreService
from app.services.web_search import WebSearchService
from app.services.rag_service import RAGService
from app.services.azure_openai_service import AzureOpenAIService
import json
import asyncio
from typing import AsyncGenerator

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

def get_azure_openai_service() -> AzureOpenAIService:
    return AzureOpenAIService()

async def generate_chat_stream(
    query: str,
    rag_service: RAGService,
    openai_service: AzureOpenAIService,
    chat_history: list = None,
    use_web_fallback: bool = True,
    images: list = None
) -> AsyncGenerator[str, None]:
    """
    Generate a streaming chat response using RAG + Azure OpenAI
    """
    try:
        # Step 1: Search for relevant documents using RAG
        search_response = await rag_service.search(
            query=query,
            limit=5,
            threshold=0.6,
            use_web_fallback=use_web_fallback
        )
        
        # Step 2: Extract context documents
        context_documents = []
        for result in search_response.results:
            context_documents.append({
                "content": result.document.content,
                "metadata": result.document.metadata,
                "similarity_score": result.similarity_score,
                "source": result.source
            })
        
        # Step 3: Send initial metadata
        metadata = {
            "type": "metadata",
            "data": {
                "context_documents_count": len(context_documents),
                "used_web_fallback": search_response.used_web_fallback,
                "total_found": search_response.total_found
            }
        }
        yield f"data: {json.dumps(metadata)}\n\n"
        
        # Step 4: Stream the AI response
        yield f"data: {json.dumps({'type': 'start', 'data': 'Generating response...'})}\n\n"
        
        async for chunk in openai_service.generate_response(
            query=query,
            context_documents=context_documents,
            chat_history=chat_history,
            images=images
        ):
            chunk_data = {
                "type": "content",
                "data": chunk
            }
            yield f"data: {json.dumps(chunk_data)}\n\n"
            await asyncio.sleep(0.01)  # Small delay to prevent overwhelming
        
        # Step 5: Send completion signal
        completion_data = {
            "type": "complete",
            "data": {
                "context_documents": context_documents,
                "used_web_fallback": search_response.used_web_fallback
            }
        }
        yield f"data: {json.dumps(completion_data)}\n\n"
        
    except Exception as e:
        error_data = {
            "type": "error",
            "data": {"error": str(e)}
        }
        yield f"data: {json.dumps(error_data)}\n\n"

@router.post("/chat/stream")
async def stream_chat(
    request: ChatRequest,
    vector_service: VectorStoreService = Depends(get_vector_service),
    web_search_service: WebSearchService = Depends(get_web_search_service),
    openai_service: AzureOpenAIService = Depends(get_azure_openai_service)
):
    """
    Stream a chat response using RAG + Azure OpenAI
    """
    try:
        rag_service = RAGService(vector_service, web_search_service)
        
        # Create streaming response
        async def event_generator():
            async for chunk in generate_chat_stream(
                query=request.query,
                rag_service=rag_service,
                openai_service=openai_service,
                chat_history=request.chat_history,
                use_web_fallback=request.use_web_fallback,
                images=request.images
            ):
                yield chunk
        
        return StreamingResponse(
            event_generator(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream",
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat streaming failed: {str(e)}")

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    vector_service: VectorStoreService = Depends(get_vector_service),
    web_search_service: WebSearchService = Depends(get_web_search_service),
    openai_service: AzureOpenAIService = Depends(get_azure_openai_service)
):
    """
    Non-streaming chat endpoint for testing
    """
    try:
        rag_service = RAGService(vector_service, web_search_service)
        
        # Search for relevant documents
        search_response = await rag_service.search(
            query=request.query,
            limit=5,
            threshold=0.6,
            use_web_fallback=request.use_web_fallback
        )
        
        # Extract context documents
        context_documents = []
        for result in search_response.results:
            context_documents.append({
                "content": result.document.content,
                "metadata": result.document.metadata,
                "similarity_score": result.similarity_score,
                "source": result.source
            })
        
        # Generate response
        response_text = await openai_service.generate_non_streaming_response(
            query=request.query,
            context_documents=context_documents,
            chat_history=request.chat_history,
            images=request.images
        )
        
        # Extract images if any
        images = await openai_service.extract_images_from_response(response_text)
        
        return ChatResponse(
            query=request.query,
            response=response_text,
            context_documents=context_documents,
            used_web_fallback=search_response.used_web_fallback,
            images=images,
            total_context_found=len(context_documents)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@router.get("/chat/test")
async def test_azure_openai(
    openai_service: AzureOpenAIService = Depends(get_azure_openai_service)
):
    """
    Test Azure OpenAI connection
    """
    return await openai_service.test_connection()

@router.get("/chat/health")
async def chat_health():
    """
    Health check for chat service
    """
    return {
        "status": "healthy",
        "service": "chat",
        "features": ["streaming", "rag_integration", "web_fallback"]
    }
