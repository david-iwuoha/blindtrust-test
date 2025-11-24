# backend/ai/tts.py

import os
import uuid

class TTSEngine:
    """Placeholder Text-to-Speech engine."""

    def __init__(self):
        self.model_loaded = False

    def load_tts(self):
        self.model_loaded = True
        return "placeholder-tts-model"

    async def text_to_speech(self, text: str, language_code: str = "en-NG") -> str:
        print(f"[TTS] Text: {text}, Language: {language_code}")
        output_path = f"output_{uuid.uuid4().hex}.mp3"
        with open(output_path, "wb") as f:
            f.write(b"FAKE_AUDIO_DATA")
        return output_path


# Top-level async function for pipeline import
_tts_engine = TTSEngine()
_tts_engine.load_tts()

async def text_to_speech(text: str, language_code: str = "en-NG") -> str:
    """Async interface, must be awaited."""
    return await _tts_engine.text_to_speech(text, language_code)
