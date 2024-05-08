import pytest
from habit_tracker_predefined import get_predefined_daily_habits, get_predefined_weekly_habits

@pytest.fixture
def habit_data():
    return [
        {"id": 1, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/1/2024", "completion_time": "23:29:27"},
        {"id": 32, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/6/2024", "completion_time": "18:23:58"},
        {"id": 50, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/4/2024", "completion_time": "20:37:55"},
        {"id": 64, "name": "Clean House", "description": "Do household chores", "periodicity": "Weekly", "created_date": "3/1/2024 19:45", "completion_date": "3/1/2024", "completion_time": "21:55:33"},
        {"id": 67, "name": "Call Family", "description": "Check in with family members", "periodicity": "Weekly", "created_date": "3/4/2024 16:15", "completion_date": "3/9/2024", "completion_time": "23:59:59"}
    ]

def test_get_predefined_daily_habits(habit_data):
    expected_habits = [
        {"id": 1, "name": "Study", "description": "Study current module", "periodicity": "Daily", "created_date": "3/1/2024 17:06", "completion_date": "3/1/2024", "completion_time": "23:29:27"},
        {"id": 32, "name": "Code", "description": "Practice coding", "periodicity": "Daily", "created_date": "3/5/2024 17:37", "completion_date": "3/6/2024", "completion_time": "18:23:58"},
        {"id": 50, "name": "Research", "description": "Do some research", "periodicity": "Daily", "created_date": "3/3/2024 17:37", "completion_date": "3/4/2024", "completion_time": "20:37:55"},
    ]
    habits = get_predefined_daily_habits(habit_data)
    assert habits == expected_habits

def test_get_predefined_weekly_habits(habit_data):
    expected_habits = [
        {"id": 64, "name": "Clean House", "description": "Do household chores", "periodicity": "Weekly", "created_date": "3/1/2024 19:45", "completion_date": "3/1/2024", "completion_time": "21:55:33"},
        {"id": 67, "name": "Call Family", "description": "Check in with family members", "periodicity": "Weekly", "created_date": "3/4/2024 16:15", "completion_date": "3/9/2024", "completion_time": "23:59:59"},
    ]
    habits = get_predefined_weekly_habits(habit_data)
    assert habits == expected_habits
