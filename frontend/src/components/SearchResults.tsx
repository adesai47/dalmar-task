'use client'

import { SearchResponse, SearchResult } from '@/types'
import { ExternalLink, Database, Globe, Clock, Tag } from 'lucide-react'

interface SearchResultsProps {
  results: SearchResponse | null
  isLoading: boolean
  query: string
}

export function SearchResults({ results, isLoading, query }: SearchResultsProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Searching healthcare documents...</p>
        </div>
      </div>
    )
  }

  if (!results && !isLoading) {
    return (
      <div className="text-center py-12">
        <Database className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">Enter a search query to find healthcare documents</p>
      </div>
    )
  }

  if (!results) return null

  return (
    <div className="space-y-6">
      {/* Search Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-blue-900">
              Search Results for "{query}"
            </h2>
            <p className="text-blue-700">
              Found {results.total_found} document{results.total_found !== 1 ? 's' : ''}
              {results.used_web_fallback && ' (including web results)'}
            </p>
          </div>
          {results.used_web_fallback && (
            <div className="flex items-center text-blue-600">
              <Globe className="h-4 w-4 mr-1" />
              <span className="text-sm">Web Fallback Used</span>
            </div>
          )}
        </div>
      </div>

      {/* Results */}
      <div className="space-y-4">
        {results.results.map((result, index) => (
          <SearchResultCard key={result.document.id} result={result} index={index} />
        ))}
      </div>

      {/* Web Results Section */}
      {results.web_results && results.web_results.length > 0 && (
        <div className="mt-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Globe className="h-5 w-5 mr-2 text-green-600" />
            Additional Web Results
          </h3>
          <div className="space-y-3">
            {results.web_results.map((webResult, index) => (
              <div key={index} className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="font-medium text-green-900 mb-2">{webResult.title}</h4>
                    <p className="text-green-800 text-sm mb-2">{webResult.content}</p>
                    <div className="flex items-center text-xs text-green-600">
                      <span className="mr-2">{webResult.source}</span>
                      {webResult.url && (
                        <a
                          href={webResult.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center hover:text-green-800"
                        >
                          <ExternalLink className="h-3 w-3 mr-1" />
                          View Source
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function SearchResultCard({ result, index }: { result: SearchResult; index: number }) {
  const { document, similarity_score, source } = result

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center">
          <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded-full mr-3">
            #{index + 1}
          </span>
          <div className="flex items-center text-sm text-gray-500">
            {source === 'web_search' ? (
              <Globe className="h-4 w-4 mr-1 text-green-600" />
            ) : (
              <Database className="h-4 w-4 mr-1 text-blue-600" />
            )}
            <span>{source === 'web_search' ? 'Web Search' : 'Vector Store'}</span>
          </div>
        </div>
        <div className="flex items-center text-sm text-gray-500">
          <span className="bg-gray-100 px-2 py-1 rounded">
            {Math.round(similarity_score * 100)}% match
          </span>
        </div>
      </div>

      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        {document.metadata.title || 'Healthcare Document'}
      </h3>

      <p className="text-gray-700 mb-4 leading-relaxed">
        {document.content.length > 300 
          ? `${document.content.substring(0, 300)}...` 
          : document.content
        }
      </p>

      <div className="flex items-center justify-between text-sm text-gray-500">
        <div className="flex items-center space-x-4">
          {document.metadata.category && (
            <div className="flex items-center">
              <Tag className="h-4 w-4 mr-1" />
              <span>{document.metadata.category}</span>
            </div>
          )}
          <div className="flex items-center">
            <Clock className="h-4 w-4 mr-1" />
            <span>{new Date(document.created_at).toLocaleDateString()}</span>
          </div>
        </div>
        
        <div className="text-xs text-gray-400">
          Source: {document.source}
        </div>
      </div>

      {document.metadata.keywords && document.metadata.keywords.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          <div className="flex flex-wrap gap-1">
            {document.metadata.keywords.slice(0, 5).map((keyword, idx) => (
              <span
                key={idx}
                className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded"
              >
                {keyword}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

