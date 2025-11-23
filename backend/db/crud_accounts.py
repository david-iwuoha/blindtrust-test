# backend/db/crud_accounts.py
from .connection import get_db_conn

def get_account_by_user_id(user_id: int):
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,))
        return cur.fetchone()

def get_account_by_id(account_id: int):
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        return cur.fetchone()

def get_balance(user_id: int):
    acc = get_account_by_user_id(user_id)
    return acc["balance"] if acc else None

def update_balance(account_id: int, new_balance: int):
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
        conn.commit()
        return get_account_by_id(account_id)
