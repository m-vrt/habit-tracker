from datetime import datetime
import analytics
from database import HabitDatabase
from habit import Habit
from initialize_database import initialize_database
from analytics import view_longest_streak_menu


def main(habit_database):
    """Main function to initialize and run the Habit Tracker."""
    print("\n\n~WELCOME TO THE HABIT TRACKER (by MV)~\n")

    predefined_habits = initialize_database()
    analytics.calculate_streaks(habit_database)  

    while True:
        print_menu()
        choice = input("\nPlease enter the number of your choice: ").strip()

        if choice == "1":
            add_habit_menu(habit_database)
        elif choice == "2":
            manage_habits_menu(habit_database, predefined_habits)
        elif choice == "3":
            view_habit_hall_of_fame_menu(habit_database)
        elif choice == "4":
            print("~ Quitting the Habit Tracker...")
            habit_database.close()
            break
        else:
            print("~ Invalid choice. Please enter a number from 1 to 4.")


def print_menu():
    """Print the menu options."""
    print("\nWhat would you like to do?\n")
    print("1. Add habit")
    print("2. Manage habits")
    print("3. View Habit Hall of Fame")
    print("4. Quit")


def add_habit_menu(habit_database):
    """Menu for adding a new habit."""
    print("\nADD HABIT")

    while True:
        habit_name = input("Habit name: ").strip()
        if not habit_name:
            print("~ Habit name cannot be empty. Please try again.")
        else:
            break

    while True:
        habit_description = input("Habit description: ").strip()
        if not habit_description:
            print("~ Habit description cannot be empty. Please try again.")
        else:
            break

    while True:
        periodicity = input("Daily or Weekly: ").capitalize().strip()
        if periodicity in ["Daily", "Weekly"]:
            break
        else:
            print("~ Please enter either 'Daily' or 'Weekly'.")

    habit_database.add_habit(habit_name.capitalize(), habit_description.capitalize(), periodicity)
    print(f"~ Habit ('{habit_name.capitalize()}') successfully added to {periodicity} Habits!\n")


def manage_habits_menu(habit_database, predefined_habits):
    """Menu for managing habits."""
    while True:
        print("\nMANAGE HABITS")
        print("1. View list of habits")
        print("2. Clear all habits")
        print("3. Return to Main Menu")

        choice = input("\nPlease enter the number of your choice: ").strip()

        if choice == "1":
            if view_habits_menu(habit_database, predefined_habits):
                break
        elif choice == "2":
            clear_all_habits(habit_database)
        elif choice == "3":
            break
        else:
            print("~ Invalid choice. Please enter a number from 1 to 3.")


def view_habits_menu(habit_database, predefined_habits):
    """Menu for viewing the list of habits."""
    print("\nVIEW LIST OF HABITS")

    daily_habits = habit_database.get_habits_by_periodicity("Daily")
    weekly_habits = habit_database.get_habits_by_periodicity("Weekly")

    predefined_daily_habits = habit_database.get_predefined_habits_by_periodicity("Daily")
    predefined_weekly_habits = habit_database.get_predefined_habits_by_periodicity("Weekly")

    total_habits = len(daily_habits) + len(weekly_habits) + len(predefined_daily_habits) + len(predefined_weekly_habits)
    current_index = 1

    print("\nDaily Habits:")
    if not daily_habits:
        print("No daily habits added yet.")
    else:
        for habit in daily_habits:
            print(f"{current_index}. {habit['name']} - {habit['description']}")
            current_index += 1

    print("\nWeekly Habits:")
    if not weekly_habits:
        print("No weekly habits added yet.")
    else:
        for habit in weekly_habits:
            print(f"{current_index}. {habit['name']} - {habit['description']}")
            current_index += 1

    print("\nPredefined Daily Habits:")
    if not predefined_daily_habits:
        print("No predefined daily habits added yet.")
    else:
        for index, habit in enumerate(predefined_daily_habits, start=current_index):
            print(f"{index}. {habit['name']} - {habit['description']}")
            current_index += 1

    print("\nPredefined Weekly Habits:")
    if not predefined_weekly_habits:
        print("No predefined weekly habits added yet.")
    else:
        for index, habit in enumerate(predefined_weekly_habits, start=current_index):
            print(f"{index}. {habit['name']} - {habit['description']}")
            current_index += 1

    if total_habits == 0:
        print("\n~ No habits to show.")
        return True

    while True:
        choice = input("\nPlease enter the number of your choice: ").strip()

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= total_habits:
                if choice <= len(daily_habits):
                    selected_habit = daily_habits[choice - 1]
                    periodicity = "Daily"
                elif choice <= len(daily_habits) + len(weekly_habits):
                    selected_habit = weekly_habits[choice - len(daily_habits) - 1]
                    periodicity = "Weekly"
                elif choice <= len(daily_habits) + len(weekly_habits) + len(predefined_daily_habits):
                    selected_habit = predefined_daily_habits[choice - len(daily_habits) - len(weekly_habits) - 1]
                    periodicity = "Predefined Daily"
                else:
                    selected_habit = predefined_weekly_habits[choice - len(daily_habits) - len(weekly_habits) - len(predefined_daily_habits) - 1]
                    periodicity = "Predefined Weekly"
                if manage_selected_habit_menu(habit_database, selected_habit, periodicity):                    
                    predefined_habits = habit_database.get_predefined_habits()
                break
            else:
                print(f"~ Invalid choice. Please enter a number from 1 to {total_habits}.")
        else:
            print("~ Invalid choice. Please enter a number.")

    return False


def manage_selected_habit_menu(habit_database, selected_habit, periodicity):
    """Menu for managing a selected habit."""
    if isinstance(selected_habit, str):       
        habit_name = selected_habit
        is_predefined = True
    else:       
        habit_name = selected_habit['name']
        is_predefined = False

    print(f"\n[Habit: {habit_name}]")
    print("1. Mark habit as Done")
    print("2. Check habit status")
    print("3. Delete habit")
    
    while True:
        choice = input("\nPlease enter the number of your choice: ").strip()

        if choice == "1":
            mark_habit_as_done(habit_database, habit_name)
            break
        elif choice == "2":
            check_habit_status(habit_database, habit_name)
            break
        elif choice == "3":
            if is_predefined:
                if delete_predefined_habit(habit_database, habit_name):
                    print(f"~ Habit ('{habit_name}') successfully deleted!\n")
                return True               
            else:
                if delete_habit(habit_database, habit_name):
                    print(f"~ Habit ('{habit_name}') successfully deleted!\n")
                return True
        else:
            print("~ Invalid choice. Please enter a number from 1 to 4.")

    return False

def delete_predefined_habit(habit_database, habit_name):
    """Delete a predefined habit."""
    try:
        habit_database.delete_predefined_habit(habit_name)   
    except ValueError as e:
        print(e)

def delete_habit(habit_database, habit_name):
    """Delete a habit."""
    try:
        if habit_database.is_predefined_habit(habit_name):            
            habit_database.delete_predefined_habit(habit_name)
        else:          
            habit_database.delete_habit(habit_name)           
        return True
    except ValueError as e:
        print(e)
        return False
       
def mark_habit_as_done(habit_database, habit_name):
    """Marks a habit as Done."""
    today_date = datetime.now().strftime("%Y-%m-%d")

    if habit_database.check_habit_done_today(habit_name, today_date):
        if "Weekly" in habit_name:
            print(f"~ Sorry, but you've already marked the habit ('{habit_name}') as Done this week. Please check back next week.\n")
        else:
            print(f"~ Sorry, but you've already marked the habit ('{habit_name}') as Done today. Please check back tomorrow.\n")
    elif habit_database.is_predefined_habit(habit_name):
        print(f"~ Sorry, but predefined habits like the habit '{habit_name}' cannot be marked as Done.\n")
    else:        
        habit = habit_database.get_habit_by_name(habit_name)
        if habit:
            description = habit.description
            periodicity = habit.periodicity
            habit_database.complete_habit(habit_name)
            print(f"~ Hurray! Habit '{habit_name}' marked as Done for today.\n")
        else:
            print(f"~ Habit '{habit_name}' not found in the database.\n")
            return

        habit_database.increment_counter(habit_name)
        habit_database.update_streak(habit_name, today_date)

def check_habit_status(habit_database, habit_name):
    """Check the status of a habit."""
    if habit_name == "Predefined Habits":
        check_predefined_habit_status(habit_database)
        return

    status = habit_database.check_habit_status(habit_name)

    if status == "not_started":
        print(f"~ Habit '{habit_name}' has not been started yet.\n")
    elif status == "inconsistent":
        print(f"~ You missed to complete the habit '{habit_name}' for {status} in a row. Aim for better consistency.\n")
    elif status.startswith("consistently_followed"):
        count = status.split("_")[1] 
        period = "days" if "daily" in status else "weeks"
        print(f"~ You have been consistent with the habit '{habit_name}' for [{count} {period}] in a row. Keep it up!\n")

def check_predefined_habit_status(habit_database):
    """Check the status of predefined habits."""
    predefined_habits = habit_database.get_predefined_habits()
    for habit_name in predefined_habits:
        print(f"Habit: {habit_name}")
        completion_date, completion_rate = habit_database.get_predefined_habit_status(habit_name)
        if completion_date:
            print(f"The habit was last completed on: {completion_date}")
            print(f"Predefined {'Daily' if 'Daily' in habit_name else 'Weekly'} Habit '{habit_name}' has a completion rate of {completion_rate} out of total {'days' if 'Daily' in habit_name else 'weeks'}.")
        
def get_predefined_habit_status(self, habit_name):
    """Get the last completion date and completion rate of a predefined habit."""
    cursor = self.connection.cursor()
    cursor.execute("SELECT COUNT(DISTINCT completion_date) FROM completions WHERE habit_name=?", (habit_name,))
    completion_count = cursor.fetchone()[0]
    if completion_count:
        cursor.execute("SELECT MAX(completion_date) FROM completions WHERE habit_name=?", (habit_name,))
        last_completion_date = cursor.fetchone()[0]
        if "Daily" in habit_name:
            total_days = (datetime.now() - datetime.strptime(last_completion_date, "%Y-%m-%d")).days + 1
        elif "Weekly" in habit_name:
            total_days = (datetime.now() - datetime.strptime(last_completion_date, "%Y-%m-%d")).days // 7 + 1
        else:
            total_days = 0
        completion_rate = f"{completion_count} / {total_days}"
        return last_completion_date, completion_rate
    else:
        return None, "0 / 0"

def clear_all_habits(habit_database):
    """Clear all habits."""
    try:       
        habit_database.clear_all_habits()    
        habit_database.clear_all_predefined_habits()
        print("~ All habits cleared.\n")
    except Exception as e:
        print(f"An error occurred: {e}")

def view_habit_hall_of_fame_menu(habit_database):
    """Menu for viewing the Habit Hall of Fame."""
    print("\nVIEW HABIT HALL OF FAME")
    print("1. Daily")
    print("2. Weekly")
    print("3. All habits")

    while True:
        choice = input("\nPlease enter the number of your choice: ").strip()

        if choice == "1":
            view_longest_streak_menu(habit_database, periodicity="Daily")
            break
        elif choice == "2":
            view_longest_streak_menu(habit_database, periodicity="Weekly")
            break
        elif choice == "3":
            view_longest_streak_menu(habit_database, periodicity="All")
            break
        else:
            print("~ Invalid choice. Please enter a number from 1 to 3.")




if __name__ == "__main__":
    habit_database = HabitDatabase() 
    try:
        main(habit_database)
    finally:
        habit_database.close()