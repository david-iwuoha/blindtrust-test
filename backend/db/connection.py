# backend/db/connection.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "blindtrust_demo.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # returns rows as dict-like objects
    return conn

def init_db_from_schema(schema_file: str = "backend/db/schema.sql"):
    """Initialize the SQLite database from schema.sql"""
    conn = get_connection()
    with open(schema_file, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
