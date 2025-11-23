# backend/ai/stt.py

class STTEngine:
    """Placeholder Speech-to-Text engine.
    This will later load Whisper Tiny/Small and convert audio to text.
    """

    def __init__(self):
        self.model_loaded = False  # will become True when Whisper loads

    async def audio_to_text(self, audio_file: bytes) -> str:
        """Convert audio bytes to text.
        For now, returns placeholder text.
        Whisper integration comes in Phase 4.
        """
        return "placeholder text"
