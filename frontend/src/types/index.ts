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

// Chat-related types
export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
  images?: string[] // Base64 or URL images
}

export interface ChatRequest {
  query: string
  chat_history?: ChatMessage[]
  use_web_fallback?: boolean
  stream?: boolean
  images?: string[] // Base64 encoded images
}

export interface ChatResponse {
  query: string
  response: string
  context_documents: any[]
  used_web_fallback: boolean
  images: string[]
  total_context_found: number
  timestamp: string
}

export interface ChatStreamEvent {
  type: 'metadata' | 'start' | 'content' | 'complete' | 'error'
  data: any
}

