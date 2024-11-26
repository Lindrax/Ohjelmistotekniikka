from database_connection import get_database_connection


class DatabaseManager:
    """Database operations"""

    def __init__(self, connection=None):
        """Get connection"""
        self.connection = self.connection = connection if connection else get_database_connection()

    def drop_tables(self):
        """Drop tables"""
        print("Dropping tables...")
        cursor = self.connection.cursor()
        cursor.execute('''
            DROP TABLE IF EXISTS entries;
        ''')
        self.connection.commit()

    def create_tables(self):
        """Create tables"""
        print("Creating tables...")
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                desc TEXT,
                amount INT
            );
        ''')
        self.connection.commit()

    def create_initial_data(self):
        """Populate the database with mock data."""
        print("Initializing data...")
        cursor = self.connection.cursor()
        test_data = [
            ("Groceries", -50),
            ("Salary", 1500),
            ("Rent", -700),
            ("Coffee", -3),
        ]
        cursor.executemany('''
            INSERT INTO entries (desc, amount) VALUES (?, ?);
        ''', test_data)
        self.connection.commit()

    def initialize_database(self):
        """Reset the database"""
        print("Initializing database...")
        self.drop_tables()
        self.create_tables()


if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.initialize_database()
