import sqlite3
from datetime import date

class HabitDatabase:
    def __init__(self, name: str = "main.db"):
        self.db_name = name
        self.connection = sqlite3.connect(name)
        self.create_tables()

    def create_tables(self) -> None:
        """Create necessary tables if they don't exist."""
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS counter (
            name TEXT PRIMARY KEY,
            description TEXT)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS tracker (
            date TEXT,
            counterName TEXT,
            FOREIGN KEY(counterName) REFERENCES counter(name))""")

        self.connection.commit()

    def add_counter(self, name: str, description: str) -> None:
        """Add a counter to the database."""
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO counter VALUES (?, ?)", (name, description))
        self.connection.commit()

    def increment_counter(self, name: str, event_date: str = None) -> None:
        """Increment the counter in the database."""
        cursor = self.connection.cursor()
        if not event_date:
            event_date = date.today()
        cursor.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, name))
        self.connection.commit()

    def get_counter_data(self, name: str) -> list:
        """Get counter data from the database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tracker WHERE counterName=?", (name,))
        return cursor.fetchall()

    def get_habits(self):
        """Get the list of habits."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM counter")
        return [row[0] for row in cursor.fetchall()]
