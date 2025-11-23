# backend/db/crud_transactions.py
from .connection import get_db_conn

def record_transaction(tx_type: str, from_account: int, to_account: int, amount: int, currency: str = "NGN", status: str = "completed"):
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO transactions (tx_type, from_account, to_account, amount, currency, status) VALUES (?, ?, ?, ?, ?, ?)",
            (tx_type, from_account, to_account, amount, currency, status),
        )
        conn.commit()
        return cur.lastrowid

def atomic_transfer(from_account_id: int, to_account_id: int, amount: int):
    """Perform atomic debit/credit. Returns transaction id dict or raises on error."""
    with get_db_conn() as conn:
        cur = conn.cursor()
        try:
            conn.execute("BEGIN")
            # read balances
            cur.execute("SELECT balance FROM accounts WHERE id = ?", (from_account_id,))
            row_from = cur.fetchone()
            if not row_from:
                raise ValueError("From account not found")

            cur.execute("SELECT balance FROM accounts WHERE id = ?", (to_account_id,))
            row_to = cur.fetchone()
            if not row_to:
                raise ValueError("To account not found")

            if row_from["balance"] < amount:
                raise ValueError("Insufficient funds")

            new_from = row_from["balance"] - amount
            new_to = row_to["balance"] + amount

            cur.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_from, from_account_id))
            cur.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_to, to_account_id))

            # record transactions: debit and credit
            cur.execute(
                "INSERT INTO transactions (tx_type, from_account, to_account, amount, currency, status) VALUES (?, ?, ?, ?, ?, ?)",
                ("debit", from_account_id, to_account_id, amount, "NGN", "completed")
            )
            tx_id = cur.lastrowid

            conn.commit()
            return {"tx_id": tx_id, "from_balance": new_from, "to_balance": new_to}
        except Exception:
            conn.rollback()
            raise
