from database import HabitDatabase

def initialize_database(habit_database):
    """Initialize the database with predefined habits."""
    habit_database = HabitDatabase()

    try:
        habit_database.clear_all_predefined_habits()
        habit_database.copy_predefined_data_to_completions()

        predefined_daily_habits = habit_database.get_predefined_habits_by_periodicity("Daily")
        predefined_weekly_habits = habit_database.get_predefined_habits_by_periodicity("Weekly")

        for habit in predefined_daily_habits:
            habit_database.add_predefined_habit(habit["name"], habit["description"], habit["periodicity"])
          
        for habit in predefined_weekly_habits:
            habit_database.add_predefined_habit(habit["name"], habit["description"], habit["periodicity"])

    finally:
        habit_database.close()

    return predefined_daily_habits, predefined_weekly_habits


if __name__ == "__main__":
    
    habit_database = HabitDatabase()  
    initialize_database(habit_database)
