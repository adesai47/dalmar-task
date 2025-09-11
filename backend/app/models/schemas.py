from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class Document(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]
    source: str
    created_at: datetime

class SearchRequest(BaseModel):
    query: str
    limit: int = 5
    threshold: float = 0.7
    use_web_fallback: bool = True

class SearchResult(BaseModel):
    document: Document
    similarity_score: float
    source: str

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_found: int
    used_web_fallback: bool
    web_results: Optional[List[Dict[str, Any]]] = None

class IngestRequest(BaseModel):
    documents: List[Dict[str, Any]]
    collection_name: Optional[str] = "healthcare_docs"

class IngestResponse(BaseModel):
    success: bool
    message: str
    documents_ingested: int

