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
                completion_time TIMESTAMP)""")          
        except sqlite3.Error as e:
            print("Error occurred while creating the habits table:", e)
        
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS predefined_data (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                periodicity TEXT,
                created_date TIMESTAMP,
                completion_date TEXT,
                completion_time TIMESTAMP)""")  
        except sqlite3.Error as e:
            print("Error occurred while creating the predefined_data table:", e)
             
        self.connection.commit()

    def add_habit(self, name: str, description: str, periodicity: str) -> None:
        """Add a habit to the database."""
        cursor = self.connection.cursor()
        created_date = datetime.now().strftime("%m/%d/%Y %H:%M")  
        cursor.execute("INSERT INTO habits (name, description, periodicity, created_date) VALUES (?, ?, ?, ?)",
                   (name, description, periodicity, created_date))
        self.connection.commit()       
             
    def delete_habit(self, name: str, created_date: str) -> None:
        """Delete habits with the given name and created_date from the database."""
        cursor = self.connection.cursor()
        try:          
            if self.is_predefined_habit(name):
                print(f"~ Sorry, but predefined habits like the habit '{name}' cannot be deleted.\n")
            else:
                cursor.execute("DELETE FROM habits WHERE name=? AND created_date=?", (name, created_date))
                self.connection.commit()
                print(f"~ Habit '{name}' successfully deleted!\n")
        except sqlite3.IntegrityError as e:           
            print(f"Error deleting habit: {e}")
       
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
            cursor.execute("SELECT created_date FROM habits WHERE name=? AND periodicity=? ORDER BY created_date ASC LIMIT 1", (name, periodicity))
            original_created_date = cursor.fetchone()[0]       
            existing_completion_query = "SELECT COUNT(*) FROM habits WHERE name=? AND completion_date IS NOT NULL AND periodicity=?"
            cursor.execute(existing_completion_query, (name, periodicity))
            existing_completion_count = cursor.fetchone()[0]

            if existing_completion_count == 0:               
                cursor.execute("UPDATE habits SET completion_date=?, completion_time=? WHERE name=? AND completion_date IS NULL AND periodicity=?",
                           (completion_date, completion_time, name, periodicity))
                self.connection.commit()
            else:             
                cursor.execute("INSERT INTO habits (name, description, periodicity, created_date, completion_date, completion_time) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, description, periodicity, original_created_date, completion_date, completion_time))
                self.connection.commit()
            
            cursor.execute("""SELECT * FROM habits
                          ORDER BY name, created_date, CASE periodicity WHEN 'Daily' THEN 1 ELSE 2 END, completion_date""")
        
            return True
        except Exception as e:
            self.connection.rollback()
            return False
       
    def check_habit_done(self, habit_name: str, completion_date: str, periodicity: str) -> bool:
        pass

    def clear_all_habits(self):
        """Clear all user-defined habits from the database."""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM habits")    
        self.connection.commit()
           
    def is_predefined_habit(self, habit_name: str) -> bool:
        """Check if a habit is predefined."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM predefined_data WHERE name=?", (habit_name,))
        result = cursor.fetchone()
        if result and result[0] > 0:
            return True
        return False
    
    def get_habit_description(self, habit_name: str) -> str:
        """Get the description of a habit by its name."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT description FROM habits WHERE name=?", (habit_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return ""
    
    def get_created_date(self, habit_name: str) -> str:
        """Retrieve the creation date of a habit."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT created_date FROM habits WHERE name=?", (habit_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return ""
    
    def close(self):
        """Close the database connection."""
        self.connection.close()