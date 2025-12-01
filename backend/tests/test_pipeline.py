# backend/tests/test_pipeline.py

from backend.ai.pipeline import process_audio_sync

def test_transfer_text():
    # Step 1: Input text
    text_input = "Transfer 2000 to John"

    # Step 2: Process through the pipeline
    result = process_audio_sync(text_input)

    # Step 3: Print result for inspection
    print("Pipeline output:", result)

    # Step 4: Assertions (checks automatically)
    assert result["intent"] == "transfer"
    assert result["entities"].get("amount") == 2000
    assert result["entities"].get("recipient") == "John"
