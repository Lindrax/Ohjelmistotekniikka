from tkinter import Tk, Label, Button, Entry, Text, END, messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
from budget_manager import BudgetManager


class BudgetApp:
    """
    GUI for the Budget App.

    Attributes:
        root: The root Tkinter window for the application.
        manager: The BudgetManager instance for handling budget operations.
        entry_desc: Input field for the description of a budget entry.
        entry_amount: Input field for the amount of a budget entry.
        total_label: Label displaying the total amount of all budget entries.
        text_display: Text widget for displaying budget entries.
    """

    def __init__(self, root):
        """
        Initializes the GUI and connects it to the BudgetManager.

        Args:
            root: The root Tkinter window for the application.
        """
        self.root = root
        self.root.title("Budget Buddy")
        self.manager = BudgetManager()
        self.create_ui()
        self.view_entries()

    def create_ui(self):
        """
        Creates and initializes the UI components for the application.
        """
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
        Button(self.root, text="Export to CSV", command=self.export_to_csv).grid(
            row=12, column=0, columnspan=1, pady=5)
        Button(self.root, text="Import from CSV", command=self.import_from_csv).grid(
            row=12, column=1, columnspan=1, pady=5)

        self.total_label = Label(
            self.root, text="Total Amount: 0", font=("Arial", 12), fg="blue")
        self.total_label.grid(row=10, column=0, columnspan=2, pady=10)

        self.text_display = Text(self.root, width=50, height=15, wrap="word")
        self.text_display.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

        self.text_display.bind("<ButtonRelease-1>", self.select_entry)

    def view_entries(self):
        """
        Retrieves and displays all budget entries from the BudgetManager.
        """
        entries = self.manager.get_entries()
        self.text_display.delete(1.0, END)
        if not entries:
            self.text_display.insert(END, "No entries found.\n")
        else:
            for entry in entries:
                self.text_display.insert(
                    END, f"ID: {entry[0]} (click here to select)"
                        f"\n Desc: {entry[1]} | Amount: {entry[2]}\n")
        self.update_total()

    def add_entry(self):
        """
        Adds a new budget entry.
        """
        description = self.entry_desc.get()
        amount = self.entry_amount.get()
        try:
            self.manager.add_entry(description, amount)
            self.entry_desc.delete(0, END)
            self.entry_amount.delete(0, END)
            self.view_entries()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_entry(self):
        """
        Deletes the selected budget entry.
        """
        selected_text = self.text_display.get("sel.first", "sel.last")
        entry_id = self.manager.extract_id(selected_text)
        if entry_id:
            self.manager.delete_entry(entry_id)
            self.view_entries()

    def modify_entry(self):
        """
        Modifies the selected budget entry.
        """
        selected_text = self.text_display.get("sel.first", "sel.last")
        entry_id = self.manager.extract_id(selected_text)
        description = self.entry_desc.get()
        amount = self.entry_amount.get()
        if entry_id:
            try:
                self.manager.modify_entry(entry_id, description, amount)
                self.view_entries()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def populate_database(self):
        """
        Populates the database with default entries.
        """
        self.manager.populate_database()
        self.view_entries()

    def reset_database(self):
        """
        Resets the database by clearing all entries.
        """
        self.manager.reset_database()
        self.view_entries()

    def update_total(self):
        """
        Updates the total amount displayed in the application.
        """
        total = self.manager.get_total_amount()
        self.total_label.config(text=f"Total Amount: {total}")

    def select_entry(self, event):
        """
        Selects a budget entry from the display.

        Args:
            event: The mouse event triggered by the user's selection.
        """
        try:
            index = self.text_display.index(f"@{event.x},{event.y}")
            line_start = f"{index.split('.', maxsplit=1)[0]}.0"
            next_line = f"{int(index.split('.', maxsplit=1)[0]) + 1}.end"

            self.text_display.tag_remove("sel", "1.0", END)
            self.text_display.tag_add("sel", line_start, next_line)

            selected_text = self.text_display.get(
                line_start, next_line).strip()
            description, amount = self.manager.parse_entry(selected_text)

            self.entry_desc.delete(0, END)
            self.entry_desc.insert(0, description)
            self.entry_amount.delete(0, END)
            self.entry_amount.insert(0, amount)
        except ValueError as e:
            messagebox.showerror(
                "Selection Error", f"Could not parse entry: {e}")

    def export_to_csv(self):
        """
        Exports budget entries to a CSV file.
        """
        file_path = asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Export Budget Data")
        if file_path:
            try:
                self.manager.export_to_csv(file_path)
                messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    def import_from_csv(self):
        """
        Imports budget entries from a CSV file.
        """
        file_path = askopenfilename(
            filetypes=[("CSV", "*.csv")],
            title="Import Budget Data")
        if file_path:
            try:
                self.manager.import_from_csv(file_path)
                self.view_entries()
                messagebox.showinfo("Import Successful", f"Data imported from {file_path}")
            except Exception as e:
                messagebox.showerror("Import Error", str(e))


if __name__ == "__main__":
    window = Tk()
    app = BudgetApp(window)
    window.mainloop()
