import axios from 'axios'
import { SearchRequest, SearchResponse } from '@/types'

import { config } from './config'

const API_BASE_URL = config.apiUrl

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const searchApi = {
  search: async (request: SearchRequest): Promise<SearchResponse> => {
    const response = await api.post('/api/search', request)
    return response.data
  },

  getSuggestions: async (): Promise<{ suggestions: string[] }> => {
    const response = await api.get('/api/search/suggestions')
    return response.data
  },

  healthCheck: async (): Promise<{ status: string; message: string }> => {
    const response = await api.get('/api/health')
    return response.data
  },
}

export default api
