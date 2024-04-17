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
        cursor.execute("""CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            description TEXT,
            periodicity TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_date TEXT,
            completed_time TEXT,
            streak INTEGER DEFAULT 0,
            counter INTEGER DEFAULT 0,
            is_predefined INTEGER DEFAULT 0)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY,
            habit_name TEXT,
            completion_date TEXT,
            FOREIGN KEY (habit_name) REFERENCES habits (name))""")
        self.connection.commit()

    def add_habit(self, name: str, description: str, periodicity: str) -> None:
        """Add a habit to the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO habits (name, description, periodicity, is_predefined) VALUES (?, ?, ?, 0)",
                           (name, description, periodicity))
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"Habit ('{name}') already exists.")

    def add_predefined_habit(self, name: str, description: str, periodicity: str) -> None:
        """Add a predefined habit to the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO habits (name, description, periodicity, is_predefined) VALUES (?, ?, ?, 1)",
                           (name, description, periodicity))
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"Predefined habit ('{name}') already exists.")
              
    def delete_habit(self, name: str) -> None:
        """Delete a habit from the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM habits WHERE name=?", (name,))
            if cursor.rowcount == 0:
                raise ValueError("No habit found with the given name")
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            raise e

    def get_habits(self):
        """Get the list of habits."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, description FROM habits")
        return [{'name': row[0], 'description': row[1]} for row in cursor.fetchall()]

    def get_habits_by_periodicity(self, periodicity=None):
        """Get habits filtered by periodicity."""
        cursor = self.connection.cursor()
        if periodicity:
            cursor.execute("SELECT name, description FROM habits WHERE periodicity=? AND is_predefined=0", (periodicity,))
        else:
            cursor.execute("SELECT name, description FROM habits WHERE is_predefined=0")
        return [{'name': row[0], 'description': row[1]} for row in cursor.fetchall()]

    def habit_exists(self, name: str) -> bool:
        """Check if a habit exists in the database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT 1 FROM habits WHERE name=?", (name,))
        return cursor.fetchone() is not None

    def check_habit_status(self, name: str) -> str:
        """Check the status of a habit."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT completed_date FROM habits WHERE name=? AND completed_date IS NOT NULL", (name,))
        completed_dates = [datetime.strptime(row[0], "%Y-%m-%d") for row in cursor.fetchall()]        
    
        if not completed_dates:
            return "not_started"

        last_week = datetime.now() - timedelta(days=7)
        if any(date > last_week for date in completed_dates):
            return "consistently_followed"
        else:
            return "inconsistent"

    def complete_habit(self, name: str) -> None:
        """Mark a habit as completed."""
        cursor = self.connection.cursor()
        cursor.execute("UPDATE habits SET completed_date=? WHERE name=?", (datetime.now().strftime("%Y-%m-%d"), name))
        self.connection.commit()

    def get_streak_for_habit(self, name: str) -> int:
        """Get the streak for a specific habit."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT streak FROM habits WHERE name=?", (name,))
        return cursor.fetchone()[0]

    def get_streaks(self):
        """Get streaks for all habits."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, streak FROM habits")
        return {row[0]: row[1] for row in cursor.fetchall()}

    def get_habit_by_name(self, name: str) -> Habit:
        """Get a habit by its name."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM habits WHERE name=?", (name,))
        row = cursor.fetchone()
        if row:
            id, name, description, periodicity, created_date, completed_date, completed_time, streak, counter = row
            return Habit(id, name, description, periodicity, created_date, completed_date, completed_time, streak, counter)
        else:
            return None
    
    def update_streak(self, name: str, streak: int) -> None:
        """Update the streak for a specific habit."""
        cursor = self.connection.cursor()
        cursor.execute("UPDATE habits SET streak = ? WHERE name = ?", (streak, name))
        self.connection.commit()
        
    def increment_counter(self, name: str, date: str = None) -> None:
        """Increment the counter for a specific habit."""
        cursor = self.connection.cursor()
        if date:
            cursor.execute("UPDATE habits SET counter = counter + 1 WHERE name = ? AND completed_date = ?", (name, date))
        else:
            cursor.execute("UPDATE habits SET counter = counter + 1 WHERE name = ?", (name,))
        self.connection.commit()

    def check_habit_done_today(self, habit_name: str, date: str) -> bool:
        """Check if a habit has been marked as done on the given date."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM habits WHERE name=? AND completed_date=?", (habit_name, date))
        count = cursor.fetchone()[0]
        return count > 0

    def clear_all_habits(self):
        """Clear all habits from the database."""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM habits")
        cursor.execute("DELETE FROM completions")
        self.connection.commit()

    def close(self):
        """Close the database connection."""
        self.connection.close()
