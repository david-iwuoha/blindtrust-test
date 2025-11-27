"""
Real STT module using Vosk (offline) with a backward-compatible wrapper
so the rest of your backend will not crash.

Usage (new):
    from backend.ai.stt import audio_to_text

Usage (old, still supported):
    stt = STTEngine()
    text = await stt.audio_to_text(audio_bytes)
"""

import os
import wave
import json
import tempfile
import traceback

try:
    from vosk import Model, KaldiRecognizer
except ImportError:
    Model = None
    KaldiRecognizer = None

# ---- Config ----
DEFAULT_MODEL_PATH = os.environ.get("VOSK_MODEL_PATH", "backend/ai/vosk-model")
_MODEL = None


# -------------------------
#   Internal helpers
# -------------------------
def _load_model(model_path: str = None):
    """Lazy load Vosk model only once."""
    global _MODEL
    if _MODEL is not None:
        return _MODEL

    if model_path is None:
        model_path = DEFAULT_MODEL_PATH

    if Model is None:
        raise RuntimeError(
            "vosk package not installed. Run: pip install vosk"
        )

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Vosk model not found at {model_path}")

    print(f"[STT] Loading Vosk model from '{model_path}'…")
    _MODEL = Model(model_path)
    print("[STT] Vosk model loaded.")
    return _MODEL


def _clean_transcript(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.strip().split())


# -------------------------
#   Public API
# -------------------------
def audio_to_text(audio_path: str) -> str:
    """Transcribe a stored WAV audio file using Vosk."""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    model = _load_model()

    try:
        wf = wave.open(audio_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            raise ValueError("Audio file must be WAV PCM mono 16-bit")

        rec = KaldiRecognizer(model, wf.getframerate())
        result_text = []

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                result_text.append(res.get("text", ""))

        final_res = json.loads(rec.FinalResult())
        result_text.append(final_res.get("text", ""))

        text = " ".join(filter(None, result_text))
        text = _clean_transcript(text)
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
