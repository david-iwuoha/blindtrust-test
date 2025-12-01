# backend/routes/user.py
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from backend.db.helpers import get_user_by_id, get_user_by_name, update_balance

router = APIRouter(prefix="/user", tags=["user"])

class UpdateProfileModel(BaseModel):
    phone: str | None = None
    gender: str | None = None
    username: str | None = None

class LanguageModel(BaseModel):
    language: str

def get_user_from_token(token: str | None):
    # demo token format: demo-token:<user_id>
    if not token:
        return None
    if token.startswith("demo-token:"):
        uid = int(token.split(":", 1)[1])
        user = get_user_by_id(uid)
        return user
    return None

@router.get("/me")
def me(authorization: str | None = Header(None)):
    user = get_user_from_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"user": user}

@router.post("/update")
def update(payload: UpdateProfileModel, authorization: str | None = Header(None)):
    user = get_user_from_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # --- Live DB updates ---
    conn = get_user_by_id(user[0])  # Fetch current state
    cursor = None
    from backend.db.helpers import get_connection
    with get_connection() as conn:
        cursor = conn.cursor()
        if payload.phone:
            cursor.execute("UPDATE users SET phone = ? WHERE id = ?", (payload.phone, user[0]))
        if payload.gender:
            cursor.execute("UPDATE users SET gender = ? WHERE id = ?", (payload.gender, user[0]))
        if payload.username:
            cursor.execute("UPDATE users SET name = ? WHERE id = ?", (payload.username, user[0]))
        conn.commit()

    updated_user = get_user_by_id(user[0])
    return {"user": updated_user}

@router.post("/language")
def set_language(payload: LanguageModel, authorization: str | None = Header(None)):
    user = get_user_from_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    from backend.db.helpers import get_connection
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET preferred_language = ? WHERE id = ?", (payload.language, user[0]))
        conn.commit()

    updated_user = get_user_by_id(user[0])
    return {"user": updated_user}
