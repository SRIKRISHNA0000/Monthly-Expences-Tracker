from db import init_db, get_connection
from utils import today_date
from tracker import add_expense, list_expenses, delete_expense
from analytics import (
    monthly_summary,
    predict_month_end_spend,
    plot_category_pie,
    plot_daily_trend,
)
import os
import pandas as pd


def export_csv():
    os.makedirs("exports", exist_ok=True)
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()

    if df.empty:
        print("No expenses to export.")
        return

    file_path = os.path.join("exports", "expenses_export.csv")
    df.to_csv(file_path, index=False)
    print(f"Exported to: {file_path}")


def menu():
    print("\n==== SMART EXPENSE TRACKER ====")
    print("1) Add Expense")
    print("2) View Recent Expenses")
    print("3) Delete Expense")
    print("4) Monthly Summary")
    print("5) Predict Month-End Spend")
    print("6) Category Pie Chart")
    print("7) Daily Trend Chart")
    print("8) Export CSV")
    print("0) Exit")


def main():
    init_db()

    while True:
        menu()
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            date = input("Date (YYYY-MM-DD) [Enter for today]: ").strip()
            if not date:
                date = today_date()

            title = input("Title (example: Swiggy 240): ").strip()
            amount = input("Amount: ").strip()
            category = input("Category [Enter for auto]: ").strip()

            final_category = add_expense(date, title, amount, category)
            print(f"✅ Added expense under category: {final_category}")

        elif choice == "2":
            rows = list_expenses(30)
            if not rows:
                print("No expenses found.")
            else:
                print("\nID | Date | Title | Category | Amount")
                print("-" * 65)
                for r in rows:
                    print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | ₹{r[4]}")

        elif choice == "3":
            expense_id = input("Enter Expense ID to delete: ").strip()
            delete_expense(expense_id)
            print("🗑️ Deleted (if ID existed).")

        elif choice == "4":
            summary = monthly_summary()
            if summary is None:
                print("No data.")
            else:
                print("\nMonth | Total Spend")
                print("-" * 30)
                for m, total in summary.items():
                    print(f"{m} | ₹{round(total, 2)}")

        elif choice == "5":
            pred = predict_month_end_spend()
            if pred is None:
                print("No data.")
            else:
                month, spent, predicted = pred
                print(f"\n📌 Current Month: {month}")
                print(f"Spent till now: ₹{round(spent, 2)}")
                print(f"Predicted month-end spend: ₹{predicted}")

        elif choice == "6":
            month = input("Enter month (YYYY-MM) [Enter for all]: ").strip()
            plot_category_pie(month if month else None)

        elif choice == "7":
            month = input("Enter month (YYYY-MM) [Enter for all]: ").strip()
            plot_daily_trend(month if month else None)

        elif choice == "8":
            export_csv()

        elif choice == "0":
            print("Bye 👋")
            break

        else:
            print("❌ Invalid choice. Please enter 0-8 only.")


if __name__ == "__main__":
    main()
