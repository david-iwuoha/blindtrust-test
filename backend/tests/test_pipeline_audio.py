from backend.ai.pipeline import process_audio_sync

def test_transfer_audio():
    audio_file = "backend/tests/audio/test_transfer.mp3"
    result = process_audio_sync(audio_file)
    print("Pipeline output:", result)

    assert result["intent"] == "transfer"
    assert result["entities"].get("recipient") == "John"
    assert result["entities"].get("amount") == 2000
