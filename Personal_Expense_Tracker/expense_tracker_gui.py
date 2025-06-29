import json
import os
import csv
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from collections import defaultdict
from tkinter import filedialog
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

DATA_FILE = 'expenses.json'

# Load expenses from file
def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save expenses to file
def save_expenses(expenses):
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=4)

# Add a new expense
def add_expense():
    try:
        amount = float(amount_entry.get())
        category = category_entry.get()
        date = date_entry.get() or datetime.today().strftime('%Y-%m-%d')

        if not category:
            raise ValueError("Category required")

        expense = {"amount": amount, "category": category, "date": date}
        expenses.append(expense)
        save_expenses(expenses)
        update_table()
        amount_entry.delete(0, END)
        category_entry.delete(0, END)
        date_entry.delete(0, END)
        messagebox.showinfo("Success", "Expense added.")
    except ValueError:
        messagebox.showerror("Error", "Enter valid amount and category.")

# Update the Treeview table
def update_table():
    for item in expense_table.get_children():
        expense_table.delete(item)
    for idx, exp in enumerate(expenses):
        expense_table.insert('', 'end', iid=idx, values=(exp['amount'], exp['category'], exp['date']))

# Delete selected expense
def delete_expense():
    selected = expense_table.selection()
    if selected:
        for sel in selected:
            idx = int(sel)
            expenses.pop(idx)
        save_expenses(expenses)
        update_table()
        messagebox.showinfo("Deleted", "Selected expense(s) deleted.")
    else:
        messagebox.showwarning("Warning", "No item selected.")

# Show summary window
def show_summary():
    total = 0
    by_category = defaultdict(float)
    for exp in expenses:
        total += exp['amount']
        by_category[exp['category']] += exp['amount']

    summary_win = Toplevel(root)
    summary_win.title("Summary")
    summary_text = f"Total Spending: ${total:.2f}\n\n"
    for cat, amt in by_category.items():
        summary_text += f"{cat}: ${amt:.2f}\n"

    Label(summary_win, text=summary_text, font=('Arial', 12), justify=LEFT).pack(padx=10, pady=10)

# Visualize expenses
def visualize_expenses():
    by_category = defaultdict(float)
    for exp in expenses:
        by_category[exp['category']] += exp['amount']

    if not by_category:
        messagebox.showinfo("No Data", "No data to visualize.")
        return

    labels = list(by_category.keys())
    sizes = list(by_category.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    plt.title("Expenses by Category")
    plt.show()

# Download to CSV
def download_csv():
    if not expenses:
        messagebox.showinfo("No Data", "No expenses to download.")
        return
    try:
        file_path = filedialog.asksaveasfilename(
            title="Save CSV As",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="expense_report.csv"
        )
        if not file_path:
            return  # User cancelled
        with open(file_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["amount", "category", "date"])
            writer.writeheader()
            writer.writerows(expenses)
        messagebox.showinfo("Download Complete", f"Report saved as:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save CSV:\n{e}")


# ==== GUI ====
root = Tk()
root.title("Personal Expense Tracker")
root.geometry("800x500")
root.resizable(False, False)

# --- Form Inputs ---
frame_top = Frame(root)
frame_top.pack(pady=10)

Label(frame_top, text="Amount ($):").grid(row=0, column=0, padx=5)
amount_entry = Entry(frame_top, width=15)
amount_entry.grid(row=0, column=1, padx=5)

Label(frame_top, text="Category:").grid(row=0, column=2, padx=5)
category_entry = Entry(frame_top, width=15)
category_entry.grid(row=0, column=3, padx=5)

Label(frame_top, text="Date (YYYY-MM-DD):").grid(row=0, column=4, padx=5)
date_entry = Entry(frame_top, width=15)
date_entry.grid(row=0, column=5, padx=5)

# --- Buttons ---
frame_btn = Frame(root)
frame_btn.pack(pady=10)

Button(frame_btn, text="Add Expense", command=add_expense, bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5)
Button(frame_btn, text="Delete Selected", command=delete_expense, bg="#f44336", fg="white", width=15).grid(row=0, column=1, padx=5)
Button(frame_btn, text="View Summary", command=show_summary, bg="#2196F3", fg="white", width=15).grid(row=0, column=2, padx=5)
Button(frame_btn, text="Visualize", command=visualize_expenses, bg="#FF9800", fg="white", width=15).grid(row=0, column=3, padx=5)
Button(frame_btn, text="Download CSV", command=download_csv, bg="#673AB7", fg="white", width=15).grid(row=0, column=4, padx=5)

# --- Table ---
frame_table = Frame(root)
frame_table.pack(pady=10)

cols = ("Amount", "Category", "Date")
expense_table = ttk.Treeview(frame_table, columns=cols, show="headings", height=12)
for col in cols:
    expense_table.heading(col, text=col)
    expense_table.column(col, width=150, anchor=CENTER)
expense_table.pack()

# Load data and show table
expenses = load_expenses()
update_table()

root.mainloop()
