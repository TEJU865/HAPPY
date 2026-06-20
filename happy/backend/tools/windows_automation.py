"""
Windows Automation Tool for HAPPY
Uses pyautogui for mouse clicks, keyboard typing, and screenshots
"""

import pyautogui
import time
from typing import Dict, Any, Tuple, Optional
import logging
import os

logger = logging.getLogger(__name__)

class WindowsAutomation:
    """Windows automation using pyautogui"""

    def __init__(self):
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5  # Small pause between actions

    def click_at_position(self, x: int, y: int, button: str = "left", clicks: int = 1) -> Dict[str, Any]:
        """Click at specific screen coordinates"""
        try:
            pyautogui.click(x=x, y=y, button=button, clicks=clicks)
            return {
                "success": True,
                "message": f"Clicked {button} button {clicks} time(s) at ({x}, {y})"
            }
        except Exception as e:
            logger.error(f"Failed to click at ({x}, {y}): {e}")
            return {
                "success": False,
                "message": f"Failed to click at ({x}, {y})",
                "error": str(e)
            }

    def click_on_image(self, image_path: str, confidence: float = 0.8) -> Dict[str, Any]:
        """Click on an image found on screen"""
        try:
            if not os.path.exists(image_path):
                return {
                    "success": False,
                    "message": f"Image file '{image_path}' not found"
                }

            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location is None:
                return {
                    "success": False,
                    "message": f"Image '{image_path}' not found on screen"
                }

            center = pyautogui.center(location)
            pyautogui.click(center)

            return {
                "success": True,
                "message": f"Clicked on image at {center}",
                "position": center
            }
        except Exception as e:
            logger.error(f"Failed to click on image {image_path}: {e}")
            return {
                "success": False,
                "message": f"Failed to click on image",
                "error": str(e)
            }

    def type_text(self, text: str, interval: float = 0.02) -> Dict[str, Any]:
        """Type text at current cursor position"""
        try:
            pyautogui.typewrite(text, interval=interval)
            return {
                "success": True,
                "message": f"Typed '{text}' ({len(text)} characters)"
            }
        except Exception as e:
            logger.error(f"Failed to type text: {e}")
            return {
                "success": False,
                "message": "Failed to type text",
                "error": str(e)
            }

    def press_key(self, key: str) -> Dict[str, Any]:
        """Press a single key"""
        try:
            pyautogui.press(key)
            return {
                "success": True,
                "message": f"Pressed key '{key}'"
            }
        except Exception as e:
            logger.error(f"Failed to press key {key}: {e}")
            return {
                "success": False,
                "message": f"Failed to press key '{key}'",
                "error": str(e)
            }

    def press_keys(self, keys: list) -> Dict[str, Any]:
        """Press multiple keys simultaneously (hotkey)"""
        try:
            pyautogui.hotkey(*keys)
            return {
                "success": True,
                "message": f"Pressed hotkey combination: {' + '.join(keys)}"
            }
        except Exception as e:
            logger.error(f"Failed to press hotkey {keys}: {e}")
            return {
                "success": False,
                "message": f"Failed to press hotkey combination",
                "error": str(e)
            }

    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> Dict[str, Any]:
        """Move mouse to coordinates"""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return {
                "success": True,
                "message": f"Moved mouse to ({x}, {y})"
            }
        except Exception as e:
            logger.error(f"Failed to move mouse to ({x}, {y}): {e}")
            return {
                "success": False,
                "message": f"Failed to move mouse to ({x}, {y})",
                "error": str(e)
            }

    def drag_mouse(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 1.0) -> Dict[str, Any]:
        """Drag mouse from start to end position"""
        try:
            pyautogui.moveTo(start_x, start_y)
            pyautogui.dragTo(end_x, end_y, duration=duration)
            return {
                "success": True,
                "message": f"Dragged mouse from ({start_x}, {start_y}) to ({end_x}, {end_y})"
            }
        except Exception as e:
            logger.error(f"Failed to drag mouse: {e}")
            return {
                "success": False,
                "message": "Failed to drag mouse",
                "error": str(e)
            }

    def take_screenshot(self, filename: str = "screenshot.png", region: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, Any]:
        """Take a screenshot of the screen or region"""
        try:
            if region:
                screenshot = pyautogui.screenshot(filename, region=region)
                message = f"Screenshot saved as '{filename}' (region: {region})"
            else:
                screenshot = pyautogui.screenshot(filename)
                message = f"Screenshot saved as '{filename}' (full screen)"

            return {
                "success": True,
                "message": message,
                "filename": filename,
                "size": screenshot.size if screenshot else None
            }
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return {
                "success": False,
                "message": "Failed to take screenshot",
                "error": str(e)
            }

    def get_mouse_position(self) -> Dict[str, Any]:
        """Get current mouse position"""
        try:
            x, y = pyautogui.position()
            return {
                "success": True,
                "message": f"Mouse is at ({x}, {y})",
                "position": {"x": x, "y": y}
            }
        except Exception as e:
            logger.error(f"Failed to get mouse position: {e}")
            return {
                "success": False,
                "message": "Failed to get mouse position",
                "error": str(e)
            }

    def get_screen_size(self) -> Dict[str, Any]:
        """Get screen resolution"""
        try:
            width, height = pyautogui.size()
            return {
                "success": True,
                "message": f"Screen size: {width}x{height}",
                "size": {"width": width, "height": height}
            }
        except Exception as e:
            logger.error(f"Failed to get screen size: {e}")
            return {
                "success": False,
                "message": "Failed to get screen size",
                "error": str(e)
            }

    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> Dict[str, Any]:
        """Scroll mouse wheel"""
        try:
            pyautogui.scroll(clicks, x=x, y=y)
            direction = "up" if clicks > 0 else "down"
            return {
                "success": True,
                "message": f"Scrolled {direction} {abs(clicks)} clicks"
            }
        except Exception as e:
            logger.error(f"Failed to scroll: {e}")
            return {
                "success": False,
                "message": "Failed to scroll",
                "error": str(e)
            }

    def wait_for_image(self, image_path: str, timeout: int = 10, confidence: float = 0.8) -> Dict[str, Any]:
        """Wait for an image to appear on screen"""
        try:
            if not os.path.exists(image_path):
                return {
                    "success": False,
                    "message": f"Image file '{image_path}' not found"
                }

            start_time = time.time()
            while time.time() - start_time < timeout:
                location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if location is not None:
                    center = pyautogui.center(location)
                    return {
                        "success": True,
                        "message": f"Found image after {time.time() - start_time:.1f} seconds at {center}",
                        "position": center,
                        "wait_time": time.time() - start_time
                    }
                time.sleep(0.5)

            return {
                "success": False,
                "message": f"Image '{image_path}' not found within {timeout} seconds"
            }
        except Exception as e:
            logger.error(f"Failed to wait for image {image_path}: {e}")
            return {
                "success": False,
                "message": f"Failed to wait for image",
                "error": str(e)
            }