import csv
import os
from budget_repository import BudgetRepository
from database_manager import DatabaseManager


class BudgetManager:
    """
    Handles logic for the Budget App.

    Attributes:
        db_manager (DatabaseManager): Manages the database operations.
        repository (BudgetRepository): Handles operations for budget entries.
    """

    def __init__(self):
        """
        Initializes the BudgetManager with a database connection and repository.
        """
        self.db_manager = DatabaseManager()
        self.repository = BudgetRepository(self.db_manager.connection)

    def get_entries(self):
        """
        Retrieves all budget entries.

        Returns:
            list: A list of tuples representing budget entries, 
                  where each tuple contains (id, description, amount).
        """
        return self.repository.find_all()

    def add_entry(self, description, amount):
        """
        Adds a new budget entry.

        Args:
            description: The description of the budget entry.
            amount: The amount for the budget entry.
        """
        if not description or not amount:
            raise ValueError("Both fields must be filled.")
        try:
            amount = int(amount)
        except ValueError as e:
            raise ValueError("Amount must be a number.") from e
        self.repository.add_entry(description, amount)

    def delete_entry(self, entry_id):
        """
        Deletes a budget entry by its ID.

        Args:
            entry_id: The ID of the entry to be deleted.
        """
        self.repository.delete_entry(entry_id)

    def modify_entry(self, entry_id, description, amount):
        """
        Modifies an existing budget entry.

        Args:
            entry_id: The ID of the entry to be modified.
            description: The new description for the entry.
            amount: The new amount for the entry.
        """
        if not description or not amount:
            raise ValueError("Both fields must be filled.")
        try:
            amount = int(amount)
        except ValueError as e:
            raise ValueError("Amount must be a number.") from e
        self.repository.modify_entry(entry_id, description, amount)

    def populate_database(self):
        """
        Populates the database with initial data.
        """
        self.db_manager.create_initial_data()

    def reset_database(self):
        """
        Resets the database by clearing all data.
        """
        self.db_manager.initialize_database()

    def get_total_amount(self):
        """
        Calculates the total amount of all budget entries.

        Returns:
            int: The total amount of all entries.
        """
        entries = self.get_entries()
        return sum(entry[2] for entry in entries)

    def extract_id(self, text):
        """
        Extracts the ID from the selected text.

        Args:
            text: The selected text containing the entry ID.

        Returns:
            int: The extracted entry ID.
        """
        try:

            id_line = text.split("\n")[0]
            entry_id = id_line.split(":")[1].split("(")[0].strip()
            return int(entry_id)
        except (IndexError, ValueError) as e:
            raise ValueError("Unable to extract ID from the selected text.") from e

    def parse_entry(self, text):
        """
        Parses the description and amount from the selected text.

        Args:
            text: The selected text containing the entry information.

        Returns:
            tuple: A tuple containing (description, amount).
        """
        try:
            lines = text.split("\n")
            if len(lines) < 2:
                raise ValueError(
                    "Selected text does not contain valid entry information.")

            desc_amount = lines[1].split("|")
            description = desc_amount[0].replace("Desc:", "").strip()
            amount = desc_amount[1].replace("Amount:", "").strip()

            amount = int(amount)
            return description, amount
        except (IndexError, ValueError) as e:
            raise ValueError(
                "Unable to parse description and amount from the selected text.") from e

    def export_to_csv(self, file_path):
        """
        Exports all budget entries to a CSV file.

        Args:
            file_path: The file path to save the CSV file.
        """
        entries = self.get_entries()
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Description", "Amount"])
                writer.writerows(entries)
        except Exception as e:
            raise IOError(f"Error exporting data to CSV: {e}") from e

    def import_from_csv(self, file_path):
        """
        Imports budget entries from a CSV file.

        Args:
            file_path: The file path to read the CSV file.
        """
        if not os.path.exists(file_path):
            raise IOError(f"The file '{file_path}' does not exist.")

        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader) #skip first row
                for row in reader:
                    if len(row) != 3:
                        raise ValueError("CSV file has an invalid format.")
                    _, description, amount = row
                    self.add_entry(description, int(amount))
        except ValueError as e:
            raise ValueError(f"Error parsing CSV data: {e}") from e
        except Exception as e:
            raise IOError(f"Error importing data from CSV: {e}") from e
