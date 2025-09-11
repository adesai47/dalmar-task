'use client'

interface SearchSuggestionsProps {
  onSuggestionClick: (query: string) => void
}

const suggestions = [
  'diabetes treatment guidelines',
  'hypertension management',
  'COVID-19 symptoms',
  'heart disease prevention',
  'mental health resources',
  'pediatric care protocols',
  'emergency medicine procedures',
  'pharmaceutical interactions'
]

export function SearchSuggestions({ onSuggestionClick }: SearchSuggestionsProps) {
  return (
    <div className="mb-8">
      <h3 className="text-sm font-medium text-gray-700 mb-3">Popular searches:</h3>
      <div className="flex flex-wrap gap-2">
        {suggestions.map((suggestion, index) => (
          <button
            key={index}
            onClick={() => onSuggestionClick(suggestion)}
            className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors"
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  )
}

