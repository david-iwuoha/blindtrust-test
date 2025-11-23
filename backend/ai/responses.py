# backend/ai/responses.py

# Language packs (placeholder)
NIGERIAN_ENGLISH = {
    "welcome": "Welcome to BlindTrust.",
    "ask_language": "What language would you prefer: Igbo, Yoruba, Hausa or English?",
}

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
    """Pulls system messages, templates, confirmations."""

    def __init__(self):
        self.languages = {
            "en-NG": NIGERIAN_ENGLISH,
            "ig-NG": IGBO,
            "yo-NG": YORUBA,
            "ha-NG": HAUSA
        }

    def get_message(self, lang: str, key: str) -> str:
        pack = self.languages.get(lang, NIGERIAN_ENGLISH)
        return pack.get(key, "Message not found.")


def get_template_response(intent: str, slots: dict) -> str:
    """
    Placeholder template-based response generator.
    Returns a simple string for now.
    """
    return f"Placeholder response for intent '{intent}' with slots {slots}"
