# backend/routes/beneficiaries.py
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from backend.services.beneficiary_service import add_beneficiary_for_user, list_user_beneficiaries

router = APIRouter(prefix="/beneficiaries", tags=["beneficiaries"])

class AddBeneficiaryModel(BaseModel):
    name: str
    alias: str | None = None
    account_ref: str | None = None

def get_user_from_token(token: str | None):
    if not token:
        return None
    if token.startswith("demo-token:"):
        uid = int(token.split(":", 1)[1])
        from backend.db.crud_users import get_user_by_id
        return get_user_by_id(uid)
    return None

@router.post("/add")
def add_beneficiary(payload: AddBeneficiaryModel, authorization: str | None = Header(None)):
    user = get_user_from_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    record = add_beneficiary_for_user(user["id"], payload.name, payload.alias, payload.account_ref)
    return {"beneficiary": record}

@router.get("/list")
def list_beneficiaries_route(authorization: str | None = Header(None)):
    user = get_user_from_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    items = list_user_beneficiaries(user["id"])
    return {"beneficiaries": items}
