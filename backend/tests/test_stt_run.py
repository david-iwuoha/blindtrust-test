from backend.ai.stt import audio_to_text

def test_local_stt():
    sample = "backend/tests/audio/dummy.wav"
    text = audio_to_text(sample)
    print("TRANSCRIPT:", text)

if __name__ == "__main__":  
    test_local_stt()
