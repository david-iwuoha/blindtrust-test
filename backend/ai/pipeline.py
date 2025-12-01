# backend/ai/pipeline.py

"""
Full AI pipeline for BlindTrust:
1. Audio → Text (STT)
2. Intent Extraction (NLU)
3. Generate Response (dummy logic for now)
4. Text → Audio (TTS)
"""

import asyncio
from backend.ai.stt import STTEngine, audio_to_text
from backend.ai.intents import IntentParser
from backend.ai.tts import _tts_engine, text_to_speech

# ---------------------------
# NLU / Intent Extraction
# ---------------------------
intent_parser = IntentParser()

def run_nlu(text: str) -> dict:
    """
    Run NLU to extract intent and slots from text.
    Returns dict with keys:
        - intent
        - slots
    """
    result = intent_parser.parse(text)
    return {"intent": result.intent, "entities": result.slots}


# ---------------------------
# Main Pipeline
# ---------------------------
async def process_audio(input_audio: str, language: str = "english") -> dict:
    """
    Process audio end-to-end:
    1. STT
    2. NLU / Intent
    3. Dummy response logic
    4. TTS
    """

    # Step 1: Convert audio to text
    if input_audio.endswith((".mp3", ".wav", ".m4a", ".ogg")):
        # Treat as actual audio file
        stt_engine = STTEngine()
        transcript = await stt_engine.audio_to_text(open(input_audio, "rb").read())
    else:
        # Already text (for testing)
        transcript = input_audio

    # Step 2: Detect intent
    nlu_result = run_nlu(transcript)
    intent = nlu_result.get("intent", "unknown")
    entities = nlu_result.get("entities", {})

    # Step 3: Dummy bank logic / response templates
    if intent == "check_balance":
        bot_response = "Your account balance is ten thousand naira."
    elif intent == "send_money" or intent == "transfer":
        amount = entities.get("amount", "an unknown amount")
        receiver = entities.get("recipient", "the user")
        bot_response = f"Sending {amount} to {receiver} is not yet enabled in this demo."
    elif intent == "greeting":
        bot_response = "Hello! How can I assist you today?"
    elif intent == "set_language":
        bot_response = f"Language set to {entities.get('language', 'English')}."
    elif intent == "provide_name":
        bot_response = f"Hello {entities.get('user_name', 'user')}!"
    elif intent == "provide_gender":
        bot_response = f"Gender {entities.get('gender', 'unspecified')} recorded."
    elif intent == "provide_phone":
        bot_response = f"Phone {entities.get('phone', 'unspecified')} recorded."
    elif intent == "confirm":
        bot_response = "Action confirmed."
    elif intent == "cancel":
        bot_response = "Operation canceled."
    else:
        bot_response = "Sorry, I did not understand your request."

    # Step 4: Convert response text to speech
    response_audio_path = await _tts_engine.text_to_speech(
        bot_response, language_code=entities.get("language", language)
    )

    return {
        "transcript": transcript,
        "intent": intent,
        "entities": entities,
        "response_text": bot_response,
        "response_audio_path": response_audio_path
    }


# ---------------------------
# Sync Wrapper
# ---------------------------
def process_audio_sync(input_audio: str, language: str = "english") -> dict:
    """
    Synchronous wrapper for FastAPI endpoints.
    """
    return asyncio.run(process_audio(input_audio, language))


# ---------------------------
# Object-oriented pipeline
# ---------------------------
class AIPipeline:
    """
    Object-oriented wrapper for BlindTrust AI engine.
    """

    def __init__(self):
        self.stt_engine = STTEngine()
        self.intent_parser = IntentParser()

    async def process(self, input_audio: str, language: str = "english") -> dict:
        # Step 1: STT
        if input_audio.endswith((".mp3", ".wav", ".m4a", ".ogg")):
            transcript = await self.stt_engine.audio_to_text(open(input_audio, "rb").read())
        else:
            transcript = input_audio

        # Step 2: Intent extraction
        nlu_result = run_nlu(transcript)
        intent = nlu_result.get("intent", "unknown")
        entities = nlu_result.get("entities", {})

        # Step 3: Dummy response
        if intent == "check_balance":
            bot_response = "Your account balance is ten thousand naira."
        elif intent == "send_money" or intent == "transfer":
            amount = entities.get("amount", "an unknown amount")
            receiver = entities.get("recipient", "the user")
            bot_response = f"Sending {amount} to {receiver} is not yet enabled in this demo."
        elif intent == "greeting":
            bot_response = "Hello! How can I assist you today?"
        elif intent == "set_language":
            bot_response = f"Language set to {entities.get('language', 'English')}."
        elif intent == "provide_name":
            bot_response = f"Hello {entities.get('user_name', 'user')}!"
        elif intent == "provide_gender":
            bot_response = f"Gender {entities.get('gender', 'unspecified')} recorded."
        elif intent == "provide_phone":
            bot_response = f"Phone {entities.get('phone', 'unspecified')} recorded."
        elif intent == "confirm":
            bot_response = "Action confirmed."
        elif intent == "cancel":
            bot_response = "Operation canceled."
        else:
            bot_response = "Sorry, I did not understand your request."

        # Step 4: TTS
        response_audio_path = await _tts_engine.text_to_speech(
            bot_response, language_code=entities.get("language", language)
        )

        return {
            "transcript": transcript,
            "intent": intent,
            "entities": entities,
            "response_text": bot_response,
            "response_audio_path": response_audio_path
        }

    def process_sync(self, input_audio: str, language: str = "english") -> dict:
        return asyncio.run(self.process(input_audio, language))
