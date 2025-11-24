# backend/ai/llm.py

"""
Local LLM interface for BlindTrust.
Handles conversational reasoning and smart fallback responses.
"""

def llm_attempt(context: dict, intent: str, slots: dict):
    """
    Placeholder for future LLM-based response generation.
    Returns None for now so system falls back to deterministic replies.
    """
    # Example for later:
    # return f"LLM response to intent '{intent}' with context {context}"
    return None


def generate_response(context: dict, intent: str, slots: dict) -> str:
    """
    Unified response generator.
    Tries LLM first, falls back to deterministic responses.
    """

    # 1. Try LLM first
    llm_reply = llm_attempt(context, intent, slots)
    if llm_reply:
        return llm_reply

    # 2. Deterministic fallback responses
    if intent == "onboarding":
        return "Welcome to BlindTrust. Please tell me your name."

    if intent == "set_language":
        return f"Language set to {slots.get('language', 'English')}."

    if intent == "transfer":
        return "Who would you like to transfer to?"

    if intent == "confirm":
        return "Confirmed."

    if intent == "cancel":
        return "Action cancelled."

    return "I did not understand that. Please repeat."
