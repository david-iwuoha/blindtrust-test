"""
Real STT module using whisper (openai-whisper) with a backward-compatible wrapper
so the rest of your backend will not crash.

Usage (new):
    from backend.ai.stt import audio_to_text

Usage (old, still supported):
    stt = STTEngine()
    text = await stt.audio_to_text(audio_bytes)
"""

from typing import Optional
import os
import traceback
import tempfile

# whisper requires ffmpeg
try:
    import whisper
except Exception:
    whisper = None

# ---- Config ----
DEFAULT_MODEL_SIZE = os.environ.get("WHISPER_MODEL_SIZE", "tiny")

_MODEL = None
_MODEL_SIZE = None


# -------------------------
#   Internal helpers
# -------------------------
def _load_model(model_size: Optional[str] = None):
    """Lazy load Whisper model only once."""
    global _MODEL, _MODEL_SIZE

    if model_size is None:
        model_size = DEFAULT_MODEL_SIZE

    if _MODEL is not None and _MODEL_SIZE == model_size:
        return _MODEL

    if whisper is None:
        raise RuntimeError(
            "whisper package not installed. Run: pip install openai-whisper"
        )

    print(f"[STT] Loading Whisper model '{model_size}'…")
    _MODEL = whisper.load_model(model_size, device="cpu")
    _MODEL_SIZE = model_size
    print("[STT] Whisper model loaded.")
    return _MODEL


def _clean_transcript(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.strip().split())


# -------------------------
#   Public API
# -------------------------
def audio_to_text(
    audio_path: str,
    model_size: Optional[str] = None,
    language: Optional[str] = None,
) -> str:
    """Transcribe a stored audio file."""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    model = _load_model(model_size)

    try:
        opts = {}
        if language:
            opts["language"] = language
            opts["task"] = "transcribe"

        print(f"[STT] Transcribing {audio_path} with model {_MODEL_SIZE}…")
        result = model.transcribe(audio_path, **opts)

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

    def __init__(self, model_size: str = None):
        self.model_size = model_size or DEFAULT_MODEL_SIZE

    def load_whisper(self):
        """For old code compatibility."""
        _load_model(self.model_size)
        return True

    async def audio_to_text(self, audio_file: bytes) -> str:
        """Accept raw audio bytes as before."""
        try:
            # Save temp file Whisper can read
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_file)
                tmp_path = tmp.name

            # Run real transcription
            return audio_to_text(tmp_path, model_size=self.model_size)

        except Exception as e:
            traceback.print_exc()
            print(f"[STT] Error: {e}")
            return ""
