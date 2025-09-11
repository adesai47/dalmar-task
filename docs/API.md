# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
No authentication required for this demo system.

## Endpoints

### Health Check

#### GET /api/health
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "RAG Retrieval System is running"
}
```

### Search

#### POST /api/search
Search for relevant healthcare documents.

**Request Body:**
```json
{
  "query": "diabetes treatment guidelines",
  "limit": 5,
  "threshold": 0.7,
  "use_web_fallback": true
}
```

**Parameters:**
- `query` (string, required): Search query
- `limit` (integer, optional): Maximum number of results (default: 5)
- `threshold` (float, optional): Similarity threshold (default: 0.7)
- `use_web_fallback` (boolean, optional): Enable web search fallback (default: true)

**Response:**
```json
{
  "query": "diabetes treatment guidelines",
  "results": [
    {
      "document": {
        "id": "doc_123",
        "content": "Type 2 diabetes is a chronic condition...",
        "metadata": {
          "title": "Type 2 Diabetes Management",
          "category": "Endocrinology",
          "source": "American Diabetes Association Guidelines",
          "keywords": ["diabetes", "type 2", "insulin resistance"]
        },
        "source": "American Diabetes Association Guidelines",
        "created_at": "2024-01-15T10:30:00Z"
      },
      "similarity_score": 0.85,
      "source": "vector_store"
    }
  ],
  "total_found": 1,
  "used_web_fallback": false,
  "web_results": null
}
```

#### GET /api/search/suggestions
Get search suggestions for common healthcare queries.

**Response:**
```json
{
  "suggestions": [
    "diabetes treatment guidelines",
    "hypertension management",
    "COVID-19 symptoms",
    "heart disease prevention",
    "mental health resources",
    "pediatric care protocols",
    "emergency medicine procedures",
    "pharmaceutical interactions"
  ]
}
```

### Document Ingestion

#### POST /api/ingest
Ingest new documents into the vector store.

**Request Body:**
```json
{
  "documents": [
    {
      "content": "Document content here...",
      "metadata": {
        "title": "Document Title",
        "category": "Medical Specialty",
        "source": "Source Organization",
        "keywords": ["keyword1", "keyword2"]
      }
    }
  ],
  "collection_name": "healthcare_docs"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully ingested 1 documents",
  "documents_ingested": 1
}
```

#### GET /api/ingest/status
Get the current status of document ingestion.

**Response:**
```json
{
  "collection_name": "healthcare_docs",
  "document_count": 18,
  "status": "active"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Search failed: Error message here"
}
```

## Example Usage

### Using curl

```bash
# Health check
curl http://localhost:8000/api/health

# Search for diabetes information
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "diabetes treatment",
    "limit": 3,
    "threshold": 0.6
  }'

# Get search suggestions
curl http://localhost:8000/api/search/suggestions
```

### Using JavaScript/Fetch

```javascript
// Search for healthcare documents
const searchDocuments = async (query) => {
  const response = await fetch('http://localhost:8000/api/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: query,
      limit: 5,
      threshold: 0.7,
      use_web_fallback: true
    })
  });
  
  const data = await response.json();
  return data;
};

// Usage
searchDocuments('hypertension management')
  .then(results => console.log(results))
  .catch(error => console.error('Error:', error));
```

### Using Python requests

```python
import requests

# Search for healthcare documents
def search_documents(query):
    url = "http://localhost:8000/api/search"
    payload = {
        "query": query,
        "limit": 5,
        "threshold": 0.7,
        "use_web_fallback": True
    }
    
    response = requests.post(url, json=payload)
    return response.json()

# Usage
results = search_documents("COVID-19 symptoms")
print(results)
```

## Rate Limiting

Currently no rate limiting is implemented, but it's recommended for production use.

## CORS

The API is configured to accept requests from `http://localhost:3000` (Next.js frontend).

## Web Search Fallback

When `use_web_fallback` is enabled and vector search returns insufficient results, the system will:

1. Search DuckDuckGo Instant Answer API
2. Search healthcare-specific sources (CDC, NIH, Mayo Clinic)
3. Perform general web search as final fallback
4. Filter results for healthcare relevance
5. Combine with vector search results

The web search results are included in the `web_results` field of the response.

