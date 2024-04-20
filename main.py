from datetime import datetime
from database import HabitDatabase
from habit import Habit
from initialize_database import initialize_database
from analytics import *


def main(habit_database):
    """Main function to initialize and run the Habit Tracker."""
    print("\n\n~WELCOME TO THE HABIT TRACKER (by MV)~\n")

    predefined_habits = initialize_database()

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

    predefined_daily_habits = [habit for habit in predefined_habits if habit['periodicity'] == "Daily"]
    predefined_weekly_habits = [habit for habit in predefined_habits if habit['periodicity'] == "Weekly"]

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
        for habit in predefined_daily_habits:
            print(f"{current_index}. {habit['name']} - {habit['description']}")
            current_index += 1

    print("\nPredefined Weekly Habits:")
    if not predefined_weekly_habits:
        print("No predefined weekly habits added yet.")
    else:
        for habit in predefined_weekly_habits:
            print(f"{current_index}. {habit['name']} - {habit['description']}")
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
                else:
                    selected_habit = predefined_habits[choice - len(daily_habits) - len(weekly_habits) - 1]
                    periodicity = "Predefined"
                manage_selected_habit_menu(habit_database, selected_habit, periodicity)
                break
            else:
                print(f"~ Invalid choice. Please enter a number from 1 to {total_habits}.")
        else:
            print("~ Invalid choice. Please enter a number.")
    
    return False

def manage_selected_habit_menu(habit_database, selected_habit, periodicity):
    """Menu for managing a selected habit."""
    print(f"\nHabit: {selected_habit['name']}")
    print("1. Mark habit as Done")
    print("2. Check habit status")
    print("3. View current streak")
    print("4. Delete habit")

    while True:
        choice = input("\nPlease enter the number of your choice: ").strip()

        if choice == "1":
            mark_habit_as_done(habit_database, selected_habit['name'])
            break
        elif choice == "2":
            check_habit_status(habit_database, selected_habit['name'])
            break
        elif choice == "3":
            view_current_streak(habit_database, selected_habit['name'])
            break
        elif choice == "4":
            if periodicity == "Predefined":
                delete_predefined_habit(habit_database, selected_habit['name'])
            else:
                delete_habit(habit_database, selected_habit['name'])
            return True 
        else:
            print("~ Invalid choice. Please enter a number from 1 to 4.")
       
def delete_predefined_habit(habit_database, habit_name):
    """Delete a predefined habit."""
    try:
        habit_database.delete_predefined_habit(habit_name)
        print(f"~ Predefined habit ('{habit_name}') successfully deleted!\n")
    except ValueError as e:
        print(e)

def delete_habit(habit_database, habit_name):
    """Delete a habit."""
    try:
        if habit_database.is_predefined_habit(habit_name):            
            habit_database.delete_predefined_habit(habit_name)
            print(f"~ Predefined habit ('{habit_name}') successfully deleted!\n")
        else:          
            habit_database.delete_habit(habit_name)
            print(f"~ Habit ('{habit_name}') successfully deleted!\n")
        return True
    except ValueError as e:
        print(e)
        return False

def mark_habit_as_done(habit_database, habit_name):
    """Marks a habit as Done."""
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    if habit_database.check_habit_done_today(habit_name, today_date):
        print(f"~ Sorry, but you've already marked the habit ('{habit_name}') as Done today.\n")
    elif habit_database.is_predefined_habit(habit_name):
        print(f"~ Sorry, but predefined habits like the habit ('{habit_name}') cannot be marked as Done.\n")
    else:
        habit_database.complete_habit(habit_name)
        print(f"~ Hurray! Habit ('{habit_name}') marked as Done for today.\n")

def check_habit_status(habit_database, habit_name):
    """Check the status of a habit."""
    if habit_name == "Predefined Habits":
        view_predefined_habits_status(habit_database)
        return

    status = habit_database.check_habit_status(habit_name)

    if status == "not_started":
        print(f"~ Habit ('{habit_name}') has not been started yet.\n")
    elif status == "inconsistent":
        print(f"~ You're finding it challenging to stick to the habit ('{habit_name}'). Aim for better consistency.\n")
    elif status == "consistently_followed":
        print(f"~ You are consistent with the habit ('{habit_name}'). Keep it up!\n")
    else:
        print("Error: Unexpected return value from habit_database.check_habit_status")


def view_current_streak(habit_database, habit_name):
    """View the current streak of a habit."""
    streak = habit_database.get_streak_for_habit(habit_name)
    print(f"Current streak for habit ('{habit_name}') is {streak}.\n")


def clear_all_habits(habit_database):
    """Clear all habits."""
    user_defined_habits = habit_database.get_habits()
    predefined_habits = habit_database.get_predefined_habits()

    if not user_defined_habits and not predefined_habits:
        print("~ No habits to clear.\n")
        return

    for habit in user_defined_habits:
        habit_database.delete_habit(habit['name'])

    for habit in predefined_habits:
        habit_database.delete_habit(habit['name'])

    print("~ All habits cleared.\n")

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


def view_longest_streak_menu(habit_database, periodicity=None):
    """View the longest streak."""
    if periodicity == "All":
        longest_streak_habit, longest_streak = get_longest_streak(habit_database)
        streak_count = habit_database.get_streak_for_habit(longest_streak_habit)
        print(f"Habit ('{longest_streak_habit}') has the longest streak out of all the habits! (Streak count: {streak_count})\n")
    else:
        longest_streak_habit, longest_streak = get_longest_streak(habit_database, periodicity)
        streak_count = habit_database.get_streak_for_habit(longest_streak_habit)
        print(f"Habit ('{longest_streak_habit}') has the longest streak among {periodicity.lower()} habits! (Streak count: {streak_count})\n")


if __name__ == "__main__":
    habit_database = HabitDatabase() 
    main(habit_database)