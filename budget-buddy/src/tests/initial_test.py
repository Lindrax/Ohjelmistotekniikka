import unittest
import sqlite3
from budget_repository import BudgetRepository
from init_database import create_tables, create_initial

class TestBudgetRepository(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        create_tables(self.connection)
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
        create_initial(self.connection)
        entries = self.repository.find_all()
        self.assertEqual(len(entries), 4)

        descriptions = [entry[1] for entry in entries]
        amounts = [entry[2] for entry in entries]

        self.assertIn("Groceries", descriptions)
        self.assertIn("Salary", descriptions)
        self.assertIn(-50, amounts)
        self.assertIn(1500, amounts)

if __name__ == "__main__":
    unittest.main()