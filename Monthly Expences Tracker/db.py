import sqlite3
import os

DB_FOLDER = "data"
DB_PATH = os.path.join(DB_FOLDER, "expenses.db")


def get_connection():
    os.makedirs(DB_FOLDER, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()
