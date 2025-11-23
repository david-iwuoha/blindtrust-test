# backend/db/crud_beneficiaries.py
from .connection import get_db_conn

def add_beneficiary(user_id: int, name: str, alias: str = None, account_ref: str = None):
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO beneficiaries (user_id, name, alias, account_ref) VALUES (?, ?, ?, ?)",
            (user_id, name, alias, account_ref),
        )
        conn.commit()
        return get_beneficiary_by_id(cur.lastrowid)

def get_beneficiary_by_id(bid: int):
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM beneficiaries WHERE id = ?", (bid,))
        return cur.fetchone()

def list_beneficiaries(user_id: int):
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM beneficiaries WHERE user_id = ?", (user_id,))
        return cur.fetchall()

def find_beneficiary_by_name(user_id: int, name: str):
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM beneficiaries WHERE user_id = ? AND lower(name) = ?", (user_id, name.lower()))
        return cur.fetchone()
