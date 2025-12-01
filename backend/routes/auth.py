# backend/routes/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.db.helpers import get_user_by_name, get_connection

router = APIRouter(prefix="/auth", tags=["auth"])

class DevLoginModel(BaseModel):
    username: str
    phone: str | None = None
    gender: str | None = None
    language: str | None = "en-NG"

def onboard_user(username: str, phone=None, gender=None, language="en-NG") -> dict:
    """
    Onboard a user if they don't exist, otherwise return existing user.
    Uses live DB operations.
    """
    user = get_user_by_name(username)
    if user:
        return {
            "id": user[0],
            "name": user[1],
            "gender": user[2],
            "phone": user[3],
            "language": user[4],
        }

    # Create new user
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, gender, phone, preferred_language) VALUES (?, ?, ?, ?)",
        (username, gender, phone, language)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return {
        "id": user_id,
        "name": username,
        "gender": gender,
        "phone": phone,
        "language": language,
    }

@router.post("/dev-login")
def dev_login(payload: DevLoginModel):
    user = onboard_user(
        payload.username,
        phone=payload.phone,
        gender=payload.gender,
        language=payload.language
    )
    # Return simple token (demo). In production, replace with JWT
    token = f"demo-token:{user['id']}"
    return {"token": token, "user": user}
