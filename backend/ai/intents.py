# backend/ai/intents.py

"""
NLU / Intent Parser for BlindTrust demo.

Extracts intents and slots from raw transcribed speech.
Supports:
- onboarding
- set_language
- provide_name
- provide_gender
- provide_phone
- transfer
- amount
- confirm
- cancel
"""

import re

# List of supported languages for TTS/STT
LANGUAGES = ["english", "igbo", "yoruba", "hausa"]


class IntentResult:
    def __init__(self, intent: str, slots: dict = None):
        self.intent = intent
        self.slots = slots or {}


class IntentParser:
    """Rule-based intent extraction for BlindTrust demo."""

    def parse(self, text: str) -> IntentResult:
        text_lower = text.lower()
        slots = {}

        # --- Language selection ---
        for lang in LANGUAGES:
            if lang in text_lower:
                return IntentResult("set_language", {"language": lang})

        # --- Onboarding / profile info ---
        if "my name is" in text_lower or "i am" in text_lower:
            m = re.search(r"(?:my name is|i am) (\w+)", text_lower)
            if m:
                slots["user_name"] = m.group(1).capitalize()
            return IntentResult("provide_name", slots)

        if "male" in text_lower or "female" in text_lower:
            slots["gender"] = "male" if "male" in text_lower else "female"
            return IntentResult("provide_gender", slots)

        if re.search(r"\d{10}", text_lower):
            m = re.search(r"(\d{10})", text_lower)
            if m:
                slots["phone"] = m.group(1)
            return IntentResult("provide_phone", slots)

        # --- Transfer / amount ---
        if "transfer" in text_lower or "send" in text_lower:
            m_recipient = re.search(r"(?:to )(\w+)", text_lower)
            if m_recipient:
                slots["recipient"] = m_recipient.group(1).capitalize()
            m_amount = re.search(r"\b(\d{1,7})\b", text_lower)
            if m_amount:
                slots["amount"] = int(m_amount.group(1))
            return IntentResult("transfer", slots)

        # --- Confirm / cancel ---
        if "yes" in text_lower or "confirm" in text_lower:
            return IntentResult("confirm")
        if "no" in text_lower or "cancel" in text_lower:
            return IntentResult("cancel")

        # --- Fallback ---
        return IntentResult("unknown")


# Wrapper for backward compatibility (pipeline.py depends on this)
def parse_intent(text: str):
    parser = IntentParser()
    result = parser.parse(text)
    # Return a dict for tests expecting result["intent"]
    return {"intent": result.intent, "slots": result.slots}
