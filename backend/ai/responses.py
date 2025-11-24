# backend/ai/responses.py

"""
Language packs and template-based responses for BlindTrust.
Contains fixed responses for onboarding, confirmations, and banking messages.
"""

# Full Nigerian English pack
NIGERIAN_ENGLISH = {
    "welcome": "Welcome to BlindTrust.",
    "ask_language": "What language would you prefer?",
    "ask_name": "Please tell me your name.",
}

# Other languages (still minimal for now)
IGBO = {
    "welcome": "Nnọọ na BlindTrust.",
}

YORUBA = {
    "welcome": "Kaabo si BlindTrust.",
}

HAUSA = {
    "welcome": "Barka da zuwa BlindTrust.",
}


class ResponseBuilder:
    """Language pack helper that returns system messages for each language."""

    def __init__(self):
        self.languages = {
            "en-NG": NIGERIAN_ENGLISH,
            "ig-NG": IGBO,
            "yo-NG": YORUBA,
            "ha-NG": HAUSA,
        }

    def get_message(self, lang: str, key: str) -> str:
        """Return a single message from the language pack."""
        pack = self.languages.get(lang, NIGERIAN_ENGLISH)
        return pack.get(key, "Message not found.")


def get_template_response(intent: str, slots: dict) -> str:
    """
    Simple placeholder template generator.
    Helps the pipeline when LLM is unavailable.
    """
    return f"Placeholder response for intent '{intent}' with slots {slots}"
