# backend/services/transfer_service.py
from backend.db.helpers import get_account_by_user_id, get_user_by_name, transfer, get_beneficiaries

def transfer_from_user_by_name(sender_user_id: int, beneficiary_name: str, amount: int):
    # --- Step 1: Find sender account ---
    sender_acc = get_account_by_user_id(sender_user_id)
    if not sender_acc:
        raise ValueError("Sender account not found")

    # --- Step 2: Find beneficiary under sender ---
    all_beneficiaries = get_beneficiaries(sender_user_id)
    beneficiary_acc_id = None
    for ben_name, ben_acc_id in all_beneficiaries:
        if ben_name.lower() == beneficiary_name.lower():
            beneficiary_acc_id = ben_acc_id
            break

    if not beneficiary_acc_id:
        raise ValueError("Beneficiary not found")

    # --- Step 3: Perform transfer using live DB ---
    success, msg = transfer(sender_acc["id"], beneficiary_acc_id, amount)
    return {"success": success, "message": msg}
