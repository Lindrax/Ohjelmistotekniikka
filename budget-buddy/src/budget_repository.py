from database_connection import get_database_connection

class BudgetRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        cursor = self._connection.cursor()

        cursor.execute("select * from entries")

        rows = cursor.fetchall()

        return [(row["id"], row["desc"], row["amount"]) for row in rows]
    
    def add_entry(self, desc, amount):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO entries (desc, amount) VALUES (?, ?)", (desc, amount))
        x = self._connection.commit()
        print(x)
              


user_repository = BudgetRepository(get_database_connection())
users = user_repository.find_all()