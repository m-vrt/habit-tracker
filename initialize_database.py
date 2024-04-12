from database import HabitDatabase
from habit import Habit
from datetime import datetime, timedelta

def main():
    """Initialize the habit database."""
    db = HabitDatabase("test.db") 
    
    habits = [
        {"name": "Morning Exercise", "description": "Run for 30 minutes", "periodicity": "daily"},
        {"name": "Reading Time", "description": "Read for 1 hour", "periodicity": "daily"},
        {"name": "Meditation", "description": "Meditate for 20 minutes", "periodicity": "daily"},
        {"name": "Grocery Shopping", "description": "Buy groceries for next week", "periodicity": "weekly"},
        {"name": "Water Intake", "description": "Drink 8 glasses of water", "periodicity": "daily"}
    ]
    
    for habit_info in habits:
        habit_name = habit_info["name"]
        if habit_name not in db.get_habits():
            habit = Habit(habit_name, habit_info["description"], habit_info["periodicity"], datetime.now().strftime('%Y-%m-%d'))
            db.add_habit(habit.name, habit.task_specification)
    
    for habit_info in habits:
        habit_name = habit_info["name"]
        if habit_name in db.get_habits():
            habit = Habit(habit_name, habit_info["description"], habit_info["periodicity"], datetime.now().strftime('%Y-%m-%d'))
            for i in range(1, 5):
                for j in range(i):
                    habit.complete_task()
                    habit.completed_tasks[-1] = (datetime.now() - timedelta(weeks=i-j)).strftime("%Y-%m-%d")
        
    db.close()

if __name__ == "__main__":
    main()
