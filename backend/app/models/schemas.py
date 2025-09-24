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

# Chat-related schemas
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None
    images: Optional[List[str]] = None  # Base64 encoded images

class ChatRequest(BaseModel):
    query: str
    chat_history: Optional[List[ChatMessage]] = []
    use_web_fallback: bool = True
    stream: bool = False
    images: Optional[List[str]] = None  # Base64 encoded images

class ChatResponse(BaseModel):
    query: str
    response: str
    context_documents: List[Dict[str, Any]]
    used_web_fallback: bool
    images: List[str] = []
    total_context_found: int
    timestamp: str = datetime.now().isoformat()

class ChatStreamEvent(BaseModel):
    type: str  # "metadata", "start", "content", "complete", "error"
    data: Dict[str, Any]

