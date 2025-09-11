import { Search, Heart, Database } from 'lucide-react'

export function Header() {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <Heart className="h-8 w-8 text-blue-600" />
              <Database className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">RAG Retrieval</h1>
              <p className="text-sm text-gray-500">Healthcare Document Search</p>
            </div>
          </div>
          
        </div>
      </div>
    </header>
  )
}

