# backend/ai/intents.py

class IntentResult:
    def __init__(self, intent: str, slots: dict = None):
        self.intent = intent
        self.slots = slots or {}

class IntentParser:
    """Rule-based intent extraction (placeholder)."""

    def parse(self, text: str) -> IntentResult:
        text_lower = text.lower()

        # simple placeholder rules
        if "language" in text_lower:
            return IntentResult("set_language")

        if "transfer" in text_lower:
            return IntentResult("transfer")

        if "yes" in text_lower:
            return IntentResult("confirm")

        if "no" in text_lower:
            return IntentResult("cancel")

        return IntentResult("unknown")


# function wrapper for pipeline.py
def parse_intent(text: str):
    parser = IntentParser()
    result = parser.parse(text)
    return result.intent, result.slots
