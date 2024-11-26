from tkinter import Tk, Label, Button, Entry, Text, END, messagebox
from budget_repository import BudgetRepository
from database_manager import DatabaseManager


class BudgetApp:
    """Main application."""

    def __init__(self, root):
        """Initialize the application."""
        self.db_manager = DatabaseManager()
        self.connection = self.db_manager.connection
        self.repository = BudgetRepository(self.connection)
        self.root = root
        self.root.title("Budget Buddy")

        self.create_ui()
        self.view_entries()

    def create_ui(self):
        """UI components."""
        Label(self.root, text="Budget Buddy", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        Label(self.root, text="Description:").grid(row=1, column=0, sticky="e", padx=5)
        self.entry_desc = Entry(self.root, width=30)
        self.entry_desc.grid(row=1, column=1, pady=5)

        Label(self.root, text="Amount:").grid(row=2, column=0, sticky="e", padx=5)
        self.entry_amount = Entry(self.root, width=30)
        self.entry_amount.grid(row=2, column=1, pady=5)

        Button(self.root, text="Add Entry", command=self.add_entry).grid(row=3, column=0, columnspan=2, pady=5)
        Button(self.root, text="View Entries", command=self.view_entries).grid(row=4, column=0, columnspan=2, pady=5)
        Button(self.root, text="Populate Database", command=self.populate_database).grid(row=6, column=0, columnspan=2, pady=5)
        Button(self.root, text="Reset Database", command=self.reset_database).grid(row=7, column=0, columnspan=2, pady=5)
        Button(self.root, text="Exit", command=self.root.quit).grid(row=8, column=0, columnspan=2, pady=10)

        self.total_label = Label(self.root, text="Total Amount: 0", font=("Arial", 12), fg="blue")
        self.total_label.grid(row=9, column=0, columnspan=2, pady=10)

        self.text_display = Text(self.root, width=50, height=15, wrap="word")
        self.text_display.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

    def view_entries(self):
        """Displays all budget entries."""
        entries = self.repository.find_all()
        self.text_display.delete(1.0, END)
        if not entries:
            self.text_display.insert(END, "No entries found.\n")
        else:
            for entry in entries:
                self.text_display.insert(END, f"Desc: {entry[1]}, Amount: {entry[2]}\n")
        self.update_total()

    def add_entry(self):
        """Adds a new budget entry."""
        description = self.entry_desc.get()
        amount = self.entry_amount.get()
        if not description or not amount:
            messagebox.showwarning("Input Error", "Both fields must be filled!")
            return
        try:
            amount = int(amount)
            self.repository.add_entry(description, amount)
            messagebox.showinfo("Success", "Entry added successfully!")
            self.entry_desc.delete(0, END)
            self.entry_amount.delete(0, END)
            self.view_entries()
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number.")

    def populate_database(self):
        """Populates the database with mock data."""
        self.db_manager.create_initial_data()
        messagebox.showinfo("Success", "Database populated with test data!")
        self.view_entries()

    def reset_database(self):
        """Resets the database."""
        self.db_manager.initialize_database()
        messagebox.showinfo("Success", "Database was reset!")
        self.view_entries()

    def update_total(self):
        """Calculates the total."""
        entries = self.repository.find_all()
        total = sum(entry[2] for entry in entries) if entries else 0
        self.total_label.config(text=f"Total Amount: {total}")


if __name__ == "__main__":
    window = Tk()
    app = BudgetApp(window)
    window.mainloop()
