# backend/routes/accounts.py
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from backend.services.account_service import get_balance_for_user
from backend.services.transfer_service import transfer_from_user_by_name

router = APIRouter(prefix="/accounts", tags=["accounts"])

class TransferModel(BaseModel):
    recipient: str
    amount: int

def get_user_from_token(token: str | None):
    if not token:
        return None
    if token.startswith("demo-token:"):
        uid = int(token.split(":", 1)[1])
        from backend.db.crud_users import get_user_by_id
        return get_user_by_id(uid)
    return None

@router.get("/balance")
def balance(authorization: str | None = Header(None)):
    user = get_user_from_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    bal = get_balance_for_user(user["id"])
    return {"balance": bal}

@router.post("/transfer")
def transfer(payload: TransferModel, authorization: str | None = Header(None)):
    user = get_user_from_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        result = transfer_from_user_by_name(user["id"], payload.recipient, payload.amount)
        return {"status": "ok", "result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
