#!/usr/bin/env python3
"""
Demo script to test the RAG Retrieval System
"""

import requests
import json
import time
from typing import List, Dict

API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['message']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_search(query: str, limit: int = 3):
    """Test the search endpoint"""
    print(f"🔍 Testing search: '{query}'")
    try:
        payload = {
            "query": query,
            "limit": limit,
            "threshold": 0.6,
            "use_web_fallback": True
        }
        
        response = requests.post(f"{API_BASE_URL}/api/search", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search successful!")
            print(f"   Query: {data['query']}")
            print(f"   Results found: {data['total_found']}")
            print(f"   Web fallback used: {data['used_web_fallback']}")
            
            for i, result in enumerate(data['results'][:2], 1):
                doc = result['document']
                print(f"   Result {i}:")
                print(f"     Title: {doc['metadata'].get('title', 'N/A')}")
                print(f"     Category: {doc['metadata'].get('category', 'N/A')}")
                print(f"     Similarity: {result['similarity_score']:.2f}")
                print(f"     Source: {result['source']}")
                print(f"     Content preview: {doc['content'][:100]}...")
                print()
            
            return True
        else:
            print(f"❌ Search failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Search error: {e}")
        return False

def test_suggestions():
    """Test the suggestions endpoint"""
    print("🔍 Testing search suggestions...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/search/suggestions")
        if response.status_code == 200:
            data = response.json()
            suggestions = data['suggestions']
            print(f"✅ Got {len(suggestions)} suggestions:")
            for suggestion in suggestions[:5]:
                print(f"   - {suggestion}")
            return True
        else:
            print(f"❌ Suggestions failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Suggestions error: {e}")
        return False

def test_ingestion_status():
    """Test the ingestion status endpoint"""
    print("🔍 Testing ingestion status...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/ingest/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Ingestion status:")
            print(f"   Collection: {data['collection_name']}")
            print(f"   Document count: {data['document_count']}")
            print(f"   Status: {data['status']}")
            return True
        else:
            print(f"❌ Ingestion status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ingestion status error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 RAG Retrieval System Demo")
    print("=" * 50)
    
    # Wait for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(2)
    
    # Test health check
    if not test_health_check():
        print("❌ Backend not available. Please start the backend first.")
        return
    
    print()
    
    # Test ingestion status
    test_ingestion_status()
    print()
    
    # Test suggestions
    test_suggestions()
    print()
    
    # Test various search queries
    test_queries = [
        "diabetes treatment guidelines",
        "hypertension management",
        "COVID-19 symptoms",
        "heart disease prevention",
        "mental health resources",
        "pediatric care protocols",
        "emergency medicine procedures",
        "drug interactions"
    ]
    
    print("🔍 Testing various search queries...")
    print("-" * 50)
    
    success_count = 0
    for query in test_queries:
        if test_search(query):
            success_count += 1
        print()
    
    print("📊 Demo Results Summary")
    print("=" * 50)
    print(f"✅ Successful searches: {success_count}/{len(test_queries)}")
    print(f"📈 Success rate: {success_count/len(test_queries)*100:.1f}%")
    
    if success_count == len(test_queries):
        print("🎉 All tests passed! The RAG system is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the backend logs for details.")
    
    print("\n🌐 Frontend available at: http://localhost:3000")
    print("📚 API documentation at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()

