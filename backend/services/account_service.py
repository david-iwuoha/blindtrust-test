# backend/services/account_service.py
from backend.db.helpers import get_account_by_user_id

def get_balance_for_user(user_id: int):
    acc = get_account_by_user_id(user_id)
    if not acc:
        raise ValueError("Account not found")
    return acc[2]  # balance is the 3rd column in accounts table (id, user_id, balance)
