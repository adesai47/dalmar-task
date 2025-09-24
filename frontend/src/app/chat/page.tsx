'use client'

import { useState, useRef, useEffect } from 'react'
import { ChatMessage, ChatStreamEvent } from '@/types'
import { Send, Bot, User, Loader2, Image as ImageIcon } from 'lucide-react'

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [currentResponse, setCurrentResponse] = useState('')
  const [contextInfo, setContextInfo] = useState<any>(null)
  const [images, setImages] = useState<string[]>([])
  const [uploadedImages, setUploadedImages] = useState<string[]>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, currentResponse])

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (files) {
      Array.from(files).forEach(file => {
        if (file.type.startsWith('image/')) {
          const reader = new FileReader()
          reader.onload = (e) => {
            const result = e.target?.result as string
            setUploadedImages(prev => [...prev, result])
          }
          reader.readAsDataURL(file)
        }
      })
    }
  }

  const removeImage = (index: number) => {
    setUploadedImages(prev => prev.filter((_, i) => i !== index))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: ChatMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
      images: uploadedImages.length > 0 ? uploadedImages : undefined
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)
    setCurrentResponse('')
    setContextInfo(null)
    setImages([])
    setUploadedImages([]) // Clear uploaded images after sending

    try {
      const response = await fetch('http://localhost:8000/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: input,
          chat_history: messages.slice(-10), // Send last 10 messages for context
          use_web_fallback: true,
          stream: true,
          images: uploadedImages.length > 0 ? uploadedImages : undefined
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body?.getReader()
      if (!reader) {
        throw new Error('No response body reader available')
      }

      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              const event = data as ChatStreamEvent
              // console.log('Received SSE event:', event) // Debug log

              switch (event.type) {
                case 'metadata':
                  setContextInfo(event.data)
                  break
                case 'start':
                  // Start of response
                  break
                case 'content':
                  // Ensure event.data is a string before appending
                  const contentData = typeof event.data === 'string' ? event.data : String(event.data)
                  // console.log('Content data:', contentData) // Debug log
                  setCurrentResponse(prev => {
                    const newResponse = prev + contentData
                    // console.log('Updated response:', newResponse) // Debug log
                    return newResponse
                  })
                  break
                case 'complete':
                  // Complete the message - currentResponse already contains the full response
                  const assistantMessage: ChatMessage = {
                    role: 'assistant',
                    content: currentResponse, // Don't append event.data as it's an object
                    timestamp: new Date().toISOString()
                  }
                  setMessages(prev => [...prev, assistantMessage])
                  setCurrentResponse('')
                  setIsLoading(false) // Set loading to false here instead of in finally
                  
                  // Extract images from context documents
                  if (event.data.context_documents) {
                    const extractedImages: string[] = []
                    event.data.context_documents.forEach((doc: any) => {
                      if (doc.metadata?.images) {
                        extractedImages.push(...doc.metadata.images)
                      }
                    })
                    setImages(extractedImages)
                  }
                  break
                case 'error':
                  throw new Error(event.data.error)
              }
            } catch (parseError) {
              console.error('Error parsing SSE data:', parseError)
            }
          }
        }
      }
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
      setIsLoading(false) // Set loading to false on error
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto h-screen flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Healthcare AI Assistant</h1>
          <p className="text-gray-600">Ask questions about healthcare topics with RAG-powered responses</p>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-3xl px-4 py-3 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white border border-gray-200'
                }`}
              >
                <div className="flex items-start space-x-2">
                  {message.role === 'assistant' ? (
                    <Bot className="h-5 w-5 text-blue-600 mt-1 flex-shrink-0" />
                  ) : (
                    <User className="h-5 w-5 text-blue-200 mt-1 flex-shrink-0" />
                  )}
                  <div className="flex-1">
                    <p className="whitespace-pre-wrap">{message.content}</p>
                    
                    {/* Display images if present */}
                    {message.images && message.images.length > 0 && (
                      <div className="mt-3 space-y-2">
                        {message.images.map((image, imgIndex) => (
                          <div key={imgIndex} className="relative">
                            <img
                              src={image}
                              alt={`Uploaded image ${imgIndex + 1}`}
                              className="max-w-full h-auto rounded-lg border border-gray-200 max-h-64 object-contain"
                            />
                          </div>
                        ))}
                      </div>
                    )}
                    
                    <p className={`text-xs mt-2 ${
                      message.role === 'user' ? 'text-blue-200' : 'text-gray-500'
                    }`}>
                      {new Date(message.timestamp || '').toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}

          {/* Current streaming response */}
          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-3xl px-4 py-3 rounded-lg bg-white border border-gray-200">
                <div className="flex items-start space-x-2">
                  <Bot className="h-5 w-5 text-blue-600 mt-1 flex-shrink-0" />
                  <div className="flex-1">
                    <p className="whitespace-pre-wrap">{currentResponse || 'Generating response...'}</p>
                    <div className="flex items-center mt-2">
                      <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
                      <span className="text-xs text-gray-500 ml-2">Generating...</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Context Information */}
          {contextInfo && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-2">
                <Bot className="h-4 w-4 text-blue-600" />
                <span className="text-sm font-medium text-blue-900">Context Found</span>
              </div>
              <p className="text-sm text-blue-800">
                Found {contextInfo.context_documents_count} relevant documents
                {contextInfo.used_web_fallback && ' (including web search results)'}
              </p>
            </div>
          )}

          {/* Images */}
          {images.length > 0 && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-3">
                <ImageIcon className="h-4 w-4 text-green-600" />
                <span className="text-sm font-medium text-green-900">Related Images</span>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {images.map((imageUrl, index) => (
                  <div key={index} className="relative">
                    <img
                      src={imageUrl}
                      alt={`Context image ${index + 1}`}
                      className="w-full h-32 object-cover rounded-lg border border-green-200"
                      onError={(e) => {
                        (e.target as HTMLImageElement).style.display = 'none'
                      }}
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        <div className="bg-white border-t border-gray-200 px-6 py-4">
          {/* Image Preview */}
          {uploadedImages.length > 0 && (
            <div className="mb-4">
              <div className="flex flex-wrap gap-2">
                {uploadedImages.map((image, index) => (
                  <div key={index} className="relative">
                    <img
                      src={image}
                      alt={`Preview ${index + 1}`}
                      className="w-20 h-20 object-cover rounded-lg border border-gray-200"
                    />
                    <button
                      type="button"
                      onClick={() => removeImage(index)}
                      className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs hover:bg-red-600"
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="flex space-x-4">
            <div className="flex-1">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about healthcare topics..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isLoading}
              />
            </div>
            
            {/* Image Upload Button */}
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center space-x-2"
              disabled={isLoading}
            >
              <ImageIcon className="h-5 w-5 text-gray-600" />
              <span>Image</span>
            </button>
            
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              multiple
              onChange={handleImageUpload}
              className="hidden"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              {isLoading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5" />
              )}
              <span>Send</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
