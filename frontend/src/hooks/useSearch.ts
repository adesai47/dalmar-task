import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { searchApi } from '@/lib/api'
import { SearchResponse, SearchRequest } from '@/types'

export const useSearch = () => {
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null)

  const searchMutation = useMutation({
    mutationFn: async (query: string) => {
      const request: SearchRequest = {
        query,
        limit: 10,
        threshold: 0.05,
        use_web_fallback: true,
      }
      return await searchApi.search(request)
    },
    onSuccess: (data) => {
      setSearchResults(data)
    },
    onError: (error) => {
      console.error('Search error:', error)
    },
  })

  const search = async (query: string) => {
    if (!query.trim()) return
    await searchMutation.mutateAsync(query)
  }

  return {
    searchResults,
    isLoading: searchMutation.isPending,
    error: searchMutation.error?.message,
    search,
  }
}

