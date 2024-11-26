```mermaid
classDiagram
    direction TB

    class BudgetApp {
    }

    class DatabaseManager {
    }

    class BudgetRepository {
    }

    class DatabaseConnection {
    }

    BudgetApp --> DatabaseManager
    BudgetApp --> BudgetRepository
    DatabaseManager --> DatabaseConnection
    BudgetRepository --> DatabaseConnection

```
