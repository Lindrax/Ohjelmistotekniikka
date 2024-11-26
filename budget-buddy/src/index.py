from tkinter import Tk, Label, Button, Entry, Text, END, messagebox
from database_connection import get_database_connection
from budget_repository import BudgetRepository
from init_database import create_initial, initialize_database


connection = get_database_connection()
repository = BudgetRepository(connection)


def view_entries():
    """Displays all budget entries."""
    entries = repository.find_all()
    text_display.delete(1.0, END)
    if not entries:
        text_display.insert(END, "No entries found.\n")
    else:
        for entry in entries:
            text_display.insert(END, f"Desc: {entry[1]}, Amount: {entry[2]}\n")
    update_total()


def add_entry():
    """Adds a new budget entry."""
    description = entry_desc.get()
    amount = entry_amount.get()
    if not description or not amount:
        messagebox.showwarning("Input Error", "Both fields must be filled!")
        return
    try:
        amount = int(amount)
        repository.add_entry(description, amount)
        messagebox.showinfo("Success", "Entry added successfully!")
        entry_desc.delete(0, END)
        entry_amount.delete(0, END)
        view_entries()
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number.")


def populate_database():
    """Populates the database with mock data."""
    create_initial(connection)
    messagebox.showinfo("Success", "Database populated with test data!")
    view_entries()

def reset_database():
    """Resets the database"""
    initialize_database()
    messagebox.showinfo("Success", "Database was reset!")
    view_entries()


def update_total():
    """Calculates the total."""
    entries = repository.find_all()
    total = sum(entry[2] for entry in entries) if entries else 0
    total_label.config(text=f"Total Amount: {total}")


window = Tk()
window.title("Budget Buddy")


Label(window, text="Budget Buddy", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

Label(window, text="Description:").grid(row=1, column=0, sticky="e", padx=5)
entry_desc = Entry(window, width=30)
entry_desc.grid(row=1, column=1, pady=5)

Label(window, text="Amount:").grid(row=2, column=0, sticky="e", padx=5)
entry_amount = Entry(window, width=30)
entry_amount.grid(row=2, column=1, pady=5)

Button(window, text="Add Entry", command=add_entry).grid(row=3, column=0, columnspan=2, pady=5)

Button(window, text="View Entries", command=view_entries).grid(row=4, column=0, columnspan=2, pady=5)

Button(window, text="Populate Database", command=populate_database).grid(row=6, column=0, columnspan=2, pady=5)

Button(window, text="Reset Database", command=reset_database).grid(row=7, column=0, columnspan=2, pady=5)

Button(window, text="Exit", command=window.quit).grid(row=8, column=0, columnspan=2, pady=10)

total_label = Label(window, text="Total Amount: 0", font=("Arial", 12), fg="blue")
total_label.grid(row=9, column=0, columnspan=2, pady=10)

text_display = Text(window, width=50, height=15, wrap="word")
text_display.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

window.mainloop()
