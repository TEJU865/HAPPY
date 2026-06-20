"""
Voice Input Tool for HAPPY
Speech-to-text using faster-whisper
"""

import os
import tempfile
import threading
import time
from typing import Dict, Any, Optional, Callable
import logging
import pyaudio
import wave
import audioop
from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)

class VoiceInput:
    """Speech-to-text functionality"""

    def __init__(self, model_size: str = "base"):
        self.model = None
        self.is_listening = False
        self.audio = None
        self.stream = None
        self.frames = []
        self.model_size = model_size
        self.sample_rate = 16000
        self.channels = 1
        self.chunk_size = 1024
        self.silence_threshold = 500  # Adjust based on your microphone
        self.silence_duration = 2.0  # Seconds of silence to stop recording
        self._init_model()

    def _init_model(self):
        """Initialize the Whisper model"""
        try:
            # Use CPU for now (can be changed to GPU later)
            self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
            logger.info(f"Voice input initialized with {self.model_size} model")
        except Exception as e:
            logger.error(f"Failed to initialize voice input model: {e}")
            self.model = None

    def _open_audio_stream(self):
        """Open audio stream for recording"""
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            logger.info("Audio stream opened")
        except Exception as e:
            logger.error(f"Failed to open audio stream: {e}")
            raise

    def _close_audio_stream(self):
        """Close audio stream"""
        try:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.audio:
                self.audio.terminate()
            logger.info("Audio stream closed")
        except Exception as e:
            logger.error(f"Error closing audio stream: {e}")

    def _is_silent(self, data):
        """Check if audio data is silent"""
        rms = audioop.rms(data, 2)  # 2 bytes per sample for paInt16
        return rms < self.silence_threshold

    def _record_audio(self) -> str:
        """Record audio until silence is detected"""
        self.frames = []
        silent_chunks = 0
        silent_limit = int(self.silence_duration * self.sample_rate / self.chunk_size)

        print("🎤 Listening... Speak now!")

        while self.is_listening:
            try:
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                self.frames.append(data)

                if self._is_silent(data):
                    silent_chunks += 1
                    if silent_chunks > silent_limit:
                        print("🔇 Silence detected, stopping recording")
                        break
                else:
                    silent_chunks = 0

            except Exception as e:
                logger.error(f"Error during recording: {e}")
                break

        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_filename = temp_file.name

        try:
            with wave.open(temp_filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(self.frames))

            return temp_filename
        except Exception as e:
            logger.error(f"Failed to save audio file: {e}")
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
            raise

    def _transcribe_audio(self, audio_file: str) -> str:
        """Transcribe audio file to text"""
        try:
            segments, info = self.model.transcribe(audio_file, beam_size=5)

            text = ""
            for segment in segments:
                text += segment.text

            confidence = info.language_probability
            logger.info(f"Transcription completed with confidence: {confidence}")

            return text.strip()
        except Exception as e:
            logger.error(f"Failed to transcribe audio: {e}")
            raise

    def listen_and_transcribe(self, timeout: int = 30) -> Dict[str, Any]:
        """Listen for speech and convert to text"""
        if not self.model:
            return {
                "success": False,
                "message": "Voice input not available",
                "error": "Whisper model not initialized"
            }

        if self.is_listening:
            return {
                "success": False,
                "message": "Already listening",
                "error": "Recording in progress"
            }

        audio_file = None
        try:
            self.is_listening = True
            self._open_audio_stream()

            # Start recording in a separate thread with timeout
            def record_with_timeout():
                try:
                    audio_file = self._record_audio()
                    return audio_file
                except Exception as e:
                    logger.error(f"Recording failed: {e}")
                    return None

            record_thread = threading.Thread(target=record_with_timeout, daemon=True)
            record_thread.start()
            record_thread.join(timeout)

            if record_thread.is_alive():
                self.is_listening = False
                self._close_audio_stream()
                return {
                    "success": False,
                    "message": "Recording timed out",
                    "error": f"No speech detected within {timeout} seconds"
                }

            if not audio_file:
                return {
                    "success": False,
                    "message": "Recording failed"
                }

            # Transcribe
            text = self._transcribe_audio(audio_file)

            return {
                "success": True,
                "message": f"Transcribed: '{text}'",
                "text": text
            }

        except Exception as e:
            logger.error(f"Voice input failed: {e}")
            return {
                "success": False,
                "message": "Voice input failed",
                "error": str(e)
            }
        finally:
            self.is_listening = False
            self._close_audio_stream()
            if audio_file and os.path.exists(audio_file):
                os.unlink(audio_file)

    def listen_async(self, callback: Callable[[Dict[str, Any]], None], timeout: int = 30):
        """Listen asynchronously and call callback with result"""
        def listen_thread():
            result = self.listen_and_transcribe(timeout)
            callback(result)

        thread = threading.Thread(target=listen_thread, daemon=True)
        thread.start()

    def stop_listening(self) -> Dict[str, Any]:
        """Stop current listening session"""
        if self.is_listening:
            self.is_listening = False
            return {
                "success": True,
                "message": "Stopped listening"
            }
        else:
            return {
                "success": True,
                "message": "Not currently listening"
            }

    def calibrate_silence(self, duration: int = 3) -> Dict[str, Any]:
        """Calibrate silence threshold based on current environment"""
        try:
            print(f"🎤 Calibrating silence for {duration} seconds...")

            self._open_audio_stream()
            samples = []

            start_time = time.time()
            while time.time() - start_time < duration:
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                rms = audioop.rms(data, 2)
                samples.append(rms)

            self._close_audio_stream()

            if samples:
                avg_rms = sum(samples) / len(samples)
                # Set threshold slightly above average ambient noise
                self.silence_threshold = int(avg_rms * 1.5)

                return {
                    "success": True,
                    "message": f"Silence threshold calibrated to {self.silence_threshold}",
                    "threshold": self.silence_threshold,
                    "average_noise": avg_rms
                }
            else:
                return {
                    "success": False,
                    "message": "Calibration failed - no audio samples"
                }

        except Exception as e:
            logger.error(f"Calibration failed: {e}")
            return {
                "success": False,
                "message": "Calibration failed",
                "error": str(e)
            }

    def get_status(self) -> Dict[str, Any]:
        """Get current voice input status"""
        return {
            "success": True,
            "message": "Voice input status",
            "status": {
                "model_loaded": self.model is not None,
                "model_size": self.model_size,
                "is_listening": self.is_listening,
                "silence_threshold": self.silence_threshold,
                "sample_rate": self.sample_rate
            }
        }