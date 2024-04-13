from database import HabitDatabase
from habit import Habit
from initialize_database import initialize_database
from analytics import *


def main():
    """Main function to initialize and run the Habit Tracker."""
    initialize_database()
       
    habit_database = HabitDatabase()
    
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip().lower()  
        
        if choice == "1":
            add_habit(habit_database)
        elif choice == "2":
            delete_habit(habit_database)
        elif choice == "3":
            view_habits(habit_database)
        elif choice == "4":
            check_habit_status(habit_database)
        elif choice == "5":
            complete_habit(habit_database)
        elif choice == "6":
            view_streaks(habit_database)
        elif choice == "7":
            view_longest_streak_for_habit(habit_database)            
        elif choice == "8":
            view_longest_streak(habit_database)            
        elif choice == "9":
            print("Exiting the Habit Tracker...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")

def print_menu():
    """Print the menu options."""
    print("1. Add habit")
    print("2. Delete habit")
    print("3. View list of habits")
    print("4. Check habit status")
    print("5. Check off completed task")
    print("6. View streaks")
    print("7. View longest streak for each habit")
    print("8. View Habit Hall of Fame")
    print("9. Quit")

def add_habit(habit_database):
    """Add a new habit."""
    habit_name = input("New habit to add: ").strip().lower() 
    habit_description = input("Habit description: ")
    while True:
        periodicity = input("Daily or Weekly?: ").strip().lower()
        if periodicity in ["daily", "weekly"]:
            break
        else:
            print("Error: Please enter either 'Daily' or 'Weekly'.")

    habit_database.add_habit(habit_name, habit_description, periodicity)
    print(f"'{habit_name}' successfully added!\n")

def delete_habit(habit_database):
    """Delete an existing habit."""
    habit_name = input("Existing habit to delete: ").strip().lower()  
    habits = habit_database.get_habits()
    habit_names = [habit['name'].lower() for habit in habits]  
    if habit_name in habit_names:  
        try:
            habit_database.delete_habit(habit_name)
            print(f"'{habit_name}' successfully deleted!\n")
        except ValueError as e:
            print(e)
    else:
        print(f"'{habit_name}' does not exist.\n")

def view_habits(habit_database):
    """View the list of habits."""
    while True:
        filter_option = input("Do you want to filter by periodicity? (yes/no): ").strip().lower()
        if filter_option == "yes":
            filter_by_periodicity(habit_database)
            break
        elif filter_option == "no":
            habits = habit_database.get_habits()
            print("Habit List (All):")
            for habit in habits:
                print(f"- {habit['name']}: {habit['description']}")
            print()
            break
        else:
            print("Error: Please enter 'yes' or 'no'.")

def filter_by_periodicity(habit_database):
    """Filter habits by periodicity."""
    while True:
        periodicity = input("Enter 'Daily' or 'Weekly': ").strip().lower()
        if periodicity == "daily":
            habits = habit_database.get_habits_by_periodicity("daily")
            print("Habit List (Daily):")
            for habit in habits:
                print(f"- {habit['name']}: {habit['description']}")
            print()
            break
        elif periodicity == "weekly":
            habits = habit_database.get_habits_by_periodicity("weekly")
            print("Habit List (Weekly):")
            for habit in habits:
                print(f"- {habit['name']}: {habit['description']}")
            print()
            break
        else:
            print("Error: Please enter either 'Daily' or 'Weekly'.")

def check_habit_status(habit_database):
    """Check the status of a habit."""
    habit_name = input("Enter the name of the habit to check its status: ").strip().lower()   
    status = habit_database.check_habit_status(habit_name)
    if status is not None:
        if status == "consistently_followed":
            print(f"'{habit_name}' is consistently followed. Keep it up!")
        elif status == "inconsistent":
            print(f"You're finding it challenging to stick to '{habit_name}'. Aim for better consistency.")
    else:
        print(f"'{habit_name}' does not exist.\n")

def complete_habit(habit_database):
    """Mark a habit as completed."""
    habit_name = input("Enter the name of the habit you want to mark as completed: ").strip().lower()  
    try:
        habit_database.complete_habit(habit_name)
        streak = habit_database.get_streak_for_habit(habit_name)
        if streak is not None:
            habit_database.update_streak(habit_name, streak + 1)
            print(f"'{habit_name}' marked as completed.")
            if streak == 0:
                print(f"You've started tracking '{habit_name}'.")
            else:
                print(f"Keep it up! Your streak for '{habit_name}' is now {streak + 1}.")
        else:
            habit_database.update_streak(habit_name, 0)
            print(f"Oops! You missed completing '{habit_name}' within the specified period.")
            print(f"Your streak for '{habit_name}' has been reset to 0.")
    except ValueError as e:
        print(e)

def view_streaks(habit_database):
    """View streaks for habits."""
    streaks = habit_database.view_streaks()
    print("Habit Streaks:")
    for habit, streak in streaks.items():
        print(f"- {habit}: {streak} days")
    print()

def view_longest_streak_for_habit(habit_database):
    """View the longest streak for a specific habit."""
    habit_name = input("Enter the name of the habit: ").strip().lower()  
    habit = habit_database.get_habit_by_name(habit_name)
    if habit:
        longest_streak = get_longest_streak_for_habit(habit_database, habit['name'])
        print(f"The longest streak for habit '{habit_name}' is {longest_streak} days.")
    else:
        print(f"The habit '{habit_name}' does not exist.")

def view_longest_streak(habit_database):
    """View the longest streak for all habits."""
    longest_streak_habit, longest_streak = get_longest_streak(habit_database)
    if longest_streak_habit:
        print(f"{longest_streak_habit} earns a spot in the Habit Hall of Fame with the longest streak of {longest_streak} days!")
    else:
        print("No habits tracked yet.")



if __name__ == "__main__":
    main()
