# backend/services/beneficiary_service.py
from backend.db.helpers import add_beneficiary as db_add_beneficiary, get_beneficiaries

def add_beneficiary_for_user(user_id: int, beneficiary_name: str, beneficiary_account_id: int):
    """Add a beneficiary for a user."""
    return db_add_beneficiary(user_id, beneficiary_name, beneficiary_account_id)

def list_user_beneficiaries(user_id: int):
    """List all beneficiaries of a user."""
    return get_beneficiaries(user_id)

def find_beneficiary(user_id: int, name: str):
    """Find a specific beneficiary by name."""
    all_beneficiaries = get_beneficiaries(user_id)
    for ben_name, ben_acc_id in all_beneficiaries:
        if ben_name.lower() == name.lower():
            return {"name": ben_name, "account_id": ben_acc_id}
    return None
