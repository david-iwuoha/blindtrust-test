# backend/ai/stt.py

"""
Real STT module using Whisper (OpenAI) with a backward-compatible wrapper
so the rest of your backend will not crash.

Usage (new):
    from backend.ai.stt import audio_to_text
    text = audio_to_text("path/to/file.wav")

Usage (old, still supported):
    stt = STTEngine()
    text = await stt.audio_to_text(audio_bytes)
"""

import os
import tempfile
import traceback
from typing import Optional

# Whisper is CPU-friendly but models still take RAM/disk.
try:
    import whisper
except ImportError:
    whisper = None

# ---- Config ----
DEFAULT_MODEL_SIZE = os.environ.get("WHISPER_MODEL_SIZE", "tiny")  # "tiny" | "small" | "base" | ...
_MODEL = None
_MODEL_SIZE = None

# -------------------------
#   Internal helpers
# -------------------------
def _load_model(model_size: Optional[str] = None):
    """Lazy load Whisper model and return it."""
    global _MODEL, _MODEL_SIZE
    if model_size is None:
        model_size = DEFAULT_MODEL_SIZE

    if _MODEL is not None and _MODEL_SIZE == model_size:
        return _MODEL

    if whisper is None:
        raise RuntimeError("whisper package not installed. Run: pip install openai-whisper")

    print(f"[STT] Loading Whisper model '{model_size}' (this may take a while)...")
    try:
        _MODEL = whisper.load_model(model_size, device="cpu")
        _MODEL_SIZE = model_size
        print("[STT] Whisper model loaded.")
        return _MODEL
    except Exception as exc:
        traceback.print_exc()
        raise RuntimeError(f"Failed to load Whisper model '{model_size}': {exc}")


def _clean_transcript(text: str) -> str:
    """Simple cleaning for transcription text."""
    if not text:
        return ""
    return " ".join(text.strip().split())


# -------------------------
#   Public API
# -------------------------
def audio_to_text(audio_path: str, model_size: Optional[str] = None, language: Optional[str] = None) -> str:
    """
    Transcribe audio file to text using Whisper.

    Args:
        audio_path: Path to audio file (wav, mp3, m4a, etc).
        model_size: Optional override of model size ("tiny","small",...).
        language: Optional ISO code or hint (e.g. "en", "ig", "yo", "ha").

    Returns:
        Cleaned transcript string.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    model = _load_model(model_size)

    try:
        options = {"task": "transcribe"}
        if language:
            options["language"] = language

        print(f"[STT] Transcribing {audio_path} with model {_MODEL_SIZE}...")
        result = model.transcribe(audio_path, **options)
        text = _clean_transcript(result.get("text", ""))
        print(f"[STT] Transcript: {text}")
        return text

    except Exception as e:
        traceback.print_exc()
        print(f"[STT] Error during transcription: {e}")
        return ""


# --------------------------------------------------
#  Backward-compatible class for older architecture
# --------------------------------------------------
class STTEngine:
    """
    Compatibility wrapper so your existing pipeline continues working.
    Stores audio bytes temporarily and calls audio_to_text().
    """

    def __init__(self):
        # preload Whisper model
        _load_model()

    async def audio_to_text(self, audio_file: bytes) -> str:
        """Accept raw audio bytes as before."""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_file)
                tmp_path = tmp.name

            return audio_to_text(tmp_path)

        except Exception as e:
            traceback.print_exc()
            print(f"[STT] Error: {e}")
            return ""
