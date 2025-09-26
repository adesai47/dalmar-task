from typing import List, Dict, Any, Optional
from app.models.schemas import SearchResponse, SearchResult, Document
from app.services.vector_store import VectorStoreService
from app.services.web_search import WebSearchService
from datetime import datetime

class RAGService:
    def __init__(self, vector_service: VectorStoreService, web_search_service: WebSearchService):
        self.vector_service = vector_service
        self.web_search_service = web_search_service
    
    async def search(
        self, 
        query: str, 
        limit: int = 5, 
        threshold: float = 0.3, 
        use_web_fallback: bool = True
    ) -> SearchResponse:
        """
        Main RAG search method that combines vector search with web search fallback
        """
        try:
            # Step 1: Search vector store
            vector_results = await self.vector_service.search(query, limit, threshold)
            
            # Step 2: Check if we have sufficient results
            if len(vector_results) >= limit or not use_web_fallback:
                return SearchResponse(
                    query=query,
                    results=[self._format_search_result(result) for result in vector_results],
                    total_found=len(vector_results),
                    used_web_fallback=False,
                    web_results=None
                )
            
            # Step 3: Use web search as fallback
            web_results = await self.web_search_service.search(query, limit - len(vector_results))
            
            # Step 4: Combine results
            all_results = vector_results.copy()
            
            # Add web results as additional context
            for web_result in web_results:
                web_document = Document(
                    id=f"web_{len(all_results)}",
                    content=web_result["content"],
                    metadata={
                        "title": web_result["title"],
                        "source": web_result["source"],
                        "url": web_result.get("url", ""),
                        "type": "web_search"
                    },
                    source=web_result["source"],
                    created_at=datetime.now().isoformat()
                )
                
                all_results.append({
                    "document": web_document,
                    "similarity_score": 0.5,  # Default score for web results
                    "source": "web_search"
                })
            
            return SearchResponse(
                query=query,
                results=[self._format_search_result(result) for result in all_results],
                total_found=len(all_results),
                used_web_fallback=len(web_results) > 0,
                web_results=web_results
            )
            
        except Exception as e:
            # Fallback to web search only if vector search fails
            if use_web_fallback:
                try:
                    web_results = await self.web_search_service.search(query, limit)
                    return SearchResponse(
                        query=query,
                        results=[self._format_web_result(result) for result in web_results],
                        total_found=len(web_results),
                        used_web_fallback=True,
                        web_results=web_results
                    )
                except Exception as web_error:
                    raise Exception(f"Both vector search and web search failed: {str(e)}, {str(web_error)}")
            else:
                raise Exception(f"Vector search failed: {str(e)}")
    
    def _format_search_result(self, result: Dict[str, Any]) -> SearchResult:
        """Format a search result from vector store"""
        return SearchResult(
            document=result["document"],
            similarity_score=result["similarity_score"],
            source=result["source"]
        )
    
    def _format_web_result(self, result: Dict[str, Any]) -> SearchResult:
        """Format a web search result"""
        document = Document(
            id=f"web_{hash(result['content'])}",
            content=result["content"],
            metadata={
                "title": result["title"],
                "source": result["source"],
                "url": result.get("url", ""),
                "type": "web_search"
            },
            source=result["source"],
            created_at=datetime.now().isoformat()
        )
        
        return SearchResult(
            document=document,
            similarity_score=0.5,  # Default score for web results
            source="web_search"
        )
    
    async def get_search_analytics(self, query: str) -> Dict[str, Any]:
        """Get analytics about search performance"""
        try:
            # Get vector store status
            vector_status = await self.vector_service.get_collection_status()
            
            # Perform a test search to get metrics
            start_time = datetime.now()
            results = await self.search(query, limit=5, threshold=0.3)
            end_time = datetime.now()
            
            search_time = (end_time - start_time).total_seconds()
            
            return {
                "query": query,
                "search_time_seconds": search_time,
                "vector_store_status": vector_status,
                "results_count": len(results.results),
                "used_web_fallback": results.used_web_fallback,
                "average_similarity_score": sum(r.similarity_score for r in results.results) / len(results.results) if results.results else 0
            }
            
        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "search_time_seconds": 0,
                "results_count": 0
            }

