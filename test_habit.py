import pytest
from habit import Habit
from database import HabitDatabase
from initialize_database import initialize_database

@pytest.fixture
def habit_database():
    """Fixture to create a HabitDatabase instance for testing."""
    initialize_database()
    return HabitDatabase()

def test_habit_creation():
    created_date = "2024-04-13"
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
    assert habit.name == "Exercise"
    assert habit.task_specification == "Do workout for 30 minutes"
    assert habit.periodicity == "daily"
    assert habit.created_date == created_date  

def test_complete_task(habit_database):
    created_date = "2024-04-13"
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
    habit.store(habit_database)
    habit = habit_database.get_habit_by_name("Exercise")
    habit.complete_task()
    assert len(habit.completed_tasks) == 1

def test_update_streak_continues(habit_database):
    created_date = "2024-04-13"
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
    habit.store(habit_database)
    habit = habit_database.get_habit_by_name("Exercise")
    habit.complete_task()
    assert habit.streak == 1

def test_update_streak_breaks(habit_database):
    created_date = "2024-04-13"
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
    habit.store(habit_database)
    habit = habit_database.get_habit_by_name("Exercise")
    habit.complete_task() 
    habit.complete_task() 
    assert habit.streak == 1

def test_reset_streak(habit_database):
    created_date = "2024-04-13"
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
    habit.store(habit_database)
    habit = habit_database.get_habit_by_name("Exercise")
    habit.complete_task() 
    assert habit.streak == 1
    habit.complete_task() 
    assert habit.streak == 1

def test_habit_completion_multiple_days(habit_database):
    created_date = "2024-04-13"
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
    habit.store(habit_database)
    habit = habit_database.get_habit_by_name("Exercise")
    for _ in range(5):
        habit.complete_task()
    assert habit.streak == 5

def test_habit_completion_outside_period(habit_database):
    created_date = "2024-04-13"
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
    habit.store(habit_database)
    habit = habit_database.get_habit_by_name("Exercise")
    habit.last_completed = "2024-04-15"  
    habit.complete_task()
    assert habit.streak == 0
