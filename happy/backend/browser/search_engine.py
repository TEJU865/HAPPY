"""Search Engine - Web search functionality for HAPPY"""

import requests
import logging
from typing import List, Dict, Any
from urllib.parse import quote
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class SearchEngine:
    """Handles web searches using DuckDuckGo"""

    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.headers = {"User-Agent": self.user_agent}

    def search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search the web using DuckDuckGo
        
        Args:
            query: Search query
            limit: Number of results to return
            
        Returns:
            {
                "success": bool,
                "results": [{"title": str, "url": str, "snippet": str, "position": int}],
                "query": str,
                "message": str
            }
        """
        try:
            # DuckDuckGo HTML search endpoint
            search_url = f"https://duckduckgo.com/html/?q={quote(query)}"
            
            response = requests.get(
                search_url,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()

            # Parse HTML results
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Find search results - DuckDuckGo HTML format
            result_items = soup.find_all('div', class_='result')
            
            for idx, item in enumerate(result_items[:limit]):
                try:
                    # Extract title and URL
                    link = item.find('a', class_='result__url')
                    title_elem = item.find('a', class_='result__link')
                    snippet_elem = item.find('a', class_='result__snippet')
                    
                    if not title_elem or not link:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    url = link.get('href', '').strip()
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    # Skip invalid results
                    if not url or not title:
                        continue
                    
                    results.append({
                        "position": idx + 1,
                        "title": title,
                        "url": url,
                        "snippet": snippet[:200]  # Limit snippet length
                    })
                    
                except Exception as e:
                    logger.debug(f"Error parsing result item: {e}")
                    continue

            if not results:
                # Fallback: try generic search parsing
                results = self._fallback_search(query, limit)

            return {
                "success": True,
                "query": query,
                "results": results,
                "message": f"Found {len(results)} results"
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Search request failed: {e}")
            return {
                "success": False,
                "query": query,
                "results": [],
                "message": f"Search failed: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {
                "success": False,
                "query": query,
                "results": [],
                "message": f"Error during search: {str(e)}"
            }

    def _fallback_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Fallback search using Google if DuckDuckGo fails"""
        try:
            search_url = f"https://www.google.com/search?q={quote(query)}"
            
            response = requests.get(
                search_url,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Parse Google search results
            for idx, result in enumerate(soup.find_all('div', class_='g')[:limit]):
                try:
                    link = result.find('a')
                    title = result.find('h3')
                    snippet = result.find('div', class_='VwiC3b')
                    
                    if not link or not title:
                        continue
                    
                    url = link.get('href', '').strip()
                    if url.startswith('/'):
                        continue
                    
                    results.append({
                        "position": idx + 1,
                        "title": title.get_text(strip=True),
                        "url": url,
                        "snippet": snippet.get_text(strip=True)[:200] if snippet else ""
                    })
                except:
                    continue
            
            return results

        except Exception as e:
            logger.debug(f"Fallback search failed: {e}")
            return []

    def parse_results(self, html: str) -> List[Dict[str, Any]]:
        """Parse HTML content and extract search results"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            for idx, item in enumerate(soup.find_all('a')):
                url = item.get('href', '').strip()
                text = item.get_text(strip=True)
                
                if url and text and url.startswith('http'):
                    results.append({
                        "position": idx + 1,
                        "title": text[:100],
                        "url": url,
                        "snippet": text[:200]
                    })
            
            return results
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return []
