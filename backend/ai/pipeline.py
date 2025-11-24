# backend/ai/pipeline.py

"""
Full AI pipeline: STT → Intent → LLM → TTS.
"""

import asyncio
from .stt import STTEngine
from .intents import parse_intent
from .llm import generate_response
from .tts import _tts_engine
from .responses import get_template_response


# --- Updated parse_intent to handle all demo intents ---
def parse_intent(text: str):
    slots = {}
    text_lower = text.lower()

    if "transfer" in text_lower:
        intent = "transfer"
        # crude slot extraction
        words = text.split()
        try:
            amount_index = words.index("transfer") + 1
            to_index = words.index("to")
            slots["amount"] = int(words[amount_index])
            slots["recipient"] = words[to_index + 1]
        except (ValueError, IndexError):
            slots["amount"] = 0
            slots["recipient"] = ""
    elif "set language" in text_lower:
        intent = "set_language"
        slots["language"] = words[-1].lower()
    elif "my name is" in text_lower:
        intent = "provide_name"
        slots["user_name"] = words[-1]
    elif "my gender is" in text_lower:
        intent = "provide_gender"
        slots["gender"] = words[-1]
    elif "my phone is" in text_lower:
        intent = "provide_phone"
        slots["phone"] = words[-1]
    elif "confirm" in text_lower:
        intent = "confirm"
    elif "cancel" in text_lower:
        intent = "cancel"
    else:
        intent = "onboarding"

    return intent, slots


# --- Updated generate_response to return templates for demo intents ---
def generate_response(context, intent, slots):
    templates = {
        "onboarding": "Welcome to BlindTrust. Please tell me your name.",
        "set_language": f"Language set to {slots.get('language', 'English')}.",
        "provide_name": f"Hello {slots.get('user_name', 'user')}!",
        "provide_gender": f"Gender {slots.get('gender', 'unspecified')} recorded.",
        "provide_phone": f"Phone {slots.get('phone', 'unspecified')} recorded.",
        "transfer": f"Transfer of {slots.get('amount', 0)} to {slots.get('recipient', 'unknown')} successful.",
        "confirm": "Action confirmed.",
        "cancel": "Operation canceled."
    }
    return templates.get(intent)


async def process_audio(input_audio: str):
    """
    Main AI engine for BlindTrust.
    For now, input_audio is actually text (we'll replace with audio later).

    Returns a dict:
    {
        "text": "Processed text",
        "intent": "detected_intent",
        "slots": { ... },
        "response_text": "Generated response",
        "audio_file": "output.mp3"
    }
    """
    # --- Step 1: Convert audio to text ---
    stt_engine = STTEngine()
    text = input_audio  # placeholder: already text

    # --- Step 2: Detect intent and extract slots ---
    intent, slots = parse_intent(text)

    # --- Step 3: Generate response text ---
    response_text = generate_response(context=text, intent=intent, slots=slots)
    if not response_text:
        response_text = get_template_response(intent, slots)

    # --- Step 4: Convert text to speech (await async TTS) ---
    audio_file = await _tts_engine.text_to_speech(
        response_text, language_code=slots.get("language", "en")
    )

    return {
        "text": text,
        "intent": intent,
        "slots": slots,
        "response_text": response_text,
        "audio_file": audio_file
    }


def process_audio_sync(input_audio: str):
    """
    Sync wrapper for the async process_audio function.
    Useful for FastAPI endpoints.
    """
    return asyncio.run(process_audio(input_audio))


class AIPipeline:
    """
    Object-oriented wrapper for BlindTrust AI engine.
    """

    def __init__(self):
        self.stt_engine = STTEngine()
        # Future: self.llm, self.tts, self.intent_parser, etc.

    async def process(self, input_audio: str) -> dict:
        text = input_audio  # placeholder
        intent, slots = parse_intent(text)

        response_text = generate_response(context=text, intent=intent, slots=slots)
        if not response_text:
            response_text = get_template_response(intent, slots)

        audio_file = await _tts_engine.text_to_speech(
            response_text, language_code=slots.get("language", "en")
        )

        return {
            "text": text,
            "intent": intent,
            "slots": slots,
            "response_text": response_text,
            "audio_file": audio_file
        }

    def process_sync(self, input_audio: str) -> dict:
        return asyncio.run(self.process(input_audio))
