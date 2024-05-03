from datetime import datetime
from database import HabitDatabase
from initialize_database import initialize_database
from habit_tracker_predefined import (
    check_habit_status_predefined_daily,
    get_predefined_daily_habits,
    check_habit_status_predefined_weekly,
    get_predefined_weekly_habits
)



def main(habit_database):
    """Main function to initialize and run the Habit Tracker."""
    print("\n\n~WELCOME TO THE HABIT TRACKER (by MV)~\n")

    predefined_daily_habits, predefined_weekly_habits = initialize_database(habit_database)
    predefined_habits = predefined_daily_habits + predefined_weekly_habits

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
    print("1. Add Habit")
    print("2. Manage Habits")
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
        print("1. View List of Habits")
        print("2. Clear All Habits")
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

    predefined_daily_habits = get_predefined_daily_habits(predefined_habits)
    predefined_weekly_habits = get_predefined_weekly_habits(predefined_habits)

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
                if manage_selected_habit_menu(habit_database, selected_habit, periodicity, predefined_habits):                    
                    break
            else:
                print(f"~ Invalid choice. Please enter a number from 1 to {total_habits}.")
        else:
            print("~ Invalid choice. Please enter a number.")

    return False


def manage_selected_habit_menu(habit_database, selected_habit, periodicity, predefined_habits):
    """Menu for managing a selected habit."""
    if isinstance(selected_habit, str):       
        habit_name = selected_habit
        is_predefined = True
    else:       
        habit_name = selected_habit['name']
        is_predefined = False

    print(f"\n[Habit: {habit_name}]")
    print("1. Mark Habit as Done")
    print("2. Check Habit Status")
    print("3. Delete Habit")
    print("4. Return to Previous Menu")
    
    while True:
        choice = input("\nPlease enter the number of your choice: ").strip()

        if choice == "1":
            mark_habit_as_done(habit_database, habit_name, periodicity)
            return True
        elif choice == "2":
            predefined_daily_habits = get_predefined_daily_habits(predefined_habits)
            predefined_weekly_habits = get_predefined_weekly_habits(predefined_habits)
    
            if any(habit['name'] == habit_name for habit in predefined_daily_habits):
                habit_status = check_habit_status_predefined_daily(habit_name)
                print(f"Habit Status for '{habit_name}':")
                print(habit_status.to_string(index=False, justify='center'))
                return True    
            elif any(habit['name'] == habit_name for habit in predefined_weekly_habits):
                habit_status = check_habit_status_predefined_weekly(habit_name)
                print(f"Habit Status for '{habit_name}':")
                print(habit_status.to_string(index=False, justify='center'))
                return True           
        elif choice == "3":
            if is_predefined:
                if delete_predefined_habit(habit_database, habit_name):
                    print(f"~ Habit ('{habit_name}') successfully deleted!\n")
                return True               
            else:
                if delete_habit(habit_database, habit_name):
                    print(f"~ Habit ('{habit_name}') successfully deleted!\n")
                return True
        elif choice == "4":
            return False  
        else:
            print("~ Invalid choice. Please enter a number from 1 to 4.")


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
       
def mark_habit_as_done(habit_database, habit_name, periodicity):
    """Marks a habit as Done."""
    completion_date = datetime.now().strftime("%m/%d/%Y")

    if habit_database.check_habit_done(habit_name, completion_date, periodicity):
        if periodicity == "Weekly":
            message = f"~ Sorry, but you've already marked the habit ('{habit_name}') as Done this week. Please check back next week.\n"
        else:
            message = f"~ Sorry, but you've already marked the habit ('{habit_name}') as Done today. Please check back tomorrow.\n"
        print(message)
    elif habit_database.is_predefined_habit(habit_name):
        message = f"~ Sorry, but predefined habits like the habit '{habit_name}' cannot be marked as Done.\n"
        print(message)
    else:
        if habit_database.complete_habit(habit_name, None, periodicity): 
            if periodicity == "Weekly":
                message = f"~ Hurray! Habit '{habit_name}' marked as Done for this week.\n"
            else:
                message = f"~ Hurray! Habit '{habit_name}' marked as Done for today.\n"
            print(message)       

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
    print("3. All Habits")
    print("4. Return to Main Menu")

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
        elif choice == "4":
            return  
        else:
            print("~ Invalid choice. Please enter a number from 1 to 4.")

def view_longest_streak_menu(habit_database, periodicity):
    pass


if __name__ == "__main__":
    habit_database = HabitDatabase() 
    try:        
        main(habit_database)
    finally:
        habit_database.close()
