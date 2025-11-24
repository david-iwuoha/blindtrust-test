# backend/ai/stt.py

"""
STT module for BlindTrust.
Handles audio → text using Whisper or future cloud services.
This keeps your class-based architecture so nothing breaks.
"""

import os


class STTEngine:
    """Placeholder Speech-to-Text engine.
    This will later load Whisper Tiny/Small and convert audio to text.
    """

    def __init__(self):
        self.model_loaded = False
        self.model = None

    def load_whisper(self):
        """Load Whisper model later. 
        For now, store placeholder so backend won't crash.
        """
        self.model = "placeholder-whisper-model"
        self.model_loaded = True
        return self.model

    async def audio_to_text(self, audio_file: bytes) -> str:
        """Convert audio bytes to text.
        For now, returns placeholder text.
        """
        print("[STT] Received audio input.")
        return "hello this is a placeholder stt result"
