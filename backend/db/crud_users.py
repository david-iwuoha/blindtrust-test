# backend/db/crud_users.py
from .connection import get_db_conn

def create_user(username: str, phone: str = None, gender: str = None, language: str = "en-NG"):
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, phone, gender, language) VALUES (?, ?, ?, ?)",
            (username, phone, gender, language),
        )
        user_id = cur.lastrowid
        # create account with initial balance 10000 (demo)
        cur.execute("INSERT INTO accounts (user_id, balance) VALUES (?, ?)", (user_id, 10000))
        conn.commit()
        return get_user_by_id(user_id)

def get_user_by_id(user_id: int):
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cur.fetchone()

def get_user_by_username(username: str):
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cur.fetchone()

def update_user_language(user_id: int, language: str):
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET language = ? WHERE id = ?", (language, user_id))
        conn.commit()
        return get_user_by_id(user_id)

def update_profile(user_id: int, phone: str = None, gender: str = None, username: str = None):
    with get_db_conn() as conn:
        cur = conn.cursor()
        if phone:
            cur.execute("UPDATE users SET phone = ? WHERE id = ?", (phone, user_id))
        if gender:
            cur.execute("UPDATE users SET gender = ? WHERE id = ?", (gender, user_id))
        if username:
            cur.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
        conn.commit()
        return get_user_by_id(user_id)
