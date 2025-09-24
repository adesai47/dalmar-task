import asyncio
import json
from typing import AsyncGenerator, List, Dict, Any, Optional
from openai import AsyncAzureOpenAI
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_MODEL_NAME,
    AZURE_OPENAI_DEPLOYMENT
)

load_dotenv()

class AzureOpenAIService:
    def __init__(self):
        # Azure OpenAI configuration
        self.api_key = AZURE_OPENAI_API_KEY
        self.api_version = AZURE_OPENAI_API_VERSION
        self.endpoint = AZURE_OPENAI_ENDPOINT
        self.model_name = AZURE_OPENAI_MODEL_NAME
        self.deployment = AZURE_OPENAI_DEPLOYMENT
        
        # Initialize Azure OpenAI client
        self.client = AsyncAzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint
        )
    
    async def generate_response(
        self, 
        query: str, 
        context_documents: List[Dict[str, Any]], 
        chat_history: Optional[List[Dict[str, str]]] = None,
        images: Optional[List[str]] = None
    ) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response using Azure OpenAI with RAG context and images
        """
        try:
            # Prepare system prompt with context
            system_prompt = self._build_system_prompt(context_documents)
            
            # Prepare messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add chat history if provided
            if chat_history:
                # Convert ChatMessage objects to the format expected by OpenAI
                for msg in chat_history[-10:]:  # Keep last 10 messages for context
                    if hasattr(msg, 'role') and hasattr(msg, 'content'):
                        messages.append({"role": msg.role, "content": msg.content})
                    elif isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                        messages.append({"role": msg['role'], "content": msg['content']})
            
            # Add current query with images if provided
            if images and len(images) > 0:
                # Build content array with text and images
                content = [{"type": "text", "text": query}]
                for image in images:
                    # Remove data:image/...;base64, prefix if present
                    clean_image = image.split(',')[-1] if ',' in image else image
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{clean_image}"
                        }
                    })
                messages.append({"role": "user", "content": content})
            else:
                messages.append({"role": "user", "content": query})
            
            # Generate streaming response
            stream = await self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                stream=True,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Yield tokens as they come
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"Error generating response: {str(e)}"
    
    def _build_system_prompt(self, context_documents: List[Dict[str, Any]]) -> str:
        """Build system prompt with retrieved context"""
        base_prompt = """You are a helpful healthcare AI assistant. You have access to relevant healthcare documents and information. 
        
Please provide accurate, helpful responses based on the context provided. If the context doesn't contain enough information to answer the question, say so clearly.

If the user provides images, analyze them and provide relevant healthcare information based on what you see in the images.

Guidelines:
- Be accurate and evidence-based
- Use clear, accessible language
- Include relevant details from the context
- If you're uncertain about medical advice, recommend consulting healthcare professionals
- Always prioritize patient safety
- When analyzing images, describe what you see and provide relevant healthcare insights

Context Documents:
"""
        
        if context_documents:
            for i, doc in enumerate(context_documents, 1):
                title = doc.get("metadata", {}).get("title", f"Document {i}")
                content = doc.get("content", "")
                source = doc.get("metadata", {}).get("source", "Unknown")
                
                base_prompt += f"\n--- Document {i}: {title} ---\n"
                base_prompt += f"Source: {source}\n"
                base_prompt += f"Content: {content}\n"
        else:
            base_prompt += "\nNo specific context documents available. Please answer based on your general knowledge.\n"
        
        return base_prompt
    
    async def generate_non_streaming_response(
        self, 
        query: str, 
        context_documents: List[Dict[str, Any]], 
        chat_history: Optional[List[Dict[str, str]]] = None,
        images: Optional[List[str]] = None
    ) -> str:
        """
        Generate a non-streaming response for testing purposes
        """
        try:
            # Prepare system prompt with context
            system_prompt = self._build_system_prompt(context_documents)
            
            # Prepare messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add chat history if provided
            if chat_history:
                # Convert ChatMessage objects to the format expected by OpenAI
                for msg in chat_history[-10:]:  # Keep last 10 messages for context
                    if hasattr(msg, 'role') and hasattr(msg, 'content'):
                        messages.append({"role": msg.role, "content": msg.content})
                    elif isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                        messages.append({"role": msg['role'], "content": msg['content']})
            
            # Add current query with images if provided
            if images and len(images) > 0:
                # Build content array with text and images
                content = [{"type": "text", "text": query}]
                for image in images:
                    # Remove data:image/...;base64, prefix if present
                    clean_image = image.split(',')[-1] if ',' in image else image
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{clean_image}"
                        }
                    })
                messages.append({"role": "user", "content": content})
            else:
                messages.append({"role": "user", "content": query})
            
            # Generate response
            response = await self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    async def extract_images_from_response(self, response_text: str) -> List[str]:
        """
        Extract image URLs or references from the response text
        This is a placeholder for future image processing capabilities
        """
        # Simple regex to find potential image URLs
        import re
        image_patterns = [
            r'https?://[^\s]+\.(?:jpg|jpeg|png|gif|webp|svg)',
            r'!\[.*?\]\((.*?)\)',  # Markdown images
        ]
        
        images = []
        for pattern in image_patterns:
            matches = re.findall(pattern, response_text, re.IGNORECASE)
            images.extend(matches)
        
        return list(set(images))  # Remove duplicates
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test the Azure OpenAI connection"""
        try:
            response = await self.client.chat.completions.create(
                model=self.deployment,
                messages=[{"role": "user", "content": "Hello, this is a test message."}],
                max_tokens=10
            )
            
            return {
                "status": "success",
                "model": self.deployment,
                "endpoint": self.endpoint,
                "test_response": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "status": "error",
                "model": self.deployment,
                "endpoint": self.endpoint,
                "error": str(e)
            }
