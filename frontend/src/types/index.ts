export interface Document {
  id: string
  content: string
  metadata: {
    title?: string
    category?: string
    source?: string
    keywords?: string[]
    url?: string
    type?: string
  }
  source: string
  created_at: string
}

export interface SearchResult {
  document: Document
  similarity_score: number
  source: string
}

export interface SearchResponse {
  query: string
  results: SearchResult[]
  total_found: number
  used_web_fallback: boolean
  web_results?: WebResult[]
}

export interface WebResult {
  title: string
  content: string
  url: string
  source: string
}

export interface SearchRequest {
  query: string
  limit?: number
  threshold?: number
  use_web_fallback?: boolean
}

