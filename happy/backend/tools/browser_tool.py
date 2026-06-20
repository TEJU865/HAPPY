"""
Browser Automation Tool for HAPPY
Uses Playwright to control web browsers for automation tasks.
"""

import asyncio
from playwright.async_api import async_playwright
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BrowserTool:
    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None

    async def __aenter__(self):
        """Async context manager entry"""
        await self.start_browser()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close_browser()

    async def start_browser(self, headless: bool = False):
        """Start the browser instance"""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=headless)
            self.page = await self.browser.new_page()
            logger.info("Browser started successfully")
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise

    async def close_browser(self):
        """Close the browser instance"""
        try:
            if self.page:
                await self.page.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")

    async def open_website(self, url: str) -> Dict[str, Any]:
        """Open a website in the browser"""
        try:
            if not self.page:
                return {"success": False, "message": "Browser not started"}

            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = f"https://{url}"

            await self.page.goto(url)
            title = await self.page.title()
            return {
                "success": True,
                "message": f"Opened {url}",
                "title": title,
                "url": url
            }
        except Exception as e:
            logger.error(f"Failed to open website {url}: {e}")
            return {"success": False, "message": f"Failed to open {url}: {str(e)}"}

    async def search_web(self, query: str, engine: str = "google") -> Dict[str, Any]:
        """Perform a web search"""
        try:
            if not self.page:
                return {"success": False, "message": "Browser not started"}

            search_urls = {
                "google": f"https://www.google.com/search?q={query.replace(' ', '+')}",
                "bing": f"https://www.bing.com/search?q={query.replace(' ', '+')}",
                "duckduckgo": f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
            }

            url = search_urls.get(engine.lower(), search_urls["google"])
            await self.page.goto(url)

            # Wait for search results to load
            await self.page.wait_for_load_state('networkidle')

            title = await self.page.title()
            return {
                "success": True,
                "message": f"Searched for '{query}' on {engine}",
                "url": url,
                "title": title
            }
        except Exception as e:
            logger.error(f"Failed to search for {query}: {e}")
            return {"success": False, "message": f"Failed to search: {str(e)}"}

    async def click_element(self, selector: str, description: str = "") -> Dict[str, Any]:
        """Click on an element by selector"""
        try:
            if not self.page:
                return {"success": False, "message": "Browser not started"}

            await self.page.click(selector)
            return {
                "success": True,
                "message": f"Clicked on {description or selector}"
            }
        except Exception as e:
            logger.error(f"Failed to click element {selector}: {e}")
            return {"success": False, "message": f"Failed to click: {str(e)}"}

    async def type_text(self, selector: str, text: str) -> Dict[str, Any]:
        """Type text into an element"""
        try:
            if not self.page:
                return {"success": False, "message": "Browser not started"}

            await self.page.fill(selector, text)
            return {
                "success": True,
                "message": f"Typed '{text}' into element"
            }
        except Exception as e:
            logger.error(f"Failed to type text: {e}")
            return {"success": False, "message": f"Failed to type: {str(e)}"}

    async def get_page_content(self) -> Dict[str, Any]:
        """Get the current page content"""
        try:
            if not self.page:
                return {"success": False, "message": "Browser not started"}

            content = await self.page.content()
            title = await self.page.title()
            url = self.page.url

            return {
                "success": True,
                "content": content[:1000] + "..." if len(content) > 1000 else content,
                "title": title,
                "url": url
            }
        except Exception as e:
            logger.error(f"Failed to get page content: {e}")
            return {"success": False, "message": f"Failed to get content: {str(e)}"}

    async def take_screenshot(self, filename: str = "screenshot.png") -> Dict[str, Any]:
        """Take a screenshot of the current page"""
        try:
            if not self.page:
                return {"success": False, "message": "Browser not started"}

            await self.page.screenshot(path=filename)
            return {
                "success": True,
                "message": f"Screenshot saved as {filename}",
                "filename": filename
            }
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return {"success": False, "message": f"Failed to screenshot: {str(e)}"}

# Synchronous wrapper functions for easier integration
def open_website_sync(url: str) -> Dict[str, Any]:
    """Synchronous wrapper for opening websites"""
    async def _open():
        async with BrowserTool() as tool:
            return await tool.open_website(url)
    return asyncio.run(_open())

def search_web_sync(query: str, engine: str = "google") -> Dict[str, Any]:
    """Synchronous wrapper for web search"""
    async def _search():
        async with BrowserTool() as tool:
            return await tool.search_web(query, engine)
    return asyncio.run(_search())

def click_element_sync(selector: str, description: str = "") -> Dict[str, Any]:
    """Synchronous wrapper for clicking elements"""
    async def _click():
        async with BrowserTool() as tool:
            return await tool.click_element(selector, description)
    return asyncio.run(_click())

def type_text_sync(selector: str, text: str) -> Dict[str, Any]:
    """Synchronous wrapper for typing text"""
    async def _type():
        async with BrowserTool() as tool:
            return await tool.type_text(selector, text)
    return asyncio.run(_type())

def get_page_content_sync() -> Dict[str, Any]:
    """Synchronous wrapper for getting page content"""
    async def _get():
        async with BrowserTool() as tool:
            return await tool.get_page_content()
    return asyncio.run(_get())

def take_screenshot_sync(filename: str = "screenshot.png") -> Dict[str, Any]:
    """Synchronous wrapper for taking screenshots"""
    async def _screenshot():
        async with BrowserTool() as tool:
            return await tool.take_screenshot(filename)
    return asyncio.run(_screenshot())