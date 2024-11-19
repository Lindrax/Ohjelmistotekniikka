from database_connection import get_database_connection


def drop_tables(connection):
    print("dropping tables")
    cursor = connection.cursor()
    cursor.execute('''
        drop table if exists entries;
    ''')
    connection.commit()


def create_tables(connection):
    print("creating tables")
    cursor = connection.cursor()
    cursor.execute('''
        create table entries (
            id INTEGER primary key AUTOINCREMENT,
            desc TEXT,
            amount INT
        );
    ''')

    connection.commit()

def create_initial(connection):
    print("initialising data")
    cursor = connection.cursor()

    test_data = [
        ( "Groceries", -50),
        ( "Salary", 1500),
        ( "Rent", -700),
        ( "Coffee", -3),
    ]

    cursor.executemany('''
        insert into entries ( desc, amount) values ( ?, ?);
    ''', test_data)

    connection.commit()


def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()