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
import os

router = APIRouter(prefix="/demo", tags=["demo"])

@router.post("/interact")
async def demo_interaction(file: UploadFile = File(...)):
    # --- Step 1: Save uploaded audio temporarily ---
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # --- Step 2: Run AI pipeline ---
    result = await process_audio(temp_path)
    intent = result.get("intent")
    entities = result.get("entities", {})

    # Extract main values
    user_name = entities.get("user_name")
    language = entities.get("language", "en")

    if not user_name:
        raise HTTPException(status_code=400, detail="Missing user_name in input speech")

    # --- Step 3: Fetch user + account ---
    user = get_user_by_name(user_name)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_name} not found")

    user_id = user[0]
    user_account = get_account_by_user_id(user_id)

    if not user_account:
        raise HTTPException(status_code=404, detail=f"No account found for {user_name}")

    user_account_id = user_account[0]

    response_text = "I could not understand your request."

    # --- Step 4: Banking intent handling ---
    if intent == "check_balance":
        balance = get_balance(user_account_id)
        response_text = f"Your balance is {balance} naira."

    elif intent == "transfer":
        recipient_name = entities.get("recipient")
        amount = float(entities.get("amount", 0))

        if not recipient_name:
            response_text = "Please say the recipient name."
        else:
            recipient = get_user_by_name(recipient_name)
            if not recipient:
                response_text = f"I couldn't find any user named {recipient_name}."
            else:
                recipient_account = get_account_by_user_id(recipient[0])
                success, msg = transfer(user_account_id, recipient_account[0], amount)
                response_text = msg

    elif intent == "add_beneficiary":
        beneficiary_name = entities.get("beneficiary_name")
        if beneficiary_name:
            # Here we assume user says: "add John as beneficiary"
            recipient = get_user_by_name(beneficiary_name)
            if recipient:
                recipient_acc = get_account_by_user_id(recipient[0])
                add_beneficiary(user_id, beneficiary_name, recipient_acc[0])
                response_text = f"{beneficiary_name} added as beneficiary."
            else:
                response_text = f"No user named {beneficiary_name} found."
        else:
            response_text = "Please say a beneficiary name."

    elif intent == "greeting":
        response_text = "Hello! How can I help you?"

    elif intent == "set_language":
        response_text = f"Language set to {language}."

    elif intent == "confirm":
        response_text = "Confirmed."

    elif intent == "cancel":
        response_text = "Cancelled."

    # --- Step 5: Final TTS output ---
    audio_file = await text_to_speech(response_text, language_code=language)

    # Cleanup
    try:
        os.remove(temp_path)
    except:
        pass

    # --- Final merged response ---
    return {
        "transcript": result.get("transcript"),
        "intent": intent,
        "entities": entities,
        "response_text": response_text,
        "audio_output": audio_file,
    }
