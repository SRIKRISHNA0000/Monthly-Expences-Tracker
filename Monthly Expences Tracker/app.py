import streamlit as st
import pandas as pd
from datetime import datetime

from db import init_db, get_connection
from tracker import add_expense, delete_expense
from analytics import predict_month_end_spend


# ---------- Helpers ----------
def fetch_df():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM expenses ORDER BY date DESC, id DESC", conn)
    conn.close()

    if not df.empty:
        df["amount"] = df["amount"].astype(float)
    return df


def export_csv(df):
    return df.to_csv(index=False).encode("utf-8")


# ---------- Streamlit UI ----------
st.set_page_config(page_title="Smart Expense Tracker", page_icon="💰", layout="wide")

init_db()

st.title("💰 Smart Expense Tracker")
st.write("Track expenses • Auto-categorize • Predict month-end spend • Export reports")

# ---------- Sidebar ----------
st.sidebar.header("➕ Add Expense")

date = st.sidebar.date_input("Date", value=datetime.now())
title = st.sidebar.text_input("Title (Example: Swiggy 240)")
amount = st.sidebar.number_input("Amount", min_value=0.0, step=1.0)
category = st.sidebar.text_input("Category (Leave empty for auto)")

add_btn = st.sidebar.button("Add Expense ✅")

if add_btn:
    if title.strip() == "" or amount <= 0:
        st.sidebar.error("Please enter a valid title and amount.")
    else:
        final_cat = add_expense(date.strftime("%Y-%m-%d"), title, amount, category)
        st.sidebar.success(f"Added under category: {final_cat}")

st.sidebar.divider()

# ---------- Main content ----------
df = fetch_df()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", len(df))

with col2:
    total_spend = float(df["amount"].sum()) if not df.empty else 0
    st.metric("Total Spend", f"₹{round(total_spend, 2)}")

with col3:
    pred = predict_month_end_spend()
    if pred:
        month, spent, predicted = pred
        st.metric("Predicted Month-End", f"₹{predicted}")
    else:
        st.metric("Predicted Month-End", "No data")

st.divider()

# ---------- Recent Expenses ----------
st.subheader("📌 Recent Expenses")

if df.empty:
    st.info("No expenses added yet. Add one from the sidebar.")
else:
    st.dataframe(df, use_container_width=True)

st.divider()

# ---------- Delete Expense ----------
st.subheader("🗑️ Delete an Expense")
if df.empty:
    st.write("No records to delete.")
else:
    expense_id = st.number_input("Enter Expense ID to delete", min_value=1, step=1)
    if st.button("Delete"):
        delete_expense(expense_id)
        st.success("Deleted (if ID existed). Please refresh or re-run.")

st.divider()

# ---------- Charts ----------
st.subheader("📊 Charts")

if df.empty:
    st.write("Add expenses to view charts.")
else:
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("### Category Breakdown")
        cat_summary = (
            df.groupby("category")["amount"].sum().sort_values(ascending=False)
        )
        st.bar_chart(cat_summary)

    with chart_col2:
        st.write("### Daily Trend")
        df2 = df.copy()
        df2["date"] = pd.to_datetime(df2["date"])
        daily = df2.groupby(df2["date"].dt.date)["amount"].sum()
        st.line_chart(daily)

st.divider()

# ---------- Export ----------
st.subheader("📤 Export")

if df.empty:
    st.write("No data to export.")
else:
    st.download_button(
        label="Download CSV",
        data=export_csv(df),
        file_name="expenses_export.csv",
        mime="text/csv",
    )
