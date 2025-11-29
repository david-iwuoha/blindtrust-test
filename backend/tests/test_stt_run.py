from backend.ai.stt import audio_to_text

def test_local_stt():
    sample = "backend/tests/audio/Balance.mp3"
    # Force transcription in English
    text = audio_to_text(sample, language="ig")
    print("TRANSCRIPT:", text)

if __name__ == "__main__":  
    test_local_stt()
