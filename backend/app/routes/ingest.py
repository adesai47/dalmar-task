from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import IngestRequest, IngestResponse
from app.services.vector_store import VectorStoreService

router = APIRouter()

def get_vector_service() -> VectorStoreService:
    from app.main import vector_service
    if not vector_service:
        raise HTTPException(status_code=500, detail="Vector service not initialized")
    return vector_service

@router.post("/ingest", response_model=IngestResponse)
async def ingest_documents(
    request: IngestRequest,
    vector_service: VectorStoreService = Depends(get_vector_service)
):
    """
    Ingest new documents into the vector store
    """
    try:
        ingested_count = await vector_service.add_documents(
            documents=request.documents,
            collection_name=request.collection_name
        )
        
        return IngestResponse(
            success=True,
            message=f"Successfully ingested {ingested_count} documents",
            documents_ingested=ingested_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@router.get("/ingest/status")
async def get_ingestion_status(
    vector_service: VectorStoreService = Depends(get_vector_service)
):
    """Get the current status of document ingestion"""
    try:
        status = await vector_service.get_collection_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")

