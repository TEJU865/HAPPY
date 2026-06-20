"""
Voice Output Tool for HAPPY
Text-to-speech using pyttsx3
"""

import pyttsx3
from typing import Dict, Any, Optional
import threading
import logging

logger = logging.getLogger(__name__)

class VoiceOutput:
    """Text-to-speech functionality"""

    def __init__(self):
        self.engine = None
        self.is_speaking = False
        self._init_engine()

    def _init_engine(self):
        """Initialize the TTS engine"""
        try:
            self.engine = pyttsx3.init()
            # Configure voice settings
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to use a female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break

            # Set speech rate (words per minute)
            self.engine.setProperty('rate', 180)

            # Set volume (0.0 to 1.0)
            self.engine.setProperty('volume', 0.8)

            logger.info("Voice output initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize voice output: {e}")
            self.engine = None

    def speak(self, text: str, wait: bool = False) -> Dict[str, Any]:
        """Convert text to speech"""
        if not self.engine:
            return {
                "success": False,
                "message": "Voice output not available",
                "error": "TTS engine not initialized"
            }

        if self.is_speaking:
            return {
                "success": False,
                "message": "Already speaking, please wait",
                "error": "Speech in progress"
            }

        try:
            self.is_speaking = True

            def speak_thread():
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                finally:
                    self.is_speaking = False

            if wait:
                # Synchronous speech
                self.engine.say(text)
                self.engine.runAndWait()
                self.is_speaking = False
                return {
                    "success": True,
                    "message": f"Spoke: '{text}'"
                }
            else:
                # Asynchronous speech
                thread = threading.Thread(target=speak_thread, daemon=True)
                thread.start()
                return {
                    "success": True,
                    "message": f"Speaking: '{text}'"
                }

        except Exception as e:
            self.is_speaking = False
            logger.error(f"Failed to speak text: {e}")
            return {
                "success": False,
                "message": "Failed to speak text",
                "error": str(e)
            }

    def stop_speaking(self) -> Dict[str, Any]:
        """Stop current speech"""
        try:
            if self.engine and self.is_speaking:
                self.engine.stop()
                self.is_speaking = False
                return {
                    "success": True,
                    "message": "Speech stopped"
                }
            else:
                return {
                    "success": True,
                    "message": "No speech to stop"
                }
        except Exception as e:
            logger.error(f"Failed to stop speech: {e}")
            return {
                "success": False,
                "message": "Failed to stop speech",
                "error": str(e)
            }

    def set_voice(self, voice_index: int = 0) -> Dict[str, Any]:
        """Change the voice"""
        try:
            if not self.engine:
                return {
                    "success": False,
                    "message": "Voice output not available"
                }

            voices = self.engine.getProperty('voices')
            if voices and 0 <= voice_index < len(voices):
                self.engine.setProperty('voice', voices[voice_index].id)
                return {
                    "success": True,
                    "message": f"Voice changed to {voices[voice_index].name}"
                }
            else:
                return {
                    "success": False,
                    "message": "Invalid voice index"
                }
        except Exception as e:
            logger.error(f"Failed to set voice: {e}")
            return {
                "success": False,
                "message": "Failed to change voice",
                "error": str(e)
            }

    def set_rate(self, rate: int) -> Dict[str, Any]:
        """Set speech rate (words per minute)"""
        try:
            if not self.engine:
                return {
                    "success": False,
                    "message": "Voice output not available"
                }

            # Clamp rate between 50-300
            rate = max(50, min(300, rate))
            self.engine.setProperty('rate', rate)
            return {
                "success": True,
                "message": f"Speech rate set to {rate} words per minute"
            }
        except Exception as e:
            logger.error(f"Failed to set speech rate: {e}")
            return {
                "success": False,
                "message": "Failed to set speech rate",
                "error": str(e)
            }

    def set_volume(self, volume: float) -> Dict[str, Any]:
        """Set speech volume (0.0 to 1.0)"""
        try:
            if not self.engine:
                return {
                    "success": False,
                    "message": "Voice output not available"
                }

            # Clamp volume between 0.0-1.0
            volume = max(0.0, min(1.0, volume))
            self.engine.setProperty('volume', volume)
            return {
                "success": True,
                "message": f"Volume set to {volume}"
            }
        except Exception as e:
            logger.error(f"Failed to set volume: {e}")
            return {
                "success": False,
                "message": "Failed to set volume",
                "error": str(e)
            }

    def get_status(self) -> Dict[str, Any]:
        """Get current voice settings"""
        try:
            if not self.engine:
                return {
                    "success": False,
                    "message": "Voice output not available"
                }

            voices = self.engine.getProperty('voices')
            current_voice = self.engine.getProperty('voice')
            rate = self.engine.getProperty('rate')
            volume = self.engine.getProperty('volume')

            voice_names = [v.name for v in voices] if voices else []

            return {
                "success": True,
                "message": "Voice status retrieved",
                "settings": {
                    "voices": voice_names,
                    "current_voice": current_voice,
                    "rate": rate,
                    "volume": volume,
                    "is_speaking": self.is_speaking
                }
            }
        except Exception as e:
            logger.error(f"Failed to get voice status: {e}")
            return {
                "success": False,
                "message": "Failed to get voice status",
                "error": str(e)
            }