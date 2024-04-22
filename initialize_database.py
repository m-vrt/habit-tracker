import random
from datetime import datetime, timedelta
from database import HabitDatabase

def initialize_database():
    """Initialize the database with predefined habits."""
    habit_database = HabitDatabase()
    
    try:       
        habit_database.clear_all_predefined_habits()

        predefined_habits = []

        predefined_daily_habits = [
            {"name": "Study", "description": "Study current module.", "periodicity": "Daily"},
            {"name": "Code", "description": "Practice coding.", "periodicity": "Daily"},
            {"name": "Research", "description": "Do some research.", "periodicity": "Daily"},
            {"name": "Drink Water", "description": "Stay hydrated.", "periodicity": "Daily"},
            {"name": "Exercise", "description": "Get some form of exercise.", "periodicity": "Daily"}
        ]

        predefined_weekly_habits = [
            {"name": "Grocery Shopping", "description": "Buy groceries for next week.", "periodicity": "Weekly"},
            {"name": "Clean House", "description": "Do household chores.", "periodicity": "Weekly"},
            {"name": "Go Out", "description": "Get some fresh air.", "periodicity": "Weekly"},
            {"name": "Call Family", "description": "Check in with family members.", "periodicity": "Weekly"},
            {"name": "Review Goals", "description": "Reflect on personal goals.", "periodicity": "Weekly"}
        ]

        for habit in predefined_daily_habits:
            habit_database.add_predefined_habit(habit["name"], habit["description"], habit["periodicity"])
            predefined_habits.append(habit)

        for habit in predefined_weekly_habits:
            habit_database.add_predefined_habit(habit["name"], habit["description"], habit["periodicity"])
            predefined_habits.append(habit)

        for habit in predefined_habits:
            habit_database.mark_habit_as_predefined(habit['name'])
        
            start_date = datetime.now() - timedelta(days=28 * 4)  
            for _ in range(28 * 4):  
                completion_date = start_date + timedelta(days=random.randint(0, 3))
                status = random.choice(["not_started", "inconsistent", "consistently_followed"])
                habit_database.add_tracking_data(habit['name'], completion_date, status)

    finally:
        habit_database.close()

    return predefined_habits


if __name__ == "__main__":
    initialize_database()
