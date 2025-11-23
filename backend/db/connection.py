# backend/db/connection.py
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "blindtrust.db"

def init_db_from_schema():
    schema_file = Path(__file__).resolve().parent / "schema.sql"
    if schema_file.exists():
        conn = sqlite3.connect(DB_PATH)
        with conn:
            conn.executescript(schema_file.read_text())
        conn.close()

def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

@contextmanager
def get_db_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = dict_factory
    try:
        yield conn
    finally:
        conn.close()
