# backend/routes/demo.py

from fastapi import APIRouter, UploadFile, File
from backend.ai.pipeline import process_audio
from backend.db.demo_accounts import demo_balance, beneficiaries
from backend.ai.tts import text_to_speech

router = APIRouter(prefix="/demo", tags=["demo"])

@router.post("/interact")
async def demo_interaction(file: UploadFile = File(...)):
    # --- Step 0: Save uploaded audio temporarily ---
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # --- Step 1: Process audio through AI pipeline ---
    result = await process_audio(temp_path)  # async call
    intent = result["intent"]
    slots = result.get("slots", {})
    user = slots.get("user_name", "user")

    # --- Step 2: Demo banking logic (transfer) ---
    if intent == "transfer":
        recipient = slots.get("recipient")
        amount = slots.get("amount", 0)

        if recipient not in beneficiaries:
            response = f"No beneficiary named {recipient}."
        elif demo_balance.get(user, 0) < amount:
            response = f"Insufficient funds. Your balance is {demo_balance.get(user)}."
        else:
            demo_balance[user] -= amount
            demo_balance[recipient] += amount
            response = f"Transfer of {amount} to {recipient} successful."

        # Update response text & generate audio output
        result["response_text"] = response
        result["audio_output"] = await text_to_speech(
            response, language_code=slots.get("language", "en")
        )

    return result
