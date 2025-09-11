'use client'

import { useState } from 'react'
import { SearchBar } from '@/components/SearchBar'
import { SearchResults } from '@/components/SearchResults'
import { Header } from '@/components/Header'
import { SearchSuggestions } from '@/components/SearchSuggestions'
import { useSearch } from '@/hooks/useSearch'

export default function Home() {
  const [query, setQuery] = useState('')
  const { searchResults, isLoading, error, search } = useSearch()

  const handleSearch = async (searchQuery: string) => {
    setQuery(searchQuery)
    await search(searchQuery)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Healthcare Document Retrieval
            </h1>
            <p className="text-lg text-gray-600">
              Search through healthcare documents using advanced RAG technology
            </p>
          </div>

          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
          
          <SearchSuggestions onSuggestionClick={handleSearch} />
          
          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600">Error: {error}</p>
            </div>
          )}
          
          <SearchResults 
            results={searchResults} 
            isLoading={isLoading}
            query={query}
          />
        </div>
      </main>
    </div>
  )
}