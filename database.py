from datetime import datetime, timedelta
from typing import Dict, List
import sqlite3


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
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                periodicity TEXT,
                created_date TIMESTAMP,
                completion_date TEXT,
                completion_time TIMESTAMP,
                streak INTEGER DEFAULT 0,
                counter INTEGER DEFAULT 0,
                is_predefined INTEGER DEFAULT 0)""")          
        except sqlite3.Error as e:
            print("Error occurred while creating the habits table:", e)

        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                periodicity TEXT,
                created_date TIMESTAMP,
                completion_date TEXT,
                completion_time TIMESTAMP,
                streak INTEGER DEFAULT 0,
                counter INTEGER DEFAULT 0)""")  
        except sqlite3.Error as e:
            print("Error occurred while creating the completions table:", e)

        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS predefined_data (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                periodicity TEXT,
                created_date TIMESTAMP,
                completion_date TEXT,
                completion_time TIMESTAMP,
                streak INTEGER DEFAULT 0,
                counter INTEGER DEFAULT 0)""")  
        except sqlite3.Error as e:
            print("Error occurred while creating the predefined_data table:", e)
        
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS predefined_habits (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                periodicity TEXT)""")         
        except sqlite3.Error as e:
            print("Error occurred while creating the predefined_habits table:", e)

        self.connection.commit()

    def add_habit(self, name: str, description: str, periodicity: str) -> None:
        """Add a habit to the database."""
        cursor = self.connection.cursor()
        created_date = datetime.now().strftime("%m/%d/%Y %H:%M")  
        cursor.execute("INSERT INTO habits (name, description, periodicity, created_date) VALUES (?, ?, ?, ?)",
                   (name, description, periodicity, created_date))
        self.connection.commit()
        
    def add_predefined_habit(self, name: str, description: str, periodicity: str) -> None:
        """Add a predefined habit to the database if it doesn't already exist."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM predefined_habits WHERE name = ? AND description = ? AND periodicity = ?",
                   (name, description, periodicity))
        existing_count = cursor.fetchone()[0]
        if existing_count == 0:
            cursor.execute("INSERT INTO predefined_habits (name, description, periodicity) VALUES (?, ?, ?)",
                       (name, description, periodicity))
            self.connection.commit()
             
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

    def delete_predefined_habit(self, name: str) -> None:
        """Delete a predefined habit from the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM completions WHERE name=?", (name,))
            cursor.execute("DELETE FROM predefined_habits WHERE name=?", (name,))
            if cursor.rowcount == 0:
                print("DEBUG: No predefined habit found with the given name:", name)  
                raise ValueError("No predefined habit found with the given name")
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            raise e

    def get_habits(self):
        """Get the list of habits."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, description FROM habits")
        return [{'name': row[0], 'description': row[1]} for row in cursor.fetchall()]

    def get_habits_by_periodicity(self, periodicity):
        """Get habits filtered by periodicity."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT name, description, MIN(created_date) FROM habits WHERE periodicity=? GROUP BY name, periodicity ORDER BY MIN(created_date)", (periodicity,))
    
        habits = {}
        for row in cursor.fetchall():
            name = row[0]
            description = row[1]
            created_date = row[2]
            habit_key = (name, periodicity, created_date)
            if habit_key not in habits:
                habits[habit_key] = {'description': description}
    
        return [{'name': key[0], 'description': habit['description']} for key, habit in habits.items()]
       
    def complete_habit(self, name: str, description: str, periodicity: str) -> bool:
        """Mark a habit as completed."""
        completion_date = datetime.now().strftime("%m/%d/%Y")
        completion_time = datetime.now().strftime("%H:%M:%S")

        cursor = self.connection.cursor()

        try:            
            existing_completion_query = "SELECT COUNT(*) FROM habits WHERE name=? AND completion_date IS NOT NULL AND periodicity=?"
            cursor.execute(existing_completion_query, (name, periodicity))
            existing_completion_count = cursor.fetchone()[0]

            if existing_completion_count == 0:               
                cursor.execute("UPDATE habits SET completion_date=?, completion_time=? WHERE name=? AND completion_date IS NULL AND periodicity=?",
                           (completion_date, completion_time, name, periodicity))
                self.connection.commit()
            else:                
                cursor.execute("SELECT created_date FROM habits WHERE name=? LIMIT 1", (name,))
                row = cursor.fetchone()
                if row:
                    created_date = row[0]
                else:
                    raise ValueError("No habit found with the given name")
               
                cursor.execute("INSERT INTO habits (name, description, periodicity, created_date, completion_date, completion_time) VALUES (?, ?, ?, ?, ?, ?)",
                           (name, description, periodicity, created_date.strftime("%m/%d/%Y %H:%M"), completion_date, completion_time))
                self.connection.commit()

            return True
        except Exception as e:
            self.connection.rollback()
            return False
      
    def check_habit_done(self, habit_name: str, completion_date: str, periodicity: str) -> bool:
        """Check if a habit has been marked as done within the specified period."""
        cursor = self.connection.cursor()
        query_date = datetime.strptime(completion_date, "%m/%d/%Y")
       
        if periodicity == "daily":
            start_of_day = completion_date + " 00:00:00"
            end_of_day = completion_date + " 23:59:59"
            cursor.execute("SELECT COUNT(*) FROM completions WHERE name=? AND completion_date = ? AND periodicity = ?",
                       (habit_name, completion_date, periodicity))
        elif periodicity == "weekly":
            start_of_week = query_date - timedelta(days=query_date.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            start_of_week_str = start_of_week.strftime("%m/%d/%Y") + " 00:00:00"
            end_of_week_str = end_of_week.strftime("%m/%d/%Y") + " 23:59:59"
            cursor.execute("SELECT COUNT(*) FROM completions WHERE name=? AND completion_date BETWEEN ? AND ? AND periodicity = ?",
                       (habit_name, start_of_week_str, end_of_week_str, periodicity))

        count_row = cursor.fetchone()
        if count_row:
            count = count_row[0]
            return count > 0
        else:
            return False

    def clear_all_habits(self):
        """Clear all user-defined habits from the database."""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM habits")
        cursor.execute("DELETE FROM predefined_habits")  
        cursor.execute("DELETE FROM completions")
        self.connection.commit()

    def clear_all_predefined_habits(self):
        """Clear all predefined habits from the database."""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM predefined_habits")
        cursor.execute("DELETE FROM completions")
        self.connection.commit()

    def mark_habit_as_predefined(self, habit_name):
        """Mark a habit as predefined."""
        cursor = self.connection.cursor()
        cursor.execute("UPDATE habits SET is_predefined = 1 WHERE name = ?", (habit_name,))
        self.connection.commit()
    
    def get_predefined_habits(self) -> List[str]:
        """Get the list of predefined habits."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM predefined_data")
        return [row[0] for row in cursor.fetchall()]
    
    def get_predefined_habits_from_predefined_habits_table(self) -> List[str]:
        """Get predefined habits from predefined habits table."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM predefined_habits")
        return [row[0] for row in cursor.fetchall()]

    def get_predefined_habits_by_periodicity(self, periodicity: str) -> List[Dict[str, str]]:
        """Get predefined habits by periodicity."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, description, periodicity FROM predefined_data WHERE periodicity=?", (periodicity,))
        rows = cursor.fetchall()
        return [{'name': row[0], 'description': row[1], 'periodicity': row[2]} for row in rows]
    
    def get_predefined_habits_by_periodicity_from_predefined_habits_table(self, periodicity: str) -> List[Dict[str, str]]:
        """Get predefined habits by periodicity from predefined habits table."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, description, periodicity FROM predefined_habits WHERE periodicity=?", (periodicity,))
        rows = cursor.fetchall()
        return [{'name': row[0], 'description': row[1]} for row in rows]
    
    def is_predefined_habit(self, habit_name: str) -> bool:
        """Check if a habit is predefined."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM predefined_habits WHERE name=?", (habit_name,))
        result = cursor.fetchone()
        if result and result[0] > 0:
            return True
        return False

    def copy_predefined_data_to_completions(self):
        """Copy data from predefined_data to completions table."""
        cursor = self.connection.cursor()
        cursor.execute("""INSERT INTO completions (id, name, description, periodicity, created_date, completion_date, completion_time)
                          SELECT id, name, description, periodicity, created_date, completion_date, completion_time
                          FROM predefined_data""")
        self.connection.commit()
    
    
    
    def close(self):
        """Close the database connection."""
        self.connection.close()