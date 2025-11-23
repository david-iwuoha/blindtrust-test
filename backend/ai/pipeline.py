# backend/ai/pipeline.py
from .stt import STTEngine  # placeholder STT engine (Whisper Tiny/Small later)
from .intents import parse_intent
from .llm import generate_response
from .tts import text_to_speech
from .responses import get_template_response
import asyncio

async def process_audio(input_audio: str):
    """
    Main AI engine for BlindTrust.
    For now, input_audio is actually text (we'll replace with audio later).

    Returns a dict:
    {
        "text": "Processed text",
        "intent": "detected_intent",
        "slots": { ... },
        "audio_file": "output.mp3"
    }
    """
    # --- Step 1: Convert audio to text ---
    # For now, input_audio is already text
    stt_engine = STTEngine()
    # Later integration: text = await stt_engine.audio_to_text(input_audio)
    text = input_audio  # placeholder for demo

    # --- Step 2: Detect intent and extract arguments ---
    intent, slots = parse_intent(text)

    # --- Step 3: Generate response text ---
    # Try LLM first, fallback to template messages
    response_text = generate_response(context=text, intent=intent, slots=slots)
    if not response_text:
        response_text = get_template_response(intent, slots)

    # --- Step 4: Convert text to speech ---
    audio_file = text_to_speech(response_text, language_code=slots.get("language", "en"))

    return {
        "text": text,
        "intent": intent,
        "slots": slots,
        "response_text": response_text,
        "audio_file": audio_file
    }

# Helper to call async function from sync code (e.g., FastAPI endpoint)
def process_audio_sync(input_audio: str):
    return asyncio.run(process_audio(input_audio))


class AIPipeline:
    """
    Wrapper class for BlindTrust AI engine.
    Use this to process audio/text in a single object-oriented call.
    """

    def __init__(self):
        self.stt_engine = STTEngine()
        # Future integrations: self.llm, self.tts, self.intent_parser, etc.

    async def process(self, input_audio: str) -> dict:
        """
        Async method to process input audio/text and return structured response.
        """
        # Step 1: Convert audio to text
        # text = await self.stt_engine.audio_to_text(input_audio)
        text = input_audio  # placeholder for demo

        # Step 2: Detect intent and slots
        intent, slots = parse_intent(text)

        # Step 3: Generate response text
        response_text = generate_response(context=text, intent=intent, slots=slots)
        if not response_text:
            response_text = get_template_response(intent, slots)

        # Step 4: Convert text to speech
        audio_file = text_to_speech(response_text, language_code=slots.get("language", "en"))

        return {
            "text": text,
            "intent": intent,
            "slots": slots,
            "response_text": response_text,
            "audio_file": audio_file
        }

    def process_sync(self, input_audio: str) -> dict:
        """
        Sync wrapper for the async process method.
        """
        return asyncio.run(self.process(input_audio))
