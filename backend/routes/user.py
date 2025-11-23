# backend/routes/user.py
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from backend.db.crud_users import get_user_by_id, update_profile, update_user_language

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
        return get_user_by_id(uid)
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
    updated = update_profile(user["id"], phone=payload.phone, gender=payload.gender, username=payload.username)
    return {"user": updated}

@router.post("/language")
def set_language(payload: LanguageModel, authorization: str | None = Header(None)):
    user = get_user_from_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    updated = update_user_language(user["id"], payload.language)
    return {"user": updated}
