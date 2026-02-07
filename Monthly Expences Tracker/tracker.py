from db import get_connection
from utils import suggest_category


def add_expense(date, title, amount, category=None):
    if category is None or category.strip() == "":
        category = suggest_category(title)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO expenses (date, title, category, amount) VALUES (?, ?, ?, ?)",
        (date, title, category, float(amount)),
    )

    conn.commit()
    conn.close()
    return category


def list_expenses(limit=20):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, date, title, category, amount FROM expenses ORDER BY date DESC, id DESC LIMIT ?",
        (limit,),
    )

    rows = cur.fetchall()
    conn.close()
    return rows


def delete_expense(expense_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
