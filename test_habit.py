import pytest
from habit import Habit
from datetime import datetime

def test_habit_creation():
    created_date = datetime.now().date()  
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
    assert habit.name == "Exercise"
    assert habit.task_specification == "Do workout for 30 minutes"
    assert habit.periodicity == "daily"
    assert habit.created_date == created_date  

def test_complete_task():
    created_date = datetime.now().date()  
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
    habit.complete_task()
    assert len(habit.completed_tasks) == 1

def test_update_streak_continues():
    created_date = datetime.now().date()  
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
    habit.complete_task()
    assert habit.streak == 1

def test_update_streak_breaks():
    created_date = datetime.now().date()  
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
    habit.complete_task() 
    habit.complete_task() 
    assert habit.streak == 1

def test_update_streak_reset():
    created_date = datetime.now().date() 
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
    habit.complete_task() 
    assert habit.streak == 1
    habit.complete_task() 
    assert habit.streak == 1

def test_habit_with_streak_spanning_multiple_periods():
    created_date = datetime.now().date()  
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
  
    for _ in range(5):
        habit.complete_task()
    
    habit.complete_task()
    
    assert habit.streak == 1

def test_habit_creation_with_created_date():
    created_date = datetime.now().date()  
    habit = Habit("Exercise", "Do workout for 30 minutes", "daily", created_date)
    assert habit.name == "Exercise"
    assert habit.task_specification == "Do workout for 30 minutes"
    assert habit.periodicity == "daily"
    assert habit.created_date == created_date  
