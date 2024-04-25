from database import HabitDatabase

def initialize_database():
    """Initialize the database with predefined habits."""
    habit_database = HabitDatabase()

    try:
        habit_database.clear_all_predefined_habits()
        
        predefined_habits = habit_database.get_predefined_habits()
        
        predefined_daily_habits = []
        predefined_weekly_habits = []

        for habit in predefined_habits:
          
            habit_database.mark_habit_as_predefined(habit['name'])
         
            data = habit_database.get_predefined_data(habit['name'])

            for record in data:
                created_date = record['created_date']
                completion_date = record['completion_date']
                completion_time = record['completion_time']
                
                habit_database.add_tracking_data(
                    habit['name'],
                    habit['description'],
                    habit['periodicity'],
                    created_date,
                    completion_date,
                    completion_time
                )
               
                if habit['periodicity'] == 'Daily':
                    predefined_daily_habits.append(habit)
                elif habit['periodicity'] == 'Weekly':
                    predefined_weekly_habits.append(habit)
        
        for habit in predefined_daily_habits:
            habit_database.add_predefined_habit(habit["name"], habit["description"], habit["periodicity"])

        for habit in predefined_weekly_habits:
            habit_database.add_predefined_habit(habit["name"], habit["description"], habit["periodicity"])

    finally:
        habit_database.close()

if __name__ == "__main__":
    initialize_database()
