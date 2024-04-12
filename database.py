import sqlite3
from datetime import datetime, timedelta
from habit import Habit

class HabitDatabase:
    """Handles interactions with the SQLite database for habit tracking."""

    def __init__(self, name: str = "main.db"):
        """Initialize the database connection and create necessary tables if they don't exist."""
        self.db_name = name
        self.connection = sqlite3.connect(name)
        self.create_tables()

    def create_tables(self) -> None:
        """Create necessary tables if they don't exist."""
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS counter (
            name TEXT PRIMARY KEY,
            description TEXT UNIQUE)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS tracker (
            date TEXT,
            counterName TEXT,
            FOREIGN KEY(counterName) REFERENCES counter(name))""")
        self.connection.commit()

    def add_habit(self, name: str, description: str) -> None:
        """Add a habit to the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO counter VALUES (?, ?)", (name, description))
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"Habit with name '{name}' already exists.")

    def remove_habit(self, name: str) -> None:
        """Remove a habit from the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM counter WHERE name=?", (name,))
            if cursor.rowcount == 0:
                raise sqlite3.IntegrityError("No habit found with the given name")
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            raise e

    def increment_counter(self, name: str, event_date: str = None) -> None:
        """Increment the counter in the database."""
        cursor = self.connection.cursor()
        try:           
            cursor.execute("SELECT * FROM counter WHERE name=?", (name,))
            habit_exists = cursor.fetchone()
            if not habit_exists:
                raise sqlite3.IntegrityError("No habit found with the given name")
            
            if not event_date:
                event_date = datetime.today().date()
            cursor.execute("INSERT INTO tracker VALUES (?, ?)", (str(event_date), name))
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            raise e

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

    def get_habit_data(self, name: str) -> list:
        """Get habit data from the database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM counter WHERE name=?", (name,))
        return cursor.fetchone()

    def get_streaks(self):
        """Get streaks data from the database."""
        streaks = {}
        for habit_name in self.get_habits():
            habit_data = self.get_counter_data(habit_name)
            completed_dates = [row[0] for row in habit_data]
            streaks[habit_name] = self.calculate_streak(completed_dates)
        return streaks

    def calculate_streak(self, completed_dates: list) -> int:
        """Calculate streak based on completed dates."""
        streak = 0
        current_date = datetime.now().date()
        for completed_date_str in reversed(completed_dates):
            completed_date = datetime.strptime(completed_date_str, "%Y-%m-%d").date()
            if (current_date - completed_date).days <= 1:
                streak += 1
                current_date = completed_date - timedelta(days=1)
            else:
                break
        return streak

    def update_database(self):
        """Update the database with current habit data."""
        for habit_name in self.get_habits():
            habit = Habit(habit_name, "")
            habit_data = self.get_counter_data(habit_name)
            habit.completed_tasks = [row[0] for row in habit_data]
            self.increment_counter(habit_name, habit.completed_tasks[-1])  

    def clear_database(self):
        """Clear all data from the database."""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM counter")
        cursor.execute("DELETE FROM tracker")
        self.connection.commit()        

    def close(self):
        """Close the database connection."""
        self.connection.close()
