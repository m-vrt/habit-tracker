from datetime import datetime, timedelta
from database import HabitDatabase
from habit import Habit

def initialize_database():
    """Initialize the database with predefined habits and example tracking data."""
    db = HabitDatabase("test.db") 
    
    try:
        habits = [
            {"name": "Daily Exercise", "description": "Run for 30 minutes", "periodicity": "daily"},
            {"name": "Reading Time", "description": "Read for 1 hour", "periodicity": "daily"},
            {"name": "Meditation", "description": "Meditate for 20 minutes", "periodicity": "daily"},
            {"name": "Grocery Shopping", "description": "Buy groceries for next week", "periodicity": "weekly"},
            {"name": "Water Intake", "description": "Drink 8 glasses of water", "periodicity": "daily"}
        ]
        
        for habit_info in habits:
            habit_name = habit_info["name"]
            if habit_name not in db.get_habits():            
                habit = Habit(habit_name, habit_info["description"], habit_info["periodicity"])
                db.add_habit(habit.name, habit.task_specification)               
                if habit.periodicity == "daily":
                    current_date = datetime.now()
                    for _ in range(28):  
                        db.increment_counter(habit_name, current_date, current_date)
                        current_date -= timedelta(days=1)
                elif habit.periodicity == "weekly":
                    current_date = datetime.now()
                    for _ in range(4):  
                        db.increment_counter(habit_name, current_date, current_date)
                        current_date -= timedelta(weeks=1)

    except Exception as e:
        print(f"Error occurred during database initialization: {str(e)}")
        db.close()
    else:
        print("Database initialized successfully.")
        db.close()

if __name__ == "__main__":
    initialize_database()
