# backend/services/transfer_service.py
from backend.db.crud_accounts import get_account_by_user_id, get_account_by_id
from backend.db.crud_transactions import atomic_transfer
from backend.db.crud_beneficiaries import find_beneficiary_by_name
from backend.db.crud_users import get_user_by_username

def transfer_from_user_by_name(sender_user_id: int, beneficiary_name: str, amount: int):
    # find sender account
    sender_acc = get_account_by_user_id(sender_user_id)
    if not sender_acc:
        raise ValueError("Sender account not found")

    # find beneficiary under sender (demo)
    beneficiary = find_beneficiary_by_name(sender_user_id, beneficiary_name)
    if not beneficiary:
        # Maybe beneficiary is another demo user: find account by alias? for demo just create recipient account
        raise ValueError("Beneficiary not found")

    # For demo, the recipient account is looked up by alias or account_ref; here we map to a demo recipient account
    # We will treat beneficiary.account_ref as user username for demo recipient lookup
    # For simplicity, assume recipient has a user record named account_ref (demo)
    recipient_user_name = beneficiary.get("account_ref") or beneficiary.get("alias")
    # If using accounts table, we need account id — for demo create/find recipient account
    # Simpler approach: require that recipient is also demo user created during seeding. We'll assume accounts exist.
    # We'll try to find an account by user_id of recipient via crude lookup:
 
    

    recipient_user = get_user_by_username(recipient_user_name) if recipient_user_name else None
    if recipient_user:
        recipient_acc = get_account_by_user_id(recipient_user["id"])
        if not recipient_acc:
            raise ValueError("Recipient account not found")
        result = atomic_transfer(sender_acc["id"], recipient_acc["id"], amount)
        return result

    # fallback: if recipient is not a user, raise
    raise ValueError("Recipient user not found for demo transfer")
