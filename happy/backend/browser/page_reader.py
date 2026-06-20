"""Page Reader - Extracts content from web pages"""

import logging
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class PageReader:
    """Reads and parses web page content"""

    def __init__(self):
        self.current_url: Optional[str] = None
        self.current_html: Optional[str] = None
        self.soup: Optional[BeautifulSoup] = None

    def read(self, html: str, url: str = "") -> Dict[str, Any]:
        """
        Read and parse page content
        
        Args:
            html: Page HTML content
            url: Current URL (for resolving relative links)
            
        Returns:
            {
                "success": bool,
                "title": str,
                "url": str,
                "text": str,
                "links": [{"text": str, "href": str}],
                "buttons": [{"text": str, "type": str}],
                "images": [{"alt": str, "src": str}],
                "inputs": [{"type": str, "name": str}],
                "message": str
            }
        """
        try:
            self.current_html = html
            self.current_url = url
            self.soup = BeautifulSoup(html, 'html.parser')
            
            return {
                "success": True,
                "title": self.extract_title(),
                "url": url,
                "text": self.extract_text(),
                "links": self.extract_links(),
                "buttons": self.extract_buttons(),
                "images": self.extract_images(),
                "inputs": self.extract_inputs(),
                "message": "Page parsed successfully"
            }
            
        except Exception as e:
            logger.error(f"Error reading page: {e}")
            return {
                "success": False,
                "message": f"Error reading page: {str(e)}"
            }

    def extract_title(self) -> str:
        """Extract page title"""
        if not self.soup:
            return ""
        
        title_tag = self.soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        h1 = self.soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        return ""

    def extract_text(self) -> str:
        """Extract main text content from page"""
        if not self.soup:
            return ""
        
        try:
            # Remove script and style elements
            for script in self.soup(['script', 'style', 'meta', 'link']):
                script.decompose()
            
            # Find main content area (common patterns)
            main_content = None
            for selector in [
                self.soup.find('main'),
                self.soup.find('article'),
                self.soup.find(class_='content'),
                self.soup.find(class_='post'),
                self.soup.find(class_='article'),
            ]:
                if selector:
                    main_content = selector
                    break
            
            if not main_content:
                main_content = self.soup.find('body') or self.soup
            
            # Extract paragraphs and headings
            text_parts = []
            for elem in main_content.find_all(['p', 'h1', 'h2', 'h3', 'li']):
                text = elem.get_text(strip=True)
                if text and len(text) > 3:
                    text_parts.append(text)
            
            text = "\n\n".join(text_parts)
            
            # Limit to reasonable length
            return text[:5000]
            
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return ""

    def extract_links(self) -> List[Dict[str, str]]:
        """Extract all links from page"""
        if not self.soup:
            return []
        
        links = []
        try:
            for link in self.soup.find_all('a', href=True):
                href = link.get('href', '').strip()
                text = link.get_text(strip=True)
                
                if not href or not text:
                    continue
                
                # Resolve relative URLs
                if not href.startswith(('http://', 'https://', 'mailto:', '#')):
                    if self.current_url:
                        href = urljoin(self.current_url, href)
                    else:
                        continue
                
                links.append({
                    "text": text[:100],
                    "href": href[:500]
                })
                
                if len(links) >= 50:  # Limit number of links
                    break
            
            return links
            
        except Exception as e:
            logger.error(f"Error extracting links: {e}")
            return []

    def extract_buttons(self) -> List[Dict[str, str]]:
        """Extract all buttons from page"""
        if not self.soup:
            return []
        
        buttons = []
        try:
            for button in self.soup.find_all(['button', 'input']):
                btn_type = button.get('type', 'button').lower()
                
                if button.name == 'button':
                    text = button.get_text(strip=True)
                else:
                    text = button.get('value', '')
                
                if text:
                    buttons.append({
                        "text": text[:50],
                        "type": btn_type
                    })
                
                if len(buttons) >= 30:
                    break
            
            return buttons
            
        except Exception as e:
            logger.error(f"Error extracting buttons: {e}")
            return []

    def extract_images(self) -> List[Dict[str, str]]:
        """Extract all images from page"""
        if not self.soup:
            return []
        
        images = []
        try:
            for img in self.soup.find_all('img'):
                src = img.get('src', '').strip()
                alt = img.get('alt', '').strip()
                
                if src:
                    # Resolve relative URLs
                    if not src.startswith(('http://', 'data:')):
                        if self.current_url:
                            src = urljoin(self.current_url, src)
                    
                    images.append({
                        "alt": alt[:100] if alt else "Image",
                        "src": src[:500]
                    })
                
                if len(images) >= 20:
                    break
            
            return images
            
        except Exception as e:
            logger.error(f"Error extracting images: {e}")
            return []

    def extract_inputs(self) -> List[Dict[str, str]]:
        """Extract all input fields from page"""
        if not self.soup:
            return []
        
        inputs = []
        try:
            for inp in self.soup.find_all('input'):
                inp_type = inp.get('type', 'text').lower()
                name = inp.get('name', '').strip()
                placeholder = inp.get('placeholder', '').strip()
                
                inputs.append({
                    "type": inp_type,
                    "name": name[:50],
                    "placeholder": placeholder[:50]
                })
                
                if len(inputs) >= 20:
                    break
            
            return inputs
            
        except Exception as e:
            logger.error(f"Error extracting inputs: {e}")
            return []

    def get_text_by_selector(self, selector: str) -> str:
        """Get text content by CSS selector"""
        if not self.soup:
            return ""
        
        try:
            element = self.soup.select_one(selector)
            if element:
                return element.get_text(strip=True)[:1000]
            return ""
        except Exception as e:
            logger.error(f"Error selecting element: {e}")
            return ""

    def has_login_form(self) -> bool:
        """Check if page has a login form"""
        if not self.soup:
            return False
        
        try:
            # Look for password inputs or login keywords
            password_input = self.soup.find('input', {'type': 'password'})
            login_form = self.soup.find('form')
            
            if password_input:
                return True
            
            if login_form:
                login_form_text = login_form.get_text(strip=True).lower()
                if any(keyword in login_form_text for keyword in ['login', 'password', 'username', 'sign in']):
                    return True
            
            return False
            
        except:
            return False

    def has_payment_form(self) -> bool:
        """Check if page has a payment form"""
        if not self.soup:
            return False
        
        try:
            page_text = self.soup.get_text(strip=True).lower()
            payment_keywords = ['credit card', 'cvv', 'expiration', 'stripe', 'paypal', 'billing', 'checkout']
            
            return any(keyword in page_text for keyword in payment_keywords)
            
        except:
            return False
