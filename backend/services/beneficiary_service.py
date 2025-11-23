# backend/services/beneficiary_service.py
from backend.db.crud_beneficiaries import add_beneficiary, list_beneficiaries, find_beneficiary_by_name

def add_beneficiary_for_user(user_id: int, name: str, alias: str = None, account_ref: str = None):
    return add_beneficiary(user_id, name, alias, account_ref)

def list_user_beneficiaries(user_id: int):
    return list_beneficiaries(user_id)

def find_beneficiary(user_id: int, name: str):
    return find_beneficiary_by_name(user_id, name)
