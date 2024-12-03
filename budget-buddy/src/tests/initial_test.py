import unittest
import sqlite3
from budget_repository import BudgetRepository
from database_manager import DatabaseManager


class TestBudgetRepository(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.db_manager = DatabaseManager(self.connection)
        self.db_manager.initialize_database()
        self.repository = BudgetRepository(self.connection)

    def test_database_empty(self):
        entries = self.repository.find_all()
        self.assertEqual(entries, [])

    def test_add_entry(self):
        self.repository.add_entry("Test", 100)
        entries = self.repository.find_all()

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0][1], "Test")
        self.assertEqual(entries[0][2], 100)

    def test_initial(self):
        self.db_manager.create_initial_data()
        entries = self.repository.find_all()
        self.assertEqual(len(entries), 4)

        descriptions = [entry[1] for entry in entries]
        amounts = [entry[2] for entry in entries]

        self.assertIn("Groceries", descriptions)
        self.assertIn("Salary", descriptions)
        self.assertIn(-50, amounts)
        self.assertIn(1500, amounts)

    def test_modify_entry(self):
        self.repository.add_entry("Test", 100)
        entry = self.repository.find_all()[0]
        self.repository.modify_entry(entry[0], "Updated Test", 200)

        updated_entry = self.repository.find_all()[0]
        self.assertEqual(updated_entry[1], "Updated Test")
        self.assertEqual(updated_entry[2], 200)

    def test_delete_entry(self):
        self.repository.add_entry("Test", 100)
        entry = self.repository.find_all()[0]
        self.repository.delete_entry(entry[0])

        entries = self.repository.find_all()
        self.assertEqual(len(entries), 0)


if __name__ == "__main__":
    unittest.main()
