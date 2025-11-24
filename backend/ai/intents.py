# backend/ai/intents.py

"""
Intent and slot extraction for BlindTrust.
Handles onboarding, language selection, transfers, confirmations, etc.
"""

import re

# Unified INTENTS list
INTENTS = [
    "onboarding",
    "set_language",
    "provide_name",
    "provide_gender",
    "provide_phone",
    "transfer",
    "amount",
    "confirm",
    "cancel",
]


class IntentResult:
    def __init__(self, intent: str, slots: dict = None):
        self.intent = intent
        self.slots = slots or {}


class IntentParser:
    """Rule-based intent extraction (placeholder) for demo purposes."""

    def parse(self, text: str) -> IntentResult:
        text_lower = text.lower()

        # ===== language selection =====
        if any(lang in text_lower for lang in ["english", "igbo", "yoruba", "hausa"]):
            return IntentResult("set_language", {"language": text_lower})

        # ===== provide name =====
        if "my name is" in text_lower:
            name_match = re.search(r"my name is (\w+)", text_lower)
            name = name_match.group(1) if name_match else "user"
            return IntentResult("provide_name", {"user_name": name})

        # ===== provide gender =====
        if any(g in text_lower for g in ["male", "female"]):
            gender = "male" if "male" in text_lower else "female"
            return IntentResult("provide_gender", {"gender": gender})

        # ===== provide phone =====
        if "phone" in text_lower or re.search(r"\d{10,}", text_lower):
            phone_match = re.search(r"(\d{10,})", text_lower)
            phone = phone_match.group(1) if phone_match else None
            return IntentResult("provide_phone", {"phone": phone})

        # ===== transfer =====
        if "transfer" in text_lower:
            # extract amount
            amount_match = re.search(r"transfer (\d+)", text_lower)
            amount = int(amount_match.group(1)) if amount_match else 0

            # extract recipient
            recipient_match = re.search(r"to (\w+)", text_lower)
            recipient = recipient_match.group(1) if recipient_match else ""

            return IntentResult("transfer", {"amount": amount, "recipient": recipient})

        # ===== confirmations =====
        if "yes" in text_lower:
            return IntentResult("confirm")
        if "no" in text_lower:
            return IntentResult("cancel")

        # ===== default fallback =====
        return IntentResult("onboarding")


# Wrapper (pipeline.py depends on this)
def parse_intent(text: str):
    parser = IntentParser()
    result = parser.parse(text)
    return result.intent, result.slots
