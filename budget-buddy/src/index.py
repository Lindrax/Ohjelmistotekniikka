from database_connection import get_database_connection
from budget_repository import BudgetRepository
from init_database import create_initial

def menu():
    print("\n Budget Buddy ")
    print("1. View all entries")
    print("2. Add a new entry")
    print("3. Populate with test data")
    print("4. Exit")

def entries(repository):
    entries = repository.find_all()
    print("\n All Budget Entries")
    if not entries:
        print("No entries found.")
    else:
        for entry in entries:
            print(f"ID: {entry[0]}, Description: {entry[1]}, Amount: {entry[2]}")

def add_entry(repository):
    print("\n Add a New Entry ")
    desc = input("Enter description: ")
    try:
        amount = int(input("Enter amount: "))
        repository.add_entry(desc, amount)
        print("Entry added successfully!")
    except ValueError:
        print("Please enter a number.")

def populate():
    print("\n populating the database")
    connection = get_database_connection()
    create_initial(connection)

def main():
    connection = get_database_connection()

    repository = BudgetRepository(connection)

    while True:
        menu()
        choice = input("Choose an option: ")
        if choice == "1":
            entries(repository)
        elif choice == "2":
            add_entry(repository)
        elif choice =="3":
            populate()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
