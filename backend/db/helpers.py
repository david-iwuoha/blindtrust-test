import sqlite3
from contextlib import closing

DB_PATH = "backend/db/blindtrust_demo.db"

# --- Basic connection helper ---
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # allow dict-like row access
    return conn

# --- User queries ---
def get_user_by_name(name: str):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        return cursor.fetchone()

def get_user_by_id(user_id: int):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

# --- Account queries ---
def get_account_by_user_id(user_id: int):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,))
        return cursor.fetchone()

def update_balance(account_id: int, amount: float):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, account_id)
        )
        conn.commit()

def get_balance(account_id: int):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()
        return row["balance"] if row else None

# --- Beneficiaries ---
def add_beneficiary(user_id: int, beneficiary_name: str, beneficiary_account_id: int):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO beneficiaries (user_id, beneficiary_name, beneficiary_account_id) VALUES (?, ?, ?)",
            (user_id, beneficiary_name, beneficiary_account_id)
        )
        conn.commit()

def get_beneficiaries(user_id: int):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT beneficiary_name, beneficiary_account_id FROM beneficiaries WHERE user_id = ?",
            (user_id,)
        )
        return cursor.fetchall()

# --- Transactions ---
def log_transaction(from_account_id: int, to_account_id: int, amount: float, status: str):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (from_account_id, to_account_id, amount, status) VALUES (?, ?, ?, ?)",
            (from_account_id, to_account_id, amount, status)
        )
        conn.commit()

# --- Transfer helper ---
def transfer(from_account_id: int, to_account_id: int, amount: float):
    # reject invalid amounts
    if amount <= 0:
        return False, "Invalid transfer amount"

    with closing(get_connection()) as conn:
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT balance FROM accounts WHERE id = ?", (from_account_id,))
            row = cursor.fetchone()

            if not row:
                return False, "Source account not found"

            from_balance = row["balance"]

            if from_balance < amount:
                return False, f"Insufficient funds. Balance = {from_balance}"

            cursor.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                (amount, from_account_id)
            )
            cursor.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (amount, to_account_id)
            )
            cursor.execute(
                "INSERT INTO transactions (from_account_id, to_account_id, amount, status) VALUES (?, ?, ?, ?)",
                (from_account_id, to_account_id, amount, "success")
            )

            conn.commit()
            return True, "Transfer successful"

        except Exception as e:
            conn.rollback()
            return False, str(e)
