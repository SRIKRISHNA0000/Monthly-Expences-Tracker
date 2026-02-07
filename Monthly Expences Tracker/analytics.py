import pandas as pd
import matplotlib.pyplot as plt
from db import get_connection


def fetch_dataframe():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()

    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = df["amount"].astype(float)
    return df


def monthly_summary():
    df = fetch_dataframe()
    if df.empty:
        return None

    df["month"] = df["date"].dt.to_period("M").astype(str)
    summary = df.groupby("month")["amount"].sum().sort_index()
    return summary


def category_summary(month=None):
    df = fetch_dataframe()
    if df.empty:
        return None

    if month:
        df["month"] = df["date"].dt.to_period("M").astype(str)
        df = df[df["month"] == month]

    summary = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    return summary


def predict_month_end_spend():
    df = fetch_dataframe()
    if df.empty:
        return None

    df["month"] = df["date"].dt.to_period("M").astype(str)
    current_month = df["month"].max()

    month_df = df[df["month"] == current_month]
    if month_df.empty:
        return None

    month_df["day"] = month_df["date"].dt.day

    total_spent = month_df["amount"].sum()
    days_passed = month_df["day"].max()

    # simple trend predictor
    avg_per_day = total_spent / max(days_passed, 1)
    predicted = avg_per_day * 30

    return current_month, total_spent, round(predicted, 2)


def plot_category_pie(month=None):
    summary = category_summary(month)
    if summary is None or summary.empty:
        print("No data to plot.")
        return

    summary.plot(kind="pie", autopct="%1.1f%%")
    plt.ylabel("")
    plt.title("Expense Breakdown by Category")
    plt.tight_layout()
    plt.show()


def plot_daily_trend(month=None):
    df = fetch_dataframe()
    if df.empty:
        print("No data to plot.")
        return

    df["month"] = df["date"].dt.to_period("M").astype(str)
    if month:
        df = df[df["month"] == month]

    if df.empty:
        print("No data for that month.")
        return

    daily = df.groupby(df["date"].dt.date)["amount"].sum()
    daily.plot(kind="line", marker="o")
    plt.title("Daily Expense Trend")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.show()
