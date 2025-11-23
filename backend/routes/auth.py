# backend/routes/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.user_service import onboard_user
from backend.db.crud_users import get_user_by_username

router = APIRouter(prefix="/auth", tags=["auth"])

class DevLoginModel(BaseModel):
    username: str
    phone: str | None = None
    gender: str | None = None
    language: str | None = "en-NG"

@router.post("/dev-login")
def dev_login(payload: DevLoginModel):
    user = onboard_user(payload.username, phone=payload.phone, gender=payload.gender, language=payload.language)
    # return simple token (demo) - in production use JWT
    token = f"demo-token:{user['id']}"
    return {"token": token, "user": user}
