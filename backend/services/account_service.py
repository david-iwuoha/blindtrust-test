# backend/services/account_service.py
from backend.db.crud_accounts import get_account_by_user_id

def get_balance_for_user(user_id: int):
    acc = get_account_by_user_id(user_id)
    if not acc:
        raise ValueError("Account not found")
    return acc["balance"]
