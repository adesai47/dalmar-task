import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from typing import List, Dict, Any
import json
import re

class WebSearchService:
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def initialize(self):
        """Initialize the web search service"""
        self.session = aiohttp.ClientSession(headers=self.headers)
    
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Perform web search using DuckDuckGo (no API key required)
        Falls back to scraping search results
        """
        try:
            # Use DuckDuckGo instant answer API for healthcare queries
            results = await self._search_duckduckgo(query, limit)
            
            if not results:
                # Fallback to general web search
                results = await self._search_general(query, limit)
            
            return results
            
        except Exception as e:
            print(f"Web search error: {e}")
            return []
    
    async def _search_duckduckgo(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Search using DuckDuckGo instant answer API"""
        try:
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    results = []
                    
                    # Extract abstract if available
                    if data.get('Abstract'):
                        results.append({
                            'title': data.get('Heading', query),
                            'content': data.get('Abstract'),
                            'url': data.get('AbstractURL', ''),
                            'source': 'DuckDuckGo Instant Answer'
                        })
                    
                    # Extract related topics
                    for topic in data.get('RelatedTopics', [])[:limit-1]:
                        if isinstance(topic, dict) and 'Text' in topic:
                            results.append({
                                'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' '),
                                'content': topic.get('Text'),
                                'url': topic.get('FirstURL', ''),
                                'source': 'DuckDuckGo Related Topics'
                            })
                    
                    return results[:limit]
            
            return []
            
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
            return []
    
    async def _search_general(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """General web search fallback"""
        try:
            # Use a simple web search approach
            search_query = f"{query} healthcare medical"
            url = f"https://www.google.com/search?q={search_query}&num={limit}"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    
                    # Extract search results (this is a simplified approach)
                    search_results = soup.find_all('div', class_='g')
                    
                    for result in search_results[:limit]:
                        try:
                            title_elem = result.find('h3')
                            link_elem = result.find('a')
                            snippet_elem = result.find('span', class_='aCOpRe')
                            
                            if title_elem and link_elem:
                                title = title_elem.get_text().strip()
                                url = link_elem.get('href', '')
                                snippet = snippet_elem.get_text().strip() if snippet_elem else ''
                                
                                # Filter for healthcare-related content
                                if any(keyword in title.lower() or keyword in snippet.lower() 
                                      for keyword in ['health', 'medical', 'medicine', 'healthcare', 'clinical']):
                                    results.append({
                                        'title': title,
                                        'content': snippet,
                                        'url': url,
                                        'source': 'Web Search'
                                    })
                        except:
                            continue
                    
                    return results
            
            return []
            
        except Exception as e:
            print(f"General web search error: {e}")
            return []
    
    async def _search_healthcare_sources(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Search specific healthcare sources"""
        healthcare_sources = [
            "https://www.cdc.gov",
            "https://www.nih.gov",
            "https://www.mayoclinic.org",
            "https://www.webmd.com",
            "https://www.healthline.com"
        ]
        
        results = []
        
        for source in healthcare_sources[:2]:  # Limit to avoid rate limiting
            try:
                search_url = f"{source}/search?q={query}"
                async with self.session.get(search_url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Extract relevant content (implementation depends on site structure)
                        # This is a simplified example
                        content_elements = soup.find_all(['p', 'div'], string=re.compile(query, re.I))
                        
                        for elem in content_elements[:2]:
                            content = elem.get_text().strip()
                            if len(content) > 50:  # Filter out very short content
                                results.append({
                                    'title': f"Content from {source}",
                                    'content': content[:500],  # Limit content length
                                    'url': source,
                                    'source': f'Healthcare Source: {source}'
                                })
                                
            except Exception as e:
                print(f"Error searching {source}: {e}")
                continue
        
        return results[:limit]
    
    async def close(self):
        """Close the web search service"""
        if self.session:
            await self.session.close()

