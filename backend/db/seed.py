# backend/db/seed.py
from .helpers import get_connection, add_beneficiary, get_user_by_name

def init_db_from_schema():
    """Initialize DB from schema.sql"""
    import os
    schema_file = "backend/db/schema.sql"
    if not os.path.exists("backend/db/blindtrust_demo.db"):
        conn = get_connection()
        with open(schema_file, "r") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

# --- Demo user creation ---
def create_user(name, gender, phone, language="english"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, gender, phone, preferred_language) VALUES (?, ?, ?, ?)",
        (name, gender, phone, language)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def create_account_for_user(name):
    user = get_user_by_name(name)
    if not user:
        raise ValueError(f"User {name} not found")
    user_id = user[0]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (user_id, balance) VALUES (?, ?)", (user_id, 10000))
    conn.commit()
    account_id = cursor.lastrowid
    conn.close()
    return account_id

def seed_demo():
    """Seed demo users, accounts, and beneficiaries"""
    # Initialize DB
    init_db_from_schema()

    # Users
    alice_id = create_user("Alice", "female", "08011111111", "english")
    john_id = create_user("John", "male", "08022222222", "english")

    # Accounts
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (user_id, balance) VALUES (?, ?)", (alice_id, 10000))
    alice_acc_id = cursor.lastrowid
    cursor.execute("INSERT INTO accounts (user_id, balance) VALUES (?, ?)", (john_id, 10000))
    john_acc_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Beneficiaries
    add_beneficiary(alice_id, "John", john_acc_id)
    add_beneficiary(john_id, "Alice", alice_acc_id)
