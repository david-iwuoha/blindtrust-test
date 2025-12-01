# backend/tests/test_pipeline_tts_audio.py

from backend.ai.pipeline import process_audio_sync
import os

def test_full_pipeline_tts_audio():
    # Path to your recorded audio
    audio_file = "backend/tests/audio/test_full_pipeline.mp3"

    # Run the full pipeline (STT → Intent → Response → TTS)
    result = process_audio_sync(audio_file)
    print("Full pipeline output:", result)

    # --- Assertions ---
    # Ensure STT produced a transcript
    assert result.get("transcript"), "No transcript generated"

    # Ensure intent and entities are detected
    assert "intent" in result, "Intent not detected"
    assert "entities" in result, "Entities missing"

    # Ensure a response text was generated
    assert result.get("response_text"), "Response text missing"

    # Ensure TTS generated an audio file
    tts_path = result.get("response_audio_path")
    assert tts_path and os.path.exists(tts_path), f"TTS audio not generated: {tts_path}"
    assert tts_path.endswith(".mp3"), "TTS file is not an mp3"

    print(f"TTS file generated successfully: {tts_path}")
