from database_connection import get_database_connection


class BudgetRepository:
    """Class responsible for managing budget entries in the database.

    Attributes:
        _connection: Database connection object.
    """

    def __init__(self, connection):
        """Initializes the BudgetRepository with a database connection.

        Args:
            connection: The database connection.
        """
        self._connection = connection

    def find_all(self):
        """Retrieves all budget entries from the database.

        Returns:
            A list of tuples where each tuple contains the ID, description, and amount of an entry.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM entries")
        rows = cursor.fetchall()
        return [(row["id"], row["desc"], row["amount"]) for row in rows]

    def add_entry(self, desc, amount):
        """Adds a new budget entry to the database.

        Args:
            desc: The description of the entry.
            amount: The amount for the entry.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO entries (desc, amount) VALUES (?, ?)", (desc, amount))
        self._connection.commit()

    def delete_entry(self, entry_id):
        """Deletes a budget entry from the database.

        Args:
            entry_id: The ID of the entry to delete.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "DELETE FROM entries WHERE id = ?", (entry_id,))
        self._connection.commit()

    def modify_entry(self, entry_id, desc, amount):
        """Modifies an existing budget entry in the database.

        Args:
            entry_id: The ID of the entry to modify.
            desc: The new description of the entry.
            amount: The new amount for the entry.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "UPDATE entries SET desc = ?, amount = ? WHERE id = ?", (desc, amount, entry_id))
        self._connection.commit()


user_repository = BudgetRepository(get_database_connection())
users = user_repository.find_all()
