"""connection"""
from database_connection import get_database_connection


class BudgetRepository:
    """Budget Repository"""

    def __init__(self, connection):
        """init"""
        self._connection = connection

    def find_all(self):
        """find all"""
        cursor = self._connection.cursor()

        cursor.execute("select * from entries")

        rows = cursor.fetchall()

        return [(row["id"], row["desc"], row["amount"]) for row in rows]

    def add_entry(self, desc, amount):
        """add entry"""
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO entries (desc, amount) VALUES (?, ?)", (desc, amount))
        x = self._connection.commit()
        print(x)

    def delete_entry(self, entry_id):
        """"delete entry"""
        print(id)
        cursor = self._connection.cursor()
        cursor.execute(
            "DELETE FROM entries WHERE id = ?", (entry_id,))
        self._connection.commit()

    def modify_entry(self, entry_id, desc, amount):
        """"modify entry"""
        cursor = self._connection.cursor()
        cursor.execute(
            "UPDATE entries SET desc = ?, amount = ? WHERE id = ?", (desc, amount, entry_id))
        self._connection.commit()


user_repository = BudgetRepository(get_database_connection())
users = user_repository.find_all()
