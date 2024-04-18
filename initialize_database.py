import random
import string
from datetime import datetime, timedelta
from database import HabitDatabase

def generate_unique_habit_name(existing_names):
    """Generate a unique habit name."""
    while True:
        name = ''.join(random.choices(string.ascii_lowercase, k=8)).capitalize()
        if name not in existing_names:
            return name

def capitalize_first_letter(sentence):
    """Capitalize the first letter of each word in a sentence."""
    return ' '.join(word.capitalize() for word in sentence.split())

def initialize_database():
    """Initialize the database with predefined habits and example tracking data."""
    habit_database = HabitDatabase()

    predefined_habits = []

    predefined_daily_habit_names = set()
    predefined_weekly_habit_names = set()

    while len(predefined_daily_habit_names) < 5:
        predefined_daily_habit_names.add(generate_unique_habit_name(predefined_daily_habit_names | predefined_weekly_habit_names))

    while len(predefined_weekly_habit_names) < 5:
        predefined_weekly_habit_names.add(generate_unique_habit_name(predefined_daily_habit_names | predefined_weekly_habit_names))

    for habit_name in predefined_daily_habit_names:
        description = capitalize_first_letter(f"Description for {habit_name}")
        habit_database.add_predefined_habit(habit_name, description, "Daily")
        predefined_habits.append({"name": habit_name, "description": description, "periodicity": "Daily"})

    for habit_name in predefined_weekly_habit_names:
        description = capitalize_first_letter(f"Description for {habit_name}")
        habit_database.add_predefined_habit(habit_name, description, "Weekly")
        predefined_habits.append({"name": habit_name, "description": description, "periodicity": "Weekly"})

    for habit in predefined_habits:
        habit_database.mark_habit_as_predefined(habit['name'])

       
        start_date = datetime.now() - timedelta(days=28)
        for _ in range(28):
            completion_date = start_date + timedelta(days=random.randint(0, 3))  
            status = random.choice(["not_started", "inconsistent", "consistently_followed"])  
            habit_database.add_tracking_data(habit['name'], completion_date, status)

    return predefined_habits

if __name__ == "__main__":
    initialize_database()