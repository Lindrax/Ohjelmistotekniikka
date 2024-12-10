import unittest
import os
import csv
import sqlite3
from budget_manager import BudgetManager
from budget_repository import BudgetRepository
from database_manager import DatabaseManager

class TestBudgetManager(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.db_manager = DatabaseManager(self.connection)
        self.db_manager.initialize_database()
        self.repository = BudgetRepository(self.connection)
        self.manager = BudgetManager()
        self.manager.db_manager = self.db_manager
        self.manager.repository = self.repository

    def test_get_entries(self):
        self.repository.add_entry("Test", 100)
        entries = self.manager.get_entries()
        self.assertEqual(entries, [(1, "Test", 100)])

    def test_add_entry_valid(self):
        self.manager.add_entry("Test", 100)
        entries = self.manager.get_entries()
        self.assertEqual(entries, [(1, "Test", 100)])

    def test_add_entry_invalid(self):
        with self.assertRaises(ValueError):
            self.manager.add_entry("", 100)
        with self.assertRaises(ValueError):
            self.manager.add_entry("Test", "invalid")

    def test_delete_entry(self):
        self.repository.add_entry("Test", 100)
        entry_id = self.manager.get_entries()[0][0]
        self.manager.delete_entry(entry_id)
        entries = self.manager.get_entries()
        self.assertEqual(entries, [])

    def test_modify_entry_valid(self):
        self.repository.add_entry("Test", 100)
        entry_id = self.manager.get_entries()[0][0]
        self.manager.modify_entry(entry_id, "Updated Test", 200)
        entries = self.manager.get_entries()
        self.assertEqual(entries, [(1, "Updated Test", 200)])

    def test_modify_entry_invalid(self):
        self.repository.add_entry("Test", 100)
        entry_id = self.manager.get_entries()[0][0]
        with self.assertRaises(ValueError):
            self.manager.modify_entry(entry_id, "", 200)
        with self.assertRaises(ValueError):
            self.manager.modify_entry(entry_id, "Test", "invalid")

    def test_get_total_amount(self):
        self.repository.add_entry("Test1", 100)
        self.repository.add_entry("Test2", -50)
        total = self.manager.get_total_amount()
        self.assertEqual(total, 50)

    def test_extract_id_valid(self):
        text = "ID: 1\nDesc: Test | Amount: 100"
        entry_id = self.manager.extract_id(text)
        self.assertEqual(entry_id, 1)

    def test_extract_id_invalid(self):
        with self.assertRaises(ValueError):
            self.manager.extract_id("Invalid text")

    def test_parse_entry_valid(self):
        text = "ID: 1\nDesc: Test | Amount: 100"
        description, amount = self.manager.parse_entry(text)
        self.assertEqual(description, "Test")
        self.assertEqual(amount, 100)

    def test_parse_entry_invalid(self):
        with self.assertRaises(ValueError):
            self.manager.parse_entry("Invalid text")

    def test_import_from_csv_valid(self):
        with open("dummy.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Description", "Amount"])
            writer.writerow([1, "Test", 100])

        self.manager.import_from_csv("dummy.csv")
        entries = self.manager.get_entries()
        self.assertEqual(entries, [(1, "Test", 100)])

        os.remove("dummy.csv")

    def test_import_from_csv_invalid_format(self):
        with open("dummy.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Description", "Amount"])  # Valid header
            file.write("Invalid data")  # Invalid row

        with self.assertRaises(ValueError):
            self.manager.import_from_csv("dummy.csv")

        os.remove("dummy.csv")


    def test_import_from_csv_file_not_found(self):
        with self.assertRaises(IOError):
            self.manager.import_from_csv("nonexistent.csv")

    def test_export_to_csv(self):
        self.repository.add_entry("Test", 100)
        self.manager.export_to_csv("dummy.csv")

        with open("dummy.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)

        self.assertEqual(rows[0], ["ID", "Description", "Amount"])
        self.assertEqual(rows[1], ["1", "Test", "100"])

        os.remove("dummy.csv")

if __name__ == "__main__":
    unittest.main()
