import pytest
from backend.ai.pipeline import process_audio

@pytest.mark.anyio
async def test_pipeline_skeleton():
    # Placeholder audio/text
    dummy_audio = "I want to transfer 2000 to John"

    # Run the async pipeline directly
    result = await process_audio(dummy_audio)

    print("Input Text:", result["text"])
    print("Detected Intent:", result["intent"])
    print("Response Text:", result["response_text"])
    print("Generated Audio File:", result["audio_file"])

# Run directly outside pytest
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_pipeline_skeleton())
