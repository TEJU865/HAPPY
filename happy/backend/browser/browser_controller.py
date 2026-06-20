"""Browser Controller - Manages Chromium instance with Playwright"""

import os
from typing import Optional, List, Dict, Any
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
import asyncio
import logging

logger = logging.getLogger(__name__)


class BrowserController:
    """Manages a persistent Chromium browser for HAPPY"""

    def __init__(self, profile_dir: str = "browser_profile"):
        self.profile_dir = profile_dir
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.current_page: Optional[Page] = None
        self.pages: Dict[int, Page] = {}
        self.page_counter = 0
        self.playwright = None
        self._create_profile_dir()

    def _create_profile_dir(self):
        """Create browser profile directory if it doesn't exist"""
        os.makedirs(self.profile_dir, exist_ok=True)

    async def start(self) -> bool:
        """Start the browser instance"""
        try:
            self.playwright = await async_playwright().start()
            
            # Launch browser with persistent context (profile)
            self.browser = await self.playwright.chromium.launch(
                headless=False,  # Show browser window
                args=[
                    "--disable-blink-features=AutomationControlled",
                ]
            )
            
            # Create context with persistent storage
            self.context = await self.browser.new_context(
                viewport={"width": 1280, "height": 720},
                ignore_https_errors=True,
            )
            
            # Create initial page
            self.current_page = await self.context.new_page()
            self.pages[0] = self.current_page
            
            logger.info("Browser started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            return False

    async def stop(self) -> bool:
        """Stop the browser instance"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("Browser stopped successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to stop browser: {e}")
            return False

    async def open_url(self, url: str) -> Dict[str, Any]:
        """Open a URL in the current page"""
        try:
            if not self.current_page:
                return {"success": False, "message": "Browser not started"}

            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = f"https://{url}"

            await self.current_page.goto(url, wait_until="networkidle", timeout=30000)
            title = await self.current_page.title()
            
            return {
                "success": True,
                "message": f"Opened {url}",
                "title": title,
                "url": url
            }
        except Exception as e:
            logger.error(f"Failed to open URL {url}: {e}")
            return {
                "success": False,
                "message": f"Failed to open URL: {str(e)}"
            }

    async def new_tab(self) -> Dict[str, Any]:
        """Create a new tab"""
        try:
            if not self.context:
                return {"success": False, "message": "Browser not started"}

            self.page_counter += 1
            new_page = await self.context.new_page()
            self.pages[self.page_counter] = new_page
            self.current_page = new_page

            return {
                "success": True,
                "message": f"New tab created (Tab {self.page_counter})",
                "tab_id": self.page_counter
            }
        except Exception as e:
            logger.error(f"Failed to create new tab: {e}")
            return {
                "success": False,
                "message": f"Failed to create tab: {str(e)}"
            }

    async def switch_tab(self, tab_id: int) -> Dict[str, Any]:
        """Switch to a specific tab"""
        try:
            if tab_id not in self.pages:
                return {
                    "success": False,
                    "message": f"Tab {tab_id} not found"
                }

            self.current_page = self.pages[tab_id]
            url = self.current_page.url
            title = await self.current_page.title()

            return {
                "success": True,
                "message": f"Switched to Tab {tab_id}",
                "url": url,
                "title": title
            }
        except Exception as e:
            logger.error(f"Failed to switch tab: {e}")
            return {
                "success": False,
                "message": f"Failed to switch tab: {str(e)}"
            }

    async def close_tab(self, tab_id: int) -> Dict[str, Any]:
        """Close a specific tab"""
        try:
            if tab_id not in self.pages:
                return {
                    "success": False,
                    "message": f"Tab {tab_id} not found"
                }

            if tab_id == 0 and len(self.pages) == 1:
                return {
                    "success": False,
                    "message": "Cannot close the only tab"
                }

            page = self.pages[tab_id]
            await page.close()
            del self.pages[tab_id]

            # Switch to first available tab
            if self.current_page == page:
                available_tabs = list(self.pages.keys())
                if available_tabs:
                    self.current_page = self.pages[available_tabs[0]]

            return {
                "success": True,
                "message": f"Closed Tab {tab_id}"
            }
        except Exception as e:
            logger.error(f"Failed to close tab: {e}")
            return {
                "success": False,
                "message": f"Failed to close tab: {str(e)}"
            }

    async def get_tabs(self) -> List[Dict[str, Any]]:
        """Get all open tabs"""
        tabs = []
        for tab_id, page in self.pages.items():
            try:
                title = await page.title()
                url = page.url
                tabs.append({
                    "id": tab_id,
                    "title": title,
                    "url": url,
                    "is_current": page == self.current_page
                })
            except:
                pass
        return tabs

    async def get_page_url(self) -> str:
        """Get current page URL"""
        return self.current_page.url if self.current_page else ""

    async def get_page_title(self) -> str:
        """Get current page title"""
        if self.current_page:
            return await self.current_page.title()
        return ""


# Global browser instance
_browser_instance: Optional[BrowserController] = None


async def get_browser() -> BrowserController:
    """Get or create global browser instance"""
    global _browser_instance
    if _browser_instance is None:
        _browser_instance = BrowserController()
    return _browser_instance


async def start_browser() -> bool:
    """Start global browser"""
    browser = await get_browser()
    return await browser.start()


async def stop_browser() -> bool:
    """Stop global browser"""
    global _browser_instance
    if _browser_instance:
        return await _browser_instance.stop()
    return True
