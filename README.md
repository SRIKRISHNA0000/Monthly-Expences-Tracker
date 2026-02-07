# Monthly-Expences-Tracker

Smart Expense Tracker (Python + SQLite + Streamlit)

A Smart Expense Tracker built using Python and SQLite, with a clean Streamlit web app UI.
It helps users track daily expenses, auto-suggest categories, visualize spending, predict month-end spend, and export reports.

🚀 Features

✅ Add expenses (date, title, amount, category)
✅ Auto category suggestion (Food, Travel, Bills, Shopping, etc.)
✅ View recent expenses in a clean table
✅ Delete expenses by ID
✅ Total spend & record count
✅ Month-end spending prediction
✅ Category breakdown chart
✅ Daily trend chart
✅ Export expenses to CSV

🛠️ Tech Stack

Python

SQLite (Database)

Streamlit (Web UI)

Pandas (Data analysis)

Matplotlib (Charts)

📂 Project Structure
smart-expense-tracker/
│── app.py              # Streamlit web app (UI version)
│── main.py             # Terminal version (CLI)
│── db.py               # SQLite database setup
│── tracker.py          # Add/View/Delete expense logic
│── analytics.py        # Summary + prediction + charts
│── utils.py            # Auto category suggestion
│── requirements.txt
│── README.md
│── data/
│── exports/
