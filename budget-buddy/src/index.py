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
        Label(self.root, text="Budget Buddy", font=("Arial", 16)).grid(
            row=0, column=0, columnspan=2, pady=10)

        Label(self.root, text="Description:").grid(
            row=1, column=0, sticky="e", padx=5)
        self.entry_desc = Entry(self.root, width=30)
        self.entry_desc.grid(row=1, column=1, pady=5)

        Label(self.root, text="Amount:").grid(
            row=2, column=0, sticky="e", padx=5)
        self.entry_amount = Entry(self.root, width=30)
        self.entry_amount.grid(row=2, column=1, pady=5)

        Button(self.root, text="Add Entry", command=self.add_entry).grid(
            row=3, column=0, columnspan=2, pady=5)
        Button(self.root, text="Delete Entry", command=self.delete_entry).grid(
            row=4, column=0, columnspan=2, pady=5)
        Button(self.root, text="Modify Entry", command=self.modify_entry).grid(
            row=5, column=0, columnspan=2, pady=5)
        Button(self.root, text="View Entries", command=self.view_entries).grid(
            row=6, column=0, columnspan=2, pady=5)
        Button(self.root, text="Populate Database", command=self.populate_database).grid(
            row=7, column=0, columnspan=2, pady=5)
        Button(self.root, text="Reset Database", command=self.reset_database).grid(
            row=8, column=0, columnspan=2, pady=5)
        Button(self.root, text="Exit", command=self.root.quit).grid(
            row=9, column=0, columnspan=2, pady=10)

        self.total_label = Label(
            self.root, text="Total Amount: 0", font=("Arial", 12), fg="blue")
        self.total_label.grid(row=10, column=0, columnspan=2, pady=10)

        self.text_display = Text(self.root, width=50, height=15, wrap="word")
        self.text_display.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

        self.text_display.bind("<ButtonRelease-1>", self.select_entry)

    def view_entries(self):
        """Displays all budget entries."""
        entries = self.repository.find_all()
        self.text_display.delete(1.0, END)
        if not entries:
            self.text_display.insert(END, "No entries found.\n")
        else:
            for entry in entries:
                self.text_display.insert(
                    END, f"ID: {entry[0]} (click here to select) \n Desc: {entry[1]} | Amount: {entry[2]}\n")

        self.update_total()

    def add_entry(self):
        """Adds a new entry."""
        description = self.entry_desc.get()
        amount = self.entry_amount.get()
        if not description or not amount:
            messagebox.showwarning(
                "Input Error", "Both fields must be filled!")
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

    def delete_entry(self):
        """Deletes the entry."""
        selected_text = self.text_display.get("sel.first", "sel.last")
        if not selected_text:
            messagebox.showwarning(
                "Selection Error", "Please select an entry to delete.")
            return

        entry_id = self.extract_id(selected_text)
        if entry_id:
            self.repository.delete_entry(entry_id)
            messagebox.showinfo("Success", "Entry deleted successfully!")
            self.view_entries()

    def modify_entry(self):
        """Modifies the entry."""
        selected_text = self.text_display.get("sel.first", "sel.last")
        if not selected_text:
            messagebox.showwarning(
                "Selection Error", "Please select an entry to modify.")
            return

        entry_id = self.extract_id(selected_text)
        if entry_id:
            new_description = self.entry_desc.get()
            new_amount = self.entry_amount.get()

            if not new_description or not new_amount:
                messagebox.showwarning(
                    "Input Error", "Fill in the fields before modifying!")
                return

            try:
                new_amount = int(new_amount)
                self.repository.modify_entry(
                    entry_id, new_description, new_amount)
                messagebox.showinfo("Success", "Entry modified successfully!")
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

    def extract_id(self, text):
        """Extracts the ID from the selected text."""
        try:
            id_line = text.split("\n")[0]
            entry_id = id_line.split(":")[1].split("(")[0].strip()
            return int(entry_id)
        except (IndexError, ValueError):
            messagebox.showerror("Error", "Unable to extract ID.")
            return None

    def select_entry(self, event):
        """Selects the clicked entry."""
        try:
            index = self.text_display.index(f"@{event.x},{event.y}")
            line_start = f"{index.split('.', maxsplit=1)[0]}.0"
            next_line = f"{int(index.split('.', maxsplit=1)[0]) + 1}.end"

            self.text_display.tag_remove("sel", "1.0", END)
            self.text_display.tag_add("sel", line_start, next_line)

            selected_text = self.text_display.get(
                line_start, next_line).strip()

            lines = selected_text.split("\n")
            if len(lines) == 2:
                desc_amount = lines[1].split("|")
                description = desc_amount[0].replace("Desc:", "").strip()
                amount = desc_amount[1].replace("Amount:", "").strip()

                self.entry_desc.delete(0, END)
                self.entry_desc.insert(0, description)
                self.entry_amount.delete(0, END)
                self.entry_amount.insert(0, amount)

        except Exception:
            messagebox.showerror(
                "Selection Error", "Could not select or parse entry.")


if __name__ == "__main__":
    window = Tk()
    app = BudgetApp(window)
    window.mainloop()
