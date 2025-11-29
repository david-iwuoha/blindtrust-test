# backend/ai/tts.py

import os
import uuid
import requests
from datetime import datetime
import asyncio

# YarnGPT API key
YARN_API_KEY = "sk_live_-qoDWaPguo1ZFR47dUX-Jygei8RHo7lF0FV5VGAUauQ"
YARN_TTS_URL = "https://yarngpt.ai/api/v1/tts"

# Language to voice mapping
LANGUAGE_VOICES = {
    "english": "Idera",
    "igbo": "Chinenye",
    "yoruba": "Adaora",
    "hausa": "Zainab"
}


class TTSEngine:
    """YarnGPT Text-to-Speech engine."""

    def __init__(self):
        self.model_loaded = False

    def load_tts(self):
        """Simulate model loading (required by pipeline)."""
        self.model_loaded = True
        return "yarngpt-tts-model"

    async def text_to_speech(
        self, text: str, language_code: str = "english", output_format: str = "mp3"
    ) -> str:
        """Convert text to speech using YarnGPT API asynchronously."""
        if not text.strip():
            raise ValueError("Cannot synthesize empty text")

        voice = LANGUAGE_VOICES.get(language_code.lower(), "Idera")
        headers = {
            "Authorization": f"Bearer {YARN_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "voice": voice,
            "response_format": output_format
        }

        loop = asyncio.get_event_loop()
        try:
            # Run blocking requests.post in executor to avoid blocking event loop
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(YARN_TTS_URL, headers=headers, json=payload)
            )
        except Exception as e:
            print(f"[TTS] Request error: {e}")
            return ""

        if response.status_code != 200:
            print(f"[TTS] API error: {response.status_code} - {response.text}")
            return ""

        # Save audio to a timestamped file
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = f"output_{timestamp}.{output_format}"
        try:
            with open(filename, "wb") as f:
                f.write(response.content)
        except Exception as e:
            print(f"[TTS] Failed to save audio: {e}")
            return ""

        return filename


# Top-level async interface for pipeline
_tts_engine = TTSEngine()
_tts_engine.load_tts()


async def text_to_speech(
    text: str, language_code: str = "english", output_format: str = "mp3"
) -> str:
    """Async wrapper for pipeline usage."""
    return await _tts_engine.text_to_speech(text, language_code, output_format)


# Local testing
if __name__ == "__main__":
    import asyncio
    path = asyncio.run(text_to_speech("Hello, welcome to BlindTrust!", "english"))
    print(f"Generated TTS file: {path}")
