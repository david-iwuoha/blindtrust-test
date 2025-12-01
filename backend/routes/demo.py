# backend/routes/demo.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.ai.pipeline import process_audio
from backend.ai.tts import text_to_speech
from backend.db.helpers import (
    get_user_by_name,
    get_account_by_user_id,
    get_balance,
    update_balance,
    get_beneficiaries,
    add_beneficiary,
    transfer,
)

router = APIRouter(prefix="/demo", tags=["demo"])

@router.post("/interact")
async def demo_interaction(file: UploadFile = File(...)):
    # --- Step 0: Save uploaded audio temporarily ---
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # --- Step 1: Process audio through AI pipeline ---
    result = await process_audio(temp_path)  # async call
    intent = result.get("intent")
    slots = result.get("slots", {})
    user_name = slots.get("user_name")

    if not user_name:
        raise HTTPException(status_code=400, detail="Missing user_name in slots")

    user = get_user_by_name(user_name)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_name} not found")

    user_account = get_account_by_user_id(user[0])
    if not user_account:
        raise HTTPException(status_code=404, detail=f"Account for {user_name} not found")

    # --- Step 2: Live banking logic for transfer ---
    if intent == "transfer":
        recipient_name = slots.get("recipient")
        amount = slots.get("amount", 0)

        recipient = get_user_by_name(recipient_name)
        if not recipient:
            response = f"No beneficiary named {recipient_name}."
        else:
            recipient_account = get_account_by_user_id(recipient[0])
            success, msg = transfer(user_account[0], recipient_account[0], amount)
            response = msg if success else f"Transfer failed: {msg}"

        # Update response text & generate audio output
        result["response_text"] = response
        result["audio_output"] = await text_to_speech(
            response, language_code=slots.get("language", "en")
        )

    return result
