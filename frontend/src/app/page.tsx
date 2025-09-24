'use client'

import { useState } from 'react'
import Link from 'next/link'
import { SearchBar } from '@/components/SearchBar'
import { SearchResults } from '@/components/SearchResults'
import { Header } from '@/components/Header'
import { SearchSuggestions } from '@/components/SearchSuggestions'
import { useSearch } from '@/hooks/useSearch'
import { MessageCircle, Search } from 'lucide-react'

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
            <p className="text-lg text-gray-600 mb-6">
              Search through healthcare documents using advanced RAG technology
            </p>
            
            {/* Navigation Cards */}
            <div className="grid md:grid-cols-2 gap-6 max-w-2xl mx-auto">
              <Link 
                href="/" 
                className="p-6 bg-white rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all"
              >
                <Search className="h-8 w-8 text-blue-600 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Document Search</h3>
                <p className="text-gray-600">Search and retrieve relevant healthcare documents</p>
              </Link>
              
              <Link 
                href="/chat" 
                className="p-6 bg-white rounded-lg border border-gray-200 hover:border-green-300 hover:shadow-md transition-all"
              >
                <MessageCircle className="h-8 w-8 text-green-600 mx-auto mb-3" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Chat Assistant</h3>
                <p className="text-gray-600">Chat with AI powered by RAG and Azure OpenAI</p>
              </Link>
            </div>
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